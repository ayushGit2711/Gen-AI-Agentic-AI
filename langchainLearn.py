from dotenv import load_dotenv
import getpass
import os

load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

from langchain.chat_models import init_chat_model

model = init_chat_model("llama3-8b-8192", model_provider="groq")
response = model.invoke("Hi What's up?")
print(response)