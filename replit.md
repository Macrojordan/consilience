# LLM Council - Replit Project

## Overview
LLM Council is a web application that queries multiple AI models through OpenRouter, allows them to review each other's responses, and synthesizes a final answer. It's designed to leverage the collective intelligence of various LLMs (GPT, Gemini, Claude, Grok, etc.).

## Project Structure
- **Backend**: Python FastAPI server (port 8001)
  - Location: `backend/` directory
  - Main entry: `backend/main.py`
  - Configuration: `backend/config.py`
  - Storage: JSON files in `data/conversations/`
  
- **Frontend**: React + Vite (port 5000)
  - Location: `frontend/` directory
  - Entry point: `frontend/src/main.jsx`
  - API client: `frontend/src/api.js`

## Configuration for Replit

### Environment Variables
- **OPENROUTER_API_KEY** (Secret): Required for API access to OpenRouter
  - Get your key at https://openrouter.ai/
  - Stored in Replit Secrets

### Port Configuration
- Frontend: Port 5000 (configured for Replit webview)
- Backend: Port 8001 (internal)

### Vite Configuration
The Vite dev server is configured to:
- Run on host `0.0.0.0` (required for Replit)
- Use port 5000
- Handle HMR over WSS with clientPort 443

### CORS Configuration
Backend allows all origins to support Replit's proxy infrastructure.

## Recent Changes (Nov 26, 2024)
1. Configured Vite to run on port 5000 with proper host settings
2. Updated backend CORS to allow Replit domains
3. Modified backend to use localhost (127.0.0.1) for internal backend server
4. Updated frontend API client to dynamically detect Replit environment and use correct backend URL
5. Set up workflow to run both backend and frontend together
6. Configured deployment for autoscale with build and run commands

## How It Works
1. **Stage 1**: User query sent to all council LLMs individually
2. **Stage 2**: Each LLM reviews and ranks other LLMs' responses anonymously
3. **Stage 3**: Chairman LLM synthesizes final response from all inputs

## Dependencies
- **Python**: FastAPI, uvicorn, httpx, pydantic, python-dotenv (managed via uv)
- **JavaScript**: React, Vite, react-markdown (managed via npm)

## Running Locally
The workflow automatically runs both servers:
```bash
uv run python -m backend.main & cd frontend && npm run dev
```

## Deployment
Configured for Replit autoscale deployment:
- Build: Installs and builds frontend
- Run: Starts both backend and frontend servers
