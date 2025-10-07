# AI Agent Orchestration System

An advanced backend system for orchestrating multiple AI agents using Python, LangGraph, and FastAPI. The system includes specialized agents for GitHub interaction, proposal validation, lead generation, and personalized outreach, all coordinated by a central orchestrator.

## 🌟 Features

### Core Orchestration Layer
- **Agent Orchestrator**: Manages multiple AI agents, coordinates request flow, and tracks tool usage
- **LangGraph Workflow**: Intelligent routing and chaining of agent workflows

### Specialized Agents
- 🧩 **GitHub Agent**: Interacts with repositories (read, commit, PR, issues)
- 🧠 **Proposal Validator**: Analyzes PR descriptions or ideas for clarity & feasibility
- 🔍 **Lead Generation Agent**: Scans repositories for potential contributors or insights
- ✉️ **Outreach Agent**: Drafts personalized emails or issue replies

### MCP (Model Context Protocol) Layer
- **GitHub MCP Server**: Provides standardized API for repository access
- **Extensible Architecture**: Ready for more MCP integrations (Trello, Slack, Notion)

### Meeting Intelligence
- **Audio Processing**: Capture meeting audio and transcribe conversations
- **Speaker Identification**: Distinguish between different speakers
- **Insight Extraction**: Identify key topics, action items, and decisions
- **Summary Generation**: Create concise meeting summaries
- **Integration Ready**: Works with Teams, Slack, and Outlook

### Storage & State Management
- **Context Store**: In-memory or Redis-based session context storage
- **Persistent Logging**: Track agent activities and outputs

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker (optional, for Redis)
- OpenAI API key
- GitHub API token (for GitHub agent functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root with the following variables:
   ```
   # OpenAI API
   OPENAI_API_KEY=your_openai_api_key

   # GitHub API
   GITHUB_TOKEN=your_github_token

   # Server configuration
   PORT=8000
   GITHUB_MCP_PORT=8001

   # Storage configuration
   USE_REDIS=false
   REDIS_URL=redis://localhost:6379/0
   CONTEXT_TTL_SECONDS=3600

   # Meeting Intelligence
   ENABLE_MEETING_INTELLIGENCE=true
   ```

### Running the Application

1. **Start the main FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Start the GitHub MCP server** (in a separate terminal)
   ```bash
   uvicorn app.mcp.github_server:app --port 8001 --reload
   ```

3. **Optional: Start Redis** (if USE_REDIS=true in .env)
   ```bash
   docker run -d -p 6379:6379 redis
   ```

### API Endpoints

#### Agent Orchestration
- `POST /api/run_agent`: Run an agent workflow with the given query
- `GET /api/status/{session_id}`: Get the status of an agent workflow
- `GET /api/tools`: List available MCP tools and integrations

#### Meeting Intelligence
- `POST /meeting/upload`: Upload and process a meeting recording
- `POST /meeting/webhook/{platform}`: Webhook for meeting platform integrations
- `GET /meeting/transcript/{meeting_id}`: Get a meeting transcript
- `GET /meeting/insights/{meeting_id}`: Get insights from a meeting

## 📁 Project Structure

```
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Project dependencies
├── app/
│   ├── __init__.py
│   ├── agents/             # Specialized agent modules
│   │   ├── __init__.py
│   │   ├── base.py         # Base agent class
│   │   ├── github_agent.py
│   │   ├── lead_generation.py
│   │   ├── outreach.py
│   │   └── proposal_validator.py
│   ├── api/                # FastAPI routers
│   │   ├── __init__.py
│   │   ├── meeting_intelligence.py
│   │   └── router.py
│   ├── mcp/                # Model Context Protocol layer
│   │   ├── __init__.py
│   │   ├── github_client.py
│   │   └── github_server.py
│   ├── meeting_intelligence/  # Meeting analysis features
│   │   ├── __init__.py
│   │   └── processor.py
│   ├── orchestrator/       # Agent orchestration logic
│   │   ├── __init__.py
│   │   └── agent_orchestrator.py
│   └── storage/            # State and context management
│       ├── __init__.py
│       └── context_store.py
```

## 🧪 Testing

Run the test suite with:
```bash
pytest
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for API development
- [OpenAI](https://openai.com/) for LLM capabilities