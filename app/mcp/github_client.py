"""
GitHub MCP Client - Provides a standardized API for repository access
"""

import os
from typing import Dict, Any, List, Optional
import httpx


class GitHubMCPClient:
    """
    GitHub MCP (Model Context Protocol) Client
    
    This client interacts with the GitHub MCP server, which provides
    a standardized API for repository access.
    """
    
    def __init__(self):
        """Initialize the GitHub MCP client"""
        # Get the MCP server URL from environment variables or use default
        self.base_url = os.getenv("GITHUB_MCP_URL", "http://localhost:8001/github")
        self.timeout = 30  # Request timeout in seconds
    
    async def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the GitHub MCP server"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    # Repository operations
    
    async def get_repository_data(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository metadata"""
        endpoint = f"repos/{owner}/{repo}"
        return await self._make_request(endpoint)
    
    async def list_repository_files(self, owner: str, repo: str, path: str = "") -> List[str]:
        """List files in a repository directory"""
        endpoint = f"repos/{owner}/{repo}/contents/{path}"
        response = await self._make_request(endpoint)
        
        if "error" in response:
            return []
        
        return [item["path"] for item in response]
    
    async def get_file_content(self, owner: str, repo: str, path: str) -> str:
        """Get content of a file in the repository"""
        endpoint = f"repos/{owner}/{repo}/contents/{path}"
        response = await self._make_request(endpoint)
        
        if "error" in response or "content" not in response:
            return ""
        
        import base64
        return base64.b64decode(response["content"]).decode("utf-8")
    
    # Contributor operations
    
    async def get_contributors(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Get contributors to a repository"""
        endpoint = f"repos/{owner}/{repo}/contributors"
        response = await self._make_request(endpoint)
        
        if "error" in response:
            return []
        
        return response
    
    # Issue operations
    
    async def list_issues(self, owner: str, repo: str, state: str = "open", limit: int = 30) -> List[Dict[str, Any]]:
        """List issues in a repository"""
        endpoint = f"repos/{owner}/{repo}/issues?state={state}&per_page={limit}"
        response = await self._make_request(endpoint)
        
        if "error" in response:
            return []
        
        return response
    
    async def get_issue(self, owner: str, repo: str, issue_number: str) -> Dict[str, Any]:
        """Get a specific issue"""
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}"
        return await self._make_request(endpoint)
    
    async def create_issue(self, owner: str, repo: str, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create a new issue"""
        endpoint = f"repos/{owner}/{repo}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        return await self._make_request(endpoint, method="POST", data=data)
    
    async def create_issue_comment(self, owner: str, repo: str, issue_number: str, body: str) -> Dict[str, Any]:
        """Create a comment on an issue"""
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/comments"
        data = {"body": body}
        return await self._make_request(endpoint, method="POST", data=data)
    
    # Pull request operations
    
    async def list_pull_requests(self, owner: str, repo: str, state: str = "open", limit: int = 30) -> List[Dict[str, Any]]:
        """List pull requests in a repository"""
        endpoint = f"repos/{owner}/{repo}/pulls?state={state}&per_page={limit}"
        response = await self._make_request(endpoint)
        
        if "error" in response:
            return []
        
        return response
    
    async def get_pull_request(self, owner: str, repo: str, pr_number: str) -> Dict[str, Any]:
        """Get a specific pull request"""
        endpoint = f"repos/{owner}/{repo}/pulls/{pr_number}"
        return await self._make_request(endpoint)
    
    async def get_pull_request_files(self, owner: str, repo: str, pr_number: str) -> List[Dict[str, Any]]:
        """Get files changed in a pull request"""
        endpoint = f"repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = await self._make_request(endpoint)
        
        if "error" in response:
            return []
        
        return response
    
    async def create_pull_request(self, owner: str, repo: str, title: str, body: str, 
                                 head: str, base: str) -> Dict[str, Any]:
        """Create a new pull request"""
        endpoint = f"repos/{owner}/{repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        return await self._make_request(endpoint, method="POST", data=data)
    
    # Commit operations
    
    async def get_commit_history(self, owner: str, repo: str, branch: str = "main", limit: int = 30) -> List[Dict[str, Any]]:
        """Get commit history for a branch"""
        endpoint = f"repos/{owner}/{repo}/commits?sha={branch}&per_page={limit}"
        response = await self._make_request(endpoint)
        
        if "error" in response:
            return []
        
        return response
    
    async def create_commit(self, owner: str, repo: str, branch: str, message: str, 
                           files: List[str], contents: List[str]) -> Dict[str, Any]:
        """Create a new commit"""
        endpoint = f"repos/{owner}/{repo}/commits"
        data = {
            "branch": branch,
            "message": message,
            "files": files,
            "contents": contents
        }
        return await self._make_request(endpoint, method="POST", data=data)
    
    # For synchronous code compatibility (used in Agent classes)
    
    def get_repository_data(self, owner: str, repo: str) -> Dict[str, Any]:
        """Synchronous version of get_repository_data"""
        import asyncio
        return asyncio.run(self._get_repository_data_sync(owner, repo))
    
    async def _get_repository_data_sync(self, owner: str, repo: str) -> Dict[str, Any]:
        """Helper for synchronous get_repository_data"""
        return await self.get_repository_data(owner, repo)
    
    # Similar synchronous wrappers for other async methods
    # (In a real implementation, all async methods would have synchronous wrappers)
    
    def list_repository_files(self, owner: str, repo: str, path: str = "") -> List[str]:
        """Synchronous version of list_repository_files"""
        import asyncio
        return asyncio.run(self._list_repository_files_sync(owner, repo, path))
    
    async def _list_repository_files_sync(self, owner: str, repo: str, path: str = "") -> List[str]:
        """Helper for synchronous list_repository_files"""
        return await self.list_repository_files(owner, repo, path)
    
    def get_file_content(self, owner: str, repo: str, path: str) -> str:
        """Synchronous version of get_file_content"""
        import asyncio
        return asyncio.run(self._get_file_content_sync(owner, repo, path))
    
    async def _get_file_content_sync(self, owner: str, repo: str, path: str) -> str:
        """Helper for synchronous get_file_content"""
        return await self.get_file_content(owner, repo, path)
    
    # Add other synchronous wrappers as needed for agent usage