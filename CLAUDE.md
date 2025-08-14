# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

This project uses `uv` as the package manager and virtual environment tool.

**Initial setup:**
```bash
uv venv
source .venv/bin/activate
uv add .
uv add ".[dev]"
```

## Running the Project

**Start MCP Server:**
```bash
uv run mcp dev server.py
```

**Run the agent (in separate terminal):**
```bash
source .venv/bin/activate
uv run singleflowagent.py
```

**Test MCP server tools:**
```bash
uv run mcp dev server.py
```

## Architecture Overview

This is an MCP (Model Context Protocol) server implementation that provides employee churn prediction capabilities through integration with a FastAPI ML service.

### Core Components

**server.py** - MCP server using FastMCP framework
- Implements `PredictChurn` tool that accepts employee data
- Makes HTTP requests to external ML API (configurable via `MODEL_API_URL` env var)
- Handles batch predictions and error cases
- Runs as HTTP transport server for deployment

**singleflowagent.py** - Bee Framework agent implementation
- Uses Bee Framework's AgentWorkflow for ReAct-style interactions
- Connects to MCP server via stdio transport using `uv run server.py`
- Configured with Ollama model `granite3.1-dense:8b`
- Implements event handling for agent execution tracking

### Key Dependencies

- `mcp[cli]>=1.3.0` - Model Context Protocol implementation
- `fastmcp>=1.0` - FastMCP server framework
- `beeai-framework>=0.1.4` - Agent framework for ReAct interactions
- `requests>=2.32.3` - HTTP client for ML API calls

### Environment Variables

- `MODEL_API_URL` - ML model endpoint (defaults to `http://127.0.0.1:8000/predict`)
- `MODEL_API_KEY` - Optional API key for ML service authentication
- `PORT` - Server port for HTTP transport (defaults to 8080)

### Integration Requirements

This server is designed to work with a separate FastAPI ML service for actual churn predictions. The external ML service should accept POST requests with employee data structure:
```json
{
  "YearsAtCompany": 10,
  "EmployeeSatisfaction": 0.99,
  "Position": "Non-Manager",
  "Salary": 5.0
}
```