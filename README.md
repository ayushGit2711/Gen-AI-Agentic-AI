# GEN AI & LLM Projects – Agentic AI Workflows

This repository is a curated collection of hands-on projects exploring the development of Generative AI (GenAI), Large Language Models (LLMs), and Agentic AI workflows using tools like LangChain, LangGraph, Streamlit, MCP, and Gemini.

These projects demonstrate how to build intelligent, autonomous agents capable of reasoning, planning, and interacting with various tools and environments. The goal is to provide practical, modular, and extensible examples suitable for developers, researchers, and enthusiasts.

---

## Features

- LangGraph-based chatbots and agent workflows  
- Prebuilt and custom tool integrations  
- Retrieval-Augmented Generation (RAG) with Chroma  
- Streamlit UI for chat and multimodal interaction  
- MCP integration for filesystem and GitHub access  
- Custom MCP server implementations  
- Multi-agent systems (Supervisor and Swarm architectures)  
- Gemini-powered image generation and captioning  

---

## Getting Started

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt



## Environment Variables

Create a `.env` file with the following keys:

```ini
OPENAI_API_KEY=your_openai_key  
GROQ_API_KEY=your_groq_key  
GITHUB_TOKEN=your_github_token  
GOOGLE_API_KEY=your_google_api_key  
```

---

## Key Projects

### LangGraph Chatbot
- Basic chatbot implementation using LangGraph’s `StateGraph`
- Supports both OpenAI (`gpt-4o`) and Groq (`llama-3.3-70b-versatile`) models

### Prebuilt Agents
- Use LangGraph's `create_react_agent` with or without tools
- Example tools: weather fetcher, file system manipulator

### Streaming UI with Streamlit
- Chat UI powered by Streamlit with memory checkpointing
- Maintains message history and dynamically streams assistant output

### Structured Responses
- Generate structured replies using Pydantic models
- Examples: email generation, travel itineraries, health reports

### RAG with Chroma
- Load content from external sources using `WebBaseLoader`
- Chunk and store data in a Chroma vectorstore
- Retrieve relevant info on demand for context-aware answers

### MCP Integrations
- Connect to GitHub and filesystem MCP servers
- List files, create/edit files, execute file operations securely

### Custom MCP Server
- Create tools like `addFile()` and `addFolder()` with FastMCP
- Use in agent workflows to manipulate local directories

### Gemini Multimodal Applications
- Generate images from text or captions from uploaded images
- Streamlit UI for interacting with Gemini models

---

## Multi-Agent Architectures

### Supervisor Architecture
Example agents:
- Resume Reviewer
- Mock Interviewer
- Feedback Generator
- Document Validator

### Swarm Architecture
Example agents:
- Researcher
- Summarizer
- Critic
- Fact Checker

Related repositories:
- [LangGraph Supervisor](https://github.com/langchain-ai/langgraph-supervisor-py)
- [LangGraph Swarm](https://github.com/langchain-ai/langgraph-swarm-py)

---

## Local Model Execution with Ollama

- Run LLaMA, Mistral, Gemma models offline
- No internet needed after model download  
More at: [https://ollama.com](https://ollama.com)

---

## Documentation and References

- [LangChain](https://python.langchain.com/docs/introduction)  
- [LangGraph](https://langchain-ai.github.io/langgraph/)  
- [MCP Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)  
- [Streamlit](https://docs.streamlit.io/)  
- [Gemini API](https://ai.google.dev/gemini-api/docs/)  
- [HuggingFace](https://huggingface.co)  



