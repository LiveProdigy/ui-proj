"""
Main API router for agent orchestration endpoints
"""

import uuid
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query, Path
from pydantic import BaseModel, Field

from app.orchestrator.agent_orchestrator import AgentOrchestrator

router = APIRouter()
orchestrator = AgentOrchestrator()


# Request and response models
class AgentRequest(BaseModel):
    """Agent request model"""
    query: str = Field(..., description="User's query or goal")
    session_id: Optional[str] = Field(None, description="Session ID for context continuity")


class AgentResponse(BaseModel):
    """Agent response model"""
    session_id: str = Field(..., description="Session ID for this conversation")
    agent_used: Optional[str] = Field(None, description="The agent that processed the request")
    output: Optional[str] = Field(None, description="Agent's response")
    error: Optional[str] = Field(None, description="Error message if something went wrong")


class ToolsResponse(BaseModel):
    """Tools response model"""
    tools: List[Dict[str, Any]] = Field(..., description="Available MCP tools")


class StatusResponse(BaseModel):
    """Status response model"""
    status: str = Field(..., description="Status of the agent workflow")
    details: Dict[str, Any] = Field({}, description="Additional status details")


# Agent endpoints
@router.post("/run_agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Run an agent workflow with the given query"""
    try:
        # Generate a new session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Run the agent workflow
        result = await orchestrator.run_workflow(
            user_input=request.query,
            session_id=session_id
        )
        
        return AgentResponse(
            session_id=session_id,
            agent_used=result.get("agent_used"),
            output=result.get("output"),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running agent: {str(e)}"
        )


@router.get("/status/{session_id}", response_model=StatusResponse)
async def get_status(session_id: str = Path(..., description="Session ID to check")):
    """Get the status of an agent workflow"""
    # In a real implementation, this would check the status of a running workflow
    # For now, we'll just return a placeholder
    return StatusResponse(
        status="completed",  # or "running", "queued", "failed"
        details={
            "session_id": session_id,
            "progress": 100,
            "updated_at": "2025-10-06T12:00:00Z"
        }
    )


@router.get("/tools", response_model=ToolsResponse)
async def list_tools():
    """List available MCP tools and integrations"""
    # In a real implementation, this would dynamically discover available tools
    return ToolsResponse(
        tools=[
            {
                "name": "github",
                "description": "GitHub repository interaction",
                "status": "active",
                "capabilities": ["read", "write", "issue_management", "pr_management"]
            }
            # Additional tools would be listed here as they become available
        ]
    )