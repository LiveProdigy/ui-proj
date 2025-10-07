"""
GitHub MCP Server - Provides a standardized API for repository access via SSE or Streamable HTTP
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
import httpx
from fastapi import FastAPI, Depends, HTTPException, Body, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app for the MCP server
app = FastAPI(
    title="GitHub MCP Server",
    description="Model Context Protocol server for GitHub API access",
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


# Configuration and utilities
class GitHubClient:
    """Client for GitHub API interactions"""
    
    def __init__(self):
        """Initialize GitHub API client"""
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # Add authorization if token is available
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    async def get(self, endpoint: str) -> Dict[str, Any]:
        """Make a GET request to the GitHub API"""
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request to the GitHub API"""
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()


# Dependency to get GitHub client
async def get_github_client():
    """Get GitHub API client as a dependency"""
    return GitHubClient()


# Repository endpoints
@app.get("/github/repos/{owner}/{repo}")
async def get_repository(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get repository metadata"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/github/repos/{owner}/{repo}/contents/{path:path}")
async def get_repository_contents(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    path: str = Path("", description="File or directory path"),
    ref: str = Query(None, description="The name of the commit/branch/tag"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get contents of a file or directory in the repository"""
    try:
        endpoint = f"repos/{owner}/{repo}/contents/{path}"
        if ref:
            endpoint += f"?ref={ref}"
        
        return await github_client.get(endpoint)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Contributor endpoints
@app.get("/github/repos/{owner}/{repo}/contributors")
async def get_contributors(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get repository contributors"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}/contributors")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Issue endpoints
@app.get("/github/repos/{owner}/{repo}/issues")
async def list_issues(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    state: str = Query("open", description="Issue state (open, closed, all)"),
    per_page: int = Query(30, description="Results per page (max 100)"),
    page: int = Query(1, description="Page number"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """List repository issues"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}/issues?state={state}&per_page={per_page}&page={page}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/github/repos/{owner}/{repo}/issues/{issue_number}")
async def get_issue(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    issue_number: int = Path(..., description="Issue number"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get a specific issue"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}/issues/{issue_number}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.post("/github/repos/{owner}/{repo}/issues")
async def create_issue(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    issue_data: Dict[str, Any] = Body(..., description="Issue data"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Create a new issue"""
    try:
        return await github_client.post(f"repos/{owner}/{repo}/issues", issue_data)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.post("/github/repos/{owner}/{repo}/issues/{issue_number}/comments")
async def create_issue_comment(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    issue_number: int = Path(..., description="Issue number"),
    comment_data: Dict[str, Any] = Body(..., description="Comment data"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Create a comment on an issue"""
    try:
        return await github_client.post(f"repos/{owner}/{repo}/issues/{issue_number}/comments", comment_data)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Pull request endpoints
@app.get("/github/repos/{owner}/{repo}/pulls")
async def list_pull_requests(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    state: str = Query("open", description="PR state (open, closed, all)"),
    per_page: int = Query(30, description="Results per page (max 100)"),
    page: int = Query(1, description="Page number"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """List repository pull requests"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}/pulls?state={state}&per_page={per_page}&page={page}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/github/repos/{owner}/{repo}/pulls/{pull_number}")
async def get_pull_request(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    pull_number: int = Path(..., description="Pull request number"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get a specific pull request"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}/pulls/{pull_number}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/github/repos/{owner}/{repo}/pulls/{pull_number}/files")
async def get_pull_request_files(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    pull_number: int = Path(..., description="Pull request number"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get files changed in a pull request"""
    try:
        return await github_client.get(f"repos/{owner}/{repo}/pulls/{pull_number}/files")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.post("/github/repos/{owner}/{repo}/pulls")
async def create_pull_request(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    pr_data: Dict[str, Any] = Body(..., description="Pull request data"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Create a new pull request"""
    try:
        return await github_client.post(f"repos/{owner}/{repo}/pulls", pr_data)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Commit endpoints
@app.get("/github/repos/{owner}/{repo}/commits")
async def get_commits(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    sha: str = Query(None, description="SHA or branch to get commits from"),
    per_page: int = Query(30, description="Results per page (max 100)"),
    page: int = Query(1, description="Page number"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Get repository commits"""
    try:
        endpoint = f"repos/{owner}/{repo}/commits?per_page={per_page}&page={page}"
        if sha:
            endpoint += f"&sha={sha}"
        
        return await github_client.get(endpoint)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Server-Sent Events (SSE) endpoint example
@app.get("/github/repos/{owner}/{repo}/events")
async def repo_events_sse(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    github_client: GitHubClient = Depends(get_github_client),
):
    """Stream repository events using Server-Sent Events (SSE)"""
    async def event_generator():
        try:
            # Initial events
            events = await github_client.get(f"repos/{owner}/{repo}/events")
            yield {"event": "initial", "data": json.dumps(events)}
            
            # Continue streaming events (in a real implementation, this would use polling or webhooks)
            for i in range(10):  # Just for demonstration
                await asyncio.sleep(2)  # Wait between events
                yield {"event": "update", "data": json.dumps({"message": f"Update {i}"})}
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"error": str(e)})}
    
    return EventSourceResponse(event_generator())


# Start MCP server directly when run as a script
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("GITHUB_MCP_PORT", 8001))
    uvicorn.run("app.mcp.github_server:app", host="0.0.0.0", port=port, reload=True)