"""
Lead Generation Agent - Scans repo or issues for potential contributors or insights
"""

import os
from typing import Dict, Any, Optional, List
import openai
from app.agents.base import BaseAgent
from app.mcp.github_client import GitHubMCPClient


class LeadGenerationAgent(BaseAgent):
    """
    Lead Generation Agent that scans repositories or issues
    for potential contributors or insights
    """
    
    def __init__(self):
        """Initialize the Lead Generation agent with MCP client"""
        super().__init__()
        # Initialize the GitHub MCP client
        self.github_client = GitHubMCPClient()
        
        # System prompt for the agent
        self.system_prompt = """
        You are a Lead Generation Agent specialized in analyzing GitHub repositories, issues, 
        and pull requests to identify potential contributors and valuable insights.
        
        Your main tasks include:
        1. Identifying active contributors who might be interested in similar projects
        2. Finding patterns in issues and PRs that reveal project needs or opportunities
        3. Suggesting potential collaboration opportunities based on repo activity
        4. Highlighting topics and trends in the repository that might be valuable
        
        Provide specific, actionable insights rather than general observations.
        """
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the Lead Generation agent with the given query and context
        
        Args:
            query: User's query related to finding contributors or insights
            context: Optional context with repository information
            
        Returns:
            Dictionary containing agent response and updated context
        """
        context = context or {}
        
        # Extract repository information from context or query
        repo_info = self._extract_repo_info(query, context)
        
        # Determine the lead generation objective
        objective = self._determine_objective(query)
        
        # Collect data based on the objective
        data = self._collect_data(repo_info, objective)
        
        # Analyze the collected data
        analysis = self._analyze_data(data, objective)
        
        # Generate actionable insights
        insights = self._generate_insights(analysis, objective)
        
        # Format the response
        response = self._format_response(insights, objective)
        
        # Update context with lead generation results
        updated_context = context.copy()
        updated_context.update({
            "lead_generation": {
                "repo_info": repo_info,
                "objective": objective,
                "insights": insights
            }
        })
        
        return {
            "response": response,
            "context": updated_context,
            "complete": True
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
    
    def _determine_objective(self, query: str) -> str:
        """Determine the lead generation objective"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Classify lead generation objectives based on user query."},
                    {"role": "user", "content": f"Classify this query into one of these lead generation objectives: 'find_contributors', 'identify_trends', 'collaboration_opportunities', 'project_needs'. Query: '{query}'"}
                ],
                temperature=0,
            )
            
            return response.choices[0].message.content.strip().lower()
        except Exception:
            # Default to find_contributors if classification fails
            return "find_contributors"
    
    def _collect_data(self, repo_info: Dict[str, Any], objective: str) -> Dict[str, Any]:
        """Collect data based on the objective"""
        try:
            if not repo_info.get("owner") or not repo_info.get("repo_name"):
                return {"error": "Repository information is incomplete"}
            
            data = {"repo_info": repo_info, "objective": objective}
            
            # Collect different data based on objective
            if objective == "find_contributors":
                # Get contributors and their activity
                contributors = self.github_client.get_contributors(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"]
                )
                
                # Get recent issues and PRs
                issues = self.github_client.list_issues(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    state="all",
                    limit=50
                )
                
                data.update({
                    "contributors": contributors,
                    "issues": issues
                })
                
            elif objective == "identify_trends":
                # Get issues with labels and comments
                issues = self.github_client.list_issues(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    state="all",
                    limit=100
                )
                
                # Get commit history
                commits = self.github_client.get_commit_history(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    limit=100
                )
                
                data.update({
                    "issues": issues,
                    "commits": commits
                })
                
            elif objective == "collaboration_opportunities":
                # Get repository topics and languages
                repo_data = self.github_client.get_repository_data(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"]
                )
                
                # Get active contributors
                contributors = self.github_client.get_contributors(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"]
                )
                
                data.update({
                    "repo_data": repo_data,
                    "contributors": contributors
                })
                
            elif objective == "project_needs":
                # Get open issues with labels
                open_issues = self.github_client.list_issues(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    state="open"
                )
                
                # Get recent PRs
                recent_prs = self.github_client.list_pull_requests(
                    owner=repo_info["owner"],
                    repo=repo_info["repo_name"],
                    state="all",
                    limit=30
                )
                
                data.update({
                    "open_issues": open_issues,
                    "recent_prs": recent_prs
                })
            
            return data
        except Exception as e:
            return {"error": f"Error collecting data: {str(e)}"}
    
    def _analyze_data(self, data: Dict[str, Any], objective: str) -> Dict[str, Any]:
        """Analyze the collected data"""
        if "error" in data:
            return {"error": data["error"]}
        
        try:
            # Format data for analysis
            data_str = str(data)[:8000]  # Truncate to avoid token limits
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Analyze GitHub repository data for the objective: {objective}. Provide structured analysis."},
                    {"role": "user", "content": f"Analyze this GitHub repository data:\n\n{data_str}\n\nProvide analysis focused on {objective} with specific findings."}
                ],
                temperature=0.3,
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse the analysis into a structured format
            try:
                structured_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Convert the analysis into a structured JSON format."},
                        {"role": "user", "content": f"Convert this analysis into a JSON structure with 'key_findings', 'details', and 'metrics' fields:\n\n{analysis_text}"}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )
                
                return structured_response.choices[0].message.content
            except Exception:
                # If structured parsing fails, return text analysis
                return {"analysis_text": analysis_text}
        except Exception as e:
            return {"error": f"Error analyzing data: {str(e)}"}
    
    def _generate_insights(self, analysis: Dict[str, Any], objective: str) -> List[Dict[str, str]]:
        """Generate actionable insights from the analysis"""
        if "error" in analysis:
            return [{"title": "Error", "description": analysis["error"]}]
        
        try:
            # Format analysis for insight generation
            analysis_str = str(analysis)
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Based on the analysis of GitHub repository data, generate specific, actionable insights."},
                    {"role": "user", "content": f"Based on this analysis: {analysis_str}, generate 3-5 specific, actionable insights for {objective}. For each insight, provide a title and description."}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            insights = response.choices[0].message.content
            
            # Return insights as a list of dicts
            if isinstance(insights, list):
                return insights
            elif isinstance(insights, dict) and "insights" in insights:
                return insights["insights"]
            else:
                # Create a basic structure if the format is unexpected
                return [
                    {"title": "Generated Insight", "description": str(insights)}
                ]
        except Exception as e:
            return [{"title": "Error", "description": f"Error generating insights: {str(e)}"}]
    
    def _format_response(self, insights: List[Dict[str, str]], objective: str) -> str:
        """Format the insights into a user-friendly response"""
        try:
            insights_str = str(insights)
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Format these insights about {objective} into a helpful, action-oriented response:\n\n{insights_str}"}
                ],
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # Create a basic formatted response if API call fails
            response = f"# Lead Generation Insights: {objective.replace('_', ' ').title()}\n\n"
            
            for insight in insights:
                title = insight.get("title", "Insight")
                description = insight.get("description", "No description provided")
                response += f"## {title}\n{description}\n\n"
            
            return response