"""
GitHub Agent - Interacts with repositories (read, commit, PR, issues)
"""

import os
from typing import Dict, Any, Optional, List
import openai
from app.agents.base import BaseAgent
from app.mcp.github_client import GitHubMCPClient


class GithubAgent(BaseAgent):
    """
    GitHub Agent that can interact with GitHub repositories
    Uses MCP server as an intermediary
    """
    
    def __init__(self):
        """Initialize the GitHub agent with MCP client"""
        super().__init__()
        # Initialize the GitHub MCP client
        self.github_client = GitHubMCPClient()
        
        # System prompt for the agent
        self.system_prompt = """
        You are a GitHub Agent specialized in interacting with GitHub repositories.
        Your capabilities include:
        1. Reading repository contents
        2. Creating and reviewing pull requests
        3. Managing issues
        4. Creating commits and branches
        
        Respond with clear, concise information from the repositories you access.
        When taking actions (like creating PRs or issues), explain what you did and why.
        """
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the GitHub agent with the given query and context
        
        Args:
            query: User's query about GitHub operations
            context: Optional context with repository information
            
        Returns:
            Dictionary containing agent response and updated context
        """
        context = context or {}
        
        # Extract repository information from context or query
        repo_info = self._extract_repo_info(query, context)
        
        # Use the MCP client to get repository data as needed
        repo_data = {}
        if repo_info.get("repo_name") and repo_info.get("owner"):
            repo_data = self.github_client.get_repository_data(
                owner=repo_info["owner"],
                repo=repo_info["repo_name"]
            )
        
        # Determine the type of GitHub operation
        operation = self._determine_operation(query)
        
        # Perform the operation
        result = self._perform_operation(operation, query, repo_info, repo_data)
        
        # Update context with repository information
        updated_context = context.copy()
        updated_context.update({
            "github": {
                "last_repo": repo_info,
                "last_operation": operation,
                "last_result": result
            }
        })
        
        # Generate a response using OpenAI
        response = self._generate_response(query, operation, result)
        
        return {
            "response": response,
            "context": updated_context,
            "complete": True  # Indicate if the agent's task is complete
        }
    
    def _extract_repo_info(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract repository information from query or context"""
        # First check if we have repo info in context
        if context.get("github", {}).get("last_repo"):
            return context["github"]["last_repo"]
        
        # Otherwise try to extract from query using OpenAI
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract GitHub repository information from the text."},
                    {"role": "user", "content": f"Extract the GitHub repository owner and name from this text: '{query}'. Return JSON format with 'owner' and 'repo_name' fields. If not found, return empty strings."}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            return response.choices[0].message.content
        except Exception:
            # If extraction fails, return empty info
            return {"owner": "", "repo_name": ""}
    
    def _determine_operation(self, query: str) -> str:
        """Determine what GitHub operation is being requested"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Classify GitHub operations based on user query."},
                    {"role": "user", "content": f"Classify this query into one of these GitHub operations: 'read_repo', 'create_pr', 'review_pr', 'manage_issue', 'create_commit'. Query: '{query}'"}
                ],
                temperature=0,
            )
            
            return response.choices[0].message.content.strip().lower()
        except Exception:
            # Default to read operation if classification fails
            return "read_repo"
    
    def _perform_operation(self, operation: str, query: str, 
                          repo_info: Dict[str, Any], repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the requested GitHub operation"""
        if operation == "read_repo":
            return self._read_repository(repo_info, query)
        elif operation == "create_pr":
            return self._create_pull_request(repo_info, query)
        elif operation == "review_pr":
            return self._review_pull_request(repo_info, query)
        elif operation == "manage_issue":
            return self._manage_issue(repo_info, query)
        elif operation == "create_commit":
            return self._create_commit(repo_info, query)
        else:
            return {"error": "Unsupported operation"}
    
    def _read_repository(self, repo_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Read repository contents"""
        try:
            # Get repo contents from MCP client
            if repo_info.get("owner") and repo_info.get("repo_name"):
                files = self.github_client.list_repository_files(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                )
                
                # Extract files of interest based on query
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You help identify relevant files in a GitHub repository based on a user query."},
                        {"role": "user", "content": f"Based on this query: '{query}', which of these files would be most relevant? Files: {', '.join(files[:50])}"}
                    ],
                    temperature=0,
                )
                
                relevant_files = response.choices[0].message.content
                
                # Get content of relevant files
                file_contents = {}
                for file in files[:5]:  # Limit to first 5 for performance
                    if file.endswith('.md') or file.endswith('.py') or file.endswith('.js'):
                        content = self.github_client.get_file_content(
                            owner=repo_info["owner"],
                            repo=repo_info["repo_name"],
                            path=file
                        )
                        file_contents[file] = content
                
                return {
                    "files": files,
                    "relevant_files": relevant_files,
                    "file_contents": file_contents
                }
            else:
                return {"error": "Repository information is incomplete"}
        except Exception as e:
            return {"error": f"Error reading repository: {str(e)}"}
    
    def _create_pull_request(self, repo_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Create a pull request"""
        try:
            # Extract PR details from query
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extract pull request details from user query."},
                    {"role": "user", "content": f"Extract pull request details from this query: '{query}'. Return JSON with 'title', 'body', 'head', 'base' fields."}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            pr_details = response.choices[0].message.content
            
            # Create PR using MCP client
            if repo_info.get("owner") and repo_info.get("repo_name"):
                pr_result = self.github_client.create_pull_request(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    title=pr_details.get("title", "New Pull Request"),
                    body=pr_details.get("body", ""),
                    head=pr_details.get("head", "main"),
                    base=pr_details.get("base", "main")
                )
                
                return {
                    "pull_request": pr_result,
                    "details": pr_details
                }
            else:
                return {"error": "Repository information is incomplete"}
        except Exception as e:
            return {"error": f"Error creating pull request: {str(e)}"}
    
    def _review_pull_request(self, repo_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Review a pull request"""
        try:
            # Extract PR number from query
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract pull request number from user query."},
                    {"role": "user", "content": f"Extract the pull request number from this query: '{query}'. Return only the number."}
                ],
                temperature=0,
            )
            
            pr_number = response.choices[0].message.content.strip()
            
            # Get PR details and files using MCP client
            if repo_info.get("owner") and repo_info.get("repo_name") and pr_number:
                pr_details = self.github_client.get_pull_request(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    pr_number=pr_number
                )
                
                pr_files = self.github_client.get_pull_request_files(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    pr_number=pr_number
                )
                
                return {
                    "pull_request": pr_details,
                    "files": pr_files
                }
            else:
                return {"error": "Repository or PR information is incomplete"}
        except Exception as e:
            return {"error": f"Error reviewing pull request: {str(e)}"}
    
    def _manage_issue(self, repo_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Manage issues (create, comment, close, etc.)"""
        try:
            # Determine issue action
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Determine the issue action from the query."},
                    {"role": "user", "content": f"What issue action is requested in this query: '{query}'? Return one of: 'create', 'comment', 'close', 'list'"}
                ],
                temperature=0,
            )
            
            action = response.choices[0].message.content.strip().lower()
            
            if action == "create":
                # Extract issue details
                details_response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Extract issue creation details."},
                        {"role": "user", "content": f"Extract issue details from this query: '{query}'. Return JSON with 'title' and 'body' fields."}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )
                
                issue_details = details_response.choices[0].message.content
                
                # Create issue using MCP client
                if repo_info.get("owner") and repo_info.get("repo_name"):
                    issue = self.github_client.create_issue(
                        owner=repo_info["owner"],
                        repo=repo_info["repo_name"],
                        title=issue_details.get("title", "New Issue"),
                        body=issue_details.get("body", "")
                    )
                    
                    return {
                        "action": "create",
                        "issue": issue
                    }
            elif action == "list":
                # List issues
                if repo_info.get("owner") and repo_info.get("repo_name"):
                    issues = self.github_client.list_issues(
                        owner=repo_info["owner"],
                        repo=repo_info["repo_name"]
                    )
                    
                    return {
                        "action": "list",
                        "issues": issues
                    }
            
            return {"error": "Unsupported issue action or incomplete repository information"}
        except Exception as e:
            return {"error": f"Error managing issue: {str(e)}"}
    
    def _create_commit(self, repo_info: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Create a commit"""
        try:
            # Extract commit details from query
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extract commit details from user query."},
                    {"role": "user", "content": f"Extract commit details from this query: '{query}'. Return JSON with 'message', 'branch', 'files' (array of file paths to modify), 'changes' (array of contents to put in each file)."}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            commit_details = response.choices[0].message.content
            
            # Create commit using MCP client
            if repo_info.get("owner") and repo_info.get("repo_name"):
                commit = self.github_client.create_commit(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    branch=commit_details.get("branch", "main"),
                    message=commit_details.get("message", "Update files"),
                    files=commit_details.get("files", []),
                    contents=commit_details.get("changes", [])
                )
                
                return {
                    "commit": commit,
                    "details": commit_details
                }
            else:
                return {"error": "Repository information is incomplete"}
        except Exception as e:
            return {"error": f"Error creating commit: {str(e)}"}
    
    def _generate_response(self, query: str, operation: str, result: Dict[str, Any]) -> str:
        """Generate a user-friendly response about the GitHub operation"""
        try:
            # Create a prompt based on operation and result
            if "error" in result:
                prompt = f"The GitHub operation '{operation}' failed with error: {result['error']}. Please provide a helpful response to the user's query: '{query}'"
            else:
                prompt = f"The GitHub operation '{operation}' was successful with result: {str(result)}. Please provide a helpful response to the user's query: '{query}'"
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"I performed the GitHub operation, but encountered an error generating a detailed response: {str(e)}"