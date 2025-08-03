import os
from dotenv import load_dotenv
load_dotenv()
import logging
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "Mozilla/5.0 ...")

st.title("🔎 RAG Website Q&A")

web_url = st.text_input("Enter the website URL to search:")
user_query = st.text_area("Enter your question:")

if st.button("Get Answer"):
    if not web_url or not user_query:
        st.warning("Please provide both a website URL and a question.")
    else:
        with st.spinner("Loading and processing website..."):
            loader = WebBaseLoader(web_paths=[web_url])
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents(docs)
            embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
            vectorstore = Chroma(
                collection_name="generic_info",
                embedding_function=embeddings,
                persist_directory="./chroma_generic"
            )
            if vectorstore._collection.count() == 0:
                vectorstore.add_documents(documents=all_splits)
                logging.info("Documents added to vectorstore.")
            else:
                logging.info("Vectorstore already contains documents.")

            @tool
            def retrieve_context(query: str, k: int = 3):
                """Search for info from the loaded website"""
                try:
                    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})
                    results = retriever.invoke(query)
                    if not results:
                        logging.warning(f"No results found for '{query}'.")
                        return f"No results found for '{query}'."
                    content = "\n\n".join([
                        f"Source: {doc.metadata.get('source', 'N/A')}\n{doc.page_content}"
                        for doc in results
                    ])
                    logging.info(f"Retrieved {len(results)} documents for query: '{query}'")
                    return content
                except Exception as e:
                    logging.error(f"Error retrieving info for '{query}': {e}")
                    return f"Error retrieving info for '{query}'. Please try again."

            llm = init_chat_model("gpt-4o", model_provider="openai")
            agent_executor = create_react_agent(llm, [retrieve_context])

            answer = ""
            for event in agent_executor.stream(
                {"messages": [{"role": "user", "content": user_query}]},
                stream_mode="values"
            ):
                answer += event["messages"][-1].content

            st.subheader("Answer")
            st.write(answer)


