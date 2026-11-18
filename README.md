# Model Context Protocol (MCP) – Python Implementation

A practical implementation of the **Model Context Protocol (MCP)** using Python, demonstrating how to build MCP servers, connect MCP clients, and integrate external tools with Large Language Models (LLMs).

This project explores two MCP communication transports — **STDIO and Streamable HTTP** — and demonstrates how AI applications can discover and execute external tools through MCP.

## 🚀 Project Overview

The Model Context Protocol (MCP) is an open standard that enables AI applications to communicate with external tools, services, and data sources through a standardized interface.

This project demonstrates how to:

- Build MCP servers using Python and FastMCP.
- Implement STDIO and Streamable HTTP transports.
- Develop MCP clients using LangChain MCP Adapters.
- Connect multiple MCP servers to a single client.
- Integrate MCP tools with LLMs using LangChain.
- Execute external API operations through MCP tools.
- Connect to GitHub's hosted MCP server.

## ✨ Features

### 1. MCP Server Implementation

Two different MCP server implementations are included:

**STDIO MCP Server**
- Uses Standard Input/Output for communication.
- Suitable for locally running MCP servers.
- Exposes tools to compatible MCP clients.

**Streamable HTTP MCP Server**
- Uses Streamable HTTP transport.
- Runs as an HTTP-based MCP service.
- Allows clients to connect through an HTTP endpoint.

### 2. Available MCP Tools

The project implements tools that allow LLM applications to interact with external services.

| Tool | Description |
|---|---|
| `get_current_weather` | Retrieves current weather information for Indian cities. |
| `get_current_date_time` | Returns the current date and time in ISO format. |
| `search_tmdb` | Searches for movies, TV shows, and people using the TMDB API. |

### 3. MCP Client Implementation

The project demonstrates different ways of connecting MCP clients to servers.

- STDIO MCP Client – launches and communicates with a local MCP server.
- HTTP MCP Client – connects to a Streamable HTTP MCP server.
- Multi-server MCP Client – demonstrates connecting to multiple MCP servers using different transports.
- GitHub MCP Client – connects to GitHub's hosted MCP endpoint.

### 4. LLM Integration

The project integrates Large Language Models using LangChain.

LLM integration enables:
- Dynamic tool selection based on user queries.
- Automatic tool invocation.
- Passing tool results back to the LLM.
- Generating responses using external tool outputs.
- Conversational interaction with tool-enabled AI applications.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| MCP Python SDK | MCP server development |
| FastMCP | Creating MCP tools and servers |
| LangChain | LLM integration and tool calling |
| LangChain MCP Adapters | Connecting MCP clients and servers |
| LangChain Groq | Groq LLM integration |
| LangChain NVIDIA AI Endpoints | NVIDIA model integration |
| Requests | External API communication |
| Python-dotenv | Environment variable management |
| Open-Meteo API | Weather and geocoding data |
| TMDB API | Movie and TV information |

## 📁 Project Structure

```text
Model-Context-Protocal/
│
├── main.py
│
├── mcpserver_stdio.py
├── mcpserver_http.py
│
├── mcpclient_stdio.py
├── mcpclient_http.py
│
├── github_mcp_client.py
│
├── README.md
│
└── .env
```

### File Descriptions

| File | Description |
|---|---|
| `main.py` | Demonstrates traditional LangChain tool calling with weather and date/time tools. |
| `mcpserver_stdio.py` | Implements an MCP server using STDIO transport. |
| `mcpserver_http.py` | Implements an MCP server using Streamable HTTP transport. |
| `mcpclient_stdio.py` | Connects an MCP client to a local STDIO server. |
| `mcpclient_http.py` | Demonstrates connecting to HTTP and STDIO MCP servers. |
| `github_mcp_client.py` | Connects to GitHub's hosted MCP server and demonstrates GitHub tool discovery and invocation. |

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/chandupradeep18/Model-Context-Protocal.git

cd Model-Context-Protocal
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install mcp requests python-dotenv langchain langchain-groq langchain-nvidia-ai-endpoints langchain-mcp-adapters
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
NVIDIA_API_KEY=your_nvidia_api_key
TMDB_ACCESS_TOKEN=your_tmdb_access_token
GITHUB_API=your_github_personal_access_token
```

**Note:**
- Groq API key is required for Groq-powered LLM examples.
- NVIDIA API key is required when using NVIDIA models.
- TMDB access token is required for movie and TV search functionality.
- GitHub token is required for the GitHub MCP client example.
- Only configure the credentials required for the example you intend to run.

Never commit your `.env` file or expose API keys in your repository.

## ▶️ Running the Project

### 1. Run the STDIO MCP Server

```bash
python mcpserver_stdio.py
```

The server starts using STDIO transport and waits for an MCP-compatible client.

### 2. Run the STDIO MCP Client

Open another terminal and execute:

```bash
python mcpclient_stdio.py
```

The client launches the local STDIO MCP server, discovers available tools, and integrates them with the Groq LLM.

### 3. Run the HTTP MCP Server

```bash
python mcpserver_http.py
```

The server starts using Streamable HTTP transport.

### 4. Run the HTTP MCP Client

Open another terminal:

```bash
python mcpclient_http.py
```

The client demonstrates connecting to both the local HTTP MCP server and the STDIO MCP server.

### 5. Run the Traditional Tool Calling Example

```bash
python main.py
```

This example demonstrates how an LLM can select and execute Python tools using LangChain without an MCP server.

### 6. Run the GitHub MCP Client

```bash
python github_mcp_client.py
```

This example connects to GitHub's hosted MCP endpoint and demonstrates discovering and invoking GitHub tools.

## 💡 Example Use Cases

Once the MCP client and servers are configured, you can explore queries such as:

**Weather Information**

```text
What is the current weather in Tanuku?
```

**Date and Time**

```text
What is the current date and time?
```

**Movie Search**

```text
Search for movies related to Avengers.
```

The LLM can identify the appropriate tool, invoke it, and use the returned information to generate a response.

## 🏗️ MCP Architecture

The project follows this general architecture:

```text
              User Query
                   |
                   v
             LLM Application
              (LangChain)
                   |
                   v
              MCP Client
                   |
          +--------+--------+
          |                 |
          v                 v
     STDIO Transport   Streamable HTTP
          |                 |
          v                 v
      MCP Server        MCP Server
          |                 |
          +--------+--------+
                   |
                   v
             Available Tools
                   |
          +--------+--------+
          |        |        |
          v        v        v
        Weather  Date/Time  TMDB
          |        |        |
          +--------+--------+
                   |
                   v
             Tool Response
                   |
                   v
              MCP Client
                   |
                   v
                  LLM
                   |
                   v
             Final Response
```

## 📚 Learning Objectives

This project is intended to provide practical experience with:

- Understanding the Model Context Protocol.
- Building MCP servers and clients.
- Understanding STDIO and Streamable HTTP transports.
- Registering and exposing tools through MCP.
- Discovering tools dynamically from MCP servers.
- Integrating MCP with LangChain.
- Connecting LLMs with external APIs.
- Understanding the difference between traditional function calling and MCP-based tool integration.

## 🔮 Future Improvements

- Implement MCP Resources and Prompts.
- Add authentication and authorization for HTTP MCP servers.
- Add more external API integrations.
- Implement error handling and logging.
- Add structured output validation.
- Integrate MCP with LangGraph agents.
- Implement automated testing for MCP tools.
- Add Docker support for deployment.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If you find an issue or have an idea to improve this project, feel free to open an issue or submit a pull request.

## 📖 References

- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [LangChain Documentation](https://python.langchain.com/docs/introduction/)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- [Groq Documentation](https://console.groq.com/docs)
- [TMDB API Documentation](https://developer.themoviedb.org/docs)

---

**Author:** [Chandu Pradeep](https://github.com/chandupradeep18)

**GitHub Repository:** [Model Context Protocol](https://github.com/chandupradeep18/Model-Context-Protocal)

⭐ If
