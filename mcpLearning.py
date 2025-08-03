from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def run_agent():
   client = MultiServerMCPClient(
       {
           "github": {
               "command": "npx",
               "args": [
                   "-y",
                   "@modelcontextprotocol/server-github"
               ],
               "env": {
                   "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
               },
               "transport": "stdio"
           },
           "PersonalFileSystem": {
               "command": "python",
               "args": [
                   "./mcp_fileServer.py"
               ],
               "transport":"stdio"
           }

       }
   )
   tools = await client.get_tools()
   agent = create_react_agent("openai:gpt-4o", tools)
   response = await agent.ainvoke({"messages": "delete a folder named 'tempLearning' in the  directory(C:\\Users\\agoyal\\OneDrive - MathWorks\\Desktop\\C++_Training) "})
   print(response["messages"][-1].content)


if __name__ == "__main__":
   asyncio.run(run_agent())
