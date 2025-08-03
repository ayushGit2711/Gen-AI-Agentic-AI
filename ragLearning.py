import os
from dotenv import load_dotenv
load_dotenv()
import logging
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

# --- Get user input ---
web_url = input("Enter the website URL to search: ").strip()
user_query = input("Enter your question: ").strip()

# --- Load and process documents ---
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

for event in agent_executor.stream(
    {"messages": [{"role": "user", "content": user_query}]},
    stream_mode="values"
):
    event["messages"][-1].pretty_print()
