"""
Main application entry point for the AI Agent Orchestration System
"""

import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.api.router import router as api_router
from app.api.meeting_intelligence import router as meeting_router

# Create FastAPI app
app = FastAPI(
    title="AI Agent Orchestration System",
    description="Backend for managing multiple AI agents, coordinating request flow, and tracking tool usage",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api", tags=["agents"])
app.include_router(meeting_router, prefix="/meeting", tags=["meeting"])

@app.get("/", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "AI Agent Orchestration System is running"}

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)