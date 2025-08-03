from dotenv import load_dotenv
load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent


import streamlit as st


st.title("HelllaaaW, Welcome to my Chatbot App")


if "messages" not in st.session_state:
   st.session_state.messages = []




checkpointer = InMemorySaver()


agent = create_react_agent(
   model="openai:gpt-4o", 
   tools=[], 
   checkpointer=checkpointer,
   prompt="You are a helpful assistant" 
)


def stream_graph_updates(user_input: str):
    assistant_response = ""
    # Add the new user message to the history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Send the full history to the agent
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        for event in agent.stream({"messages": st.session_state.messages}, {"configurable": {"thread_id": "def"}}):
            for value in event.values():
                new_text = value["messages"][-1].content
                assistant_response += new_text
                message_placeholder.markdown(assistant_response)
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})




# Display previous chat history
for role, message in st.session_state.messages:
   with st.chat_message(role):
       st.markdown(message)


prompt = st.chat_input("What is your question?")
if prompt:
   # Display user input as a chat message
   with st.chat_message("user"):
       st.markdown(prompt)
   # Append user input to session state
   st.session_state.messages.append(("user", prompt))
  
   # Get response from the chatbot based on user input
   response = stream_graph_updates(prompt)