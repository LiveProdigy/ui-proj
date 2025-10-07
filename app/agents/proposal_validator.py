"""
Proposal Validator Agent - Analyzes PR descriptions or ideas for clarity & feasibility
"""

import os
from typing import Dict, Any, Optional, List
import openai
from app.agents.base import BaseAgent


class ProposalValidatorAgent(BaseAgent):
    """
    Proposal Validator Agent that analyzes PR descriptions or project ideas
    for clarity, feasibility, and potential issues
    """
    
    def __init__(self):
        """Initialize the Proposal Validator agent"""
        super().__init__()
        
        # System prompt for the agent
        self.system_prompt = """
        You are a Proposal Validator Agent specialized in analyzing project proposals, PR descriptions, 
        and technical ideas for clarity, feasibility, and potential issues.
        
        For each proposal, assess:
        1. Clarity - Is the proposal well-defined and easy to understand?
        2. Feasibility - Can it be implemented with reasonable resources?
        3. Technical soundness - Are there any architectural or technical issues?
        4. Risks and challenges - What obstacles might be encountered?
        5. Improvement suggestions - How can the proposal be enhanced?
        
        Provide constructive feedback and specific recommendations for improvement.
        Be thorough but fair in your assessment.
        """
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the Proposal Validator agent with the given query and context
        
        Args:
            query: User's query containing a proposal to validate
            context: Optional context with additional information
            
        Returns:
            Dictionary containing agent response and updated context
        """
        context = context or {}
        
        # Extract the proposal from the query or context
        proposal = self._extract_proposal(query, context)
        
        # Analyze the proposal
        analysis = self._analyze_proposal(proposal)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis)
        
        # Create a comprehensive response
        response = self._format_response(analysis, recommendations)
        
        # Update context with analysis results
        updated_context = context.copy()
        updated_context.update({
            "proposal_validation": {
                "proposal": proposal,
                "analysis": analysis,
                "recommendations": recommendations
            }
        })
        
        return {
            "response": response,
            "context": updated_context,
            "complete": True
        }
    
    def _extract_proposal(self, query: str, context: Dict[str, Any]) -> str:
        """Extract the proposal text from query or context"""
        # Check if we have a proposal in context from GitHub agent
        if context.get("github", {}).get("last_result", {}).get("pull_request"):
            pr = context["github"]["last_result"]["pull_request"]
            return f"Title: {pr.get('title', '')}\n\nDescription: {pr.get('body', '')}"
        
        # Otherwise extract from the query
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract the proposal or idea to be validated from this text."},
                    {"role": "user", "content": f"Extract the main proposal or idea from this query: '{query}'. Include only the proposal itself, not any instructions or questions around it."}
                ],
                temperature=0,
            )
            
            extracted_proposal = response.choices[0].message.content.strip()
            return extracted_proposal if extracted_proposal else query
        except Exception:
            # If extraction fails, use the original query
            return query
    
    def _analyze_proposal(self, proposal: str) -> Dict[str, Any]:
        """Analyze the proposal for clarity, feasibility, and potential issues"""
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """
                    Analyze the following proposal and provide a structured assessment with these categories:
                    - clarity_score: 1-10 rating
                    - clarity_issues: List specific clarity issues
                    - feasibility_score: 1-10 rating
                    - feasibility_issues: List specific feasibility concerns
                    - technical_score: 1-10 rating
                    - technical_issues: List potential technical challenges
                    - overall_assessment: Brief paragraph summarizing the analysis
                    """}, 
                    {"role": "user", "content": proposal}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            analysis = response.choices[0].message.content
            return analysis
        except Exception as e:
            # Return a basic analysis if the API call fails
            return {
                "clarity_score": 5,
                "clarity_issues": ["Unable to perform detailed analysis"],
                "feasibility_score": 5,
                "feasibility_issues": ["Unable to perform detailed analysis"],
                "technical_score": 5,
                "technical_issues": ["Unable to perform detailed analysis"],
                "overall_assessment": f"Unable to perform detailed analysis due to error: {str(e)}"
            }
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on the analysis"""
        try:
            # Convert analysis to string if it's not already
            analysis_str = str(analysis)
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Based on the analysis of a proposal, provide specific, actionable recommendations for improvement."},
                    {"role": "user", "content": f"Based on this analysis: {analysis_str}, provide 3-5 specific, actionable recommendations to improve the proposal."}
                ],
                temperature=0.7,
            )
            
            recommendations_text = response.choices[0].message.content
            
            # Split by newlines or bullet points to get list
            recommendations = [r.strip().strip('•-*').strip() for r in recommendations_text.split('\n') if r.strip()]
            
            # Filter out any empty strings
            return [r for r in recommendations if r]
        except Exception:
            # Return basic recommendations if API call fails
            return [
                "Clarify the proposal's main objectives",
                "Add more detail about implementation steps",
                "Consider technical feasibility more carefully"
            ]
    
    def _format_response(self, analysis: Dict[str, Any], recommendations: List[str]) -> str:
        """Format the analysis and recommendations into a user-friendly response"""
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Format this analysis: {analysis} and these recommendations: {recommendations} into a helpful, constructive response. Be specific but supportive."}
                ],
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # Create a basic formatted response if API call fails
            clarity_score = analysis.get("clarity_score", "N/A")
            feasibility_score = analysis.get("feasibility_score", "N/A")
            technical_score = analysis.get("technical_score", "N/A")
            
            response = f"# Proposal Assessment\n\n"
            response += f"## Overall Assessment\n{analysis.get('overall_assessment', 'Unable to provide detailed assessment.')}\n\n"
            response += f"## Scores\n- Clarity: {clarity_score}/10\n- Feasibility: {feasibility_score}/10\n- Technical Soundness: {technical_score}/10\n\n"
            response += "## Recommendations\n"
            
            for i, rec in enumerate(recommendations, 1):
                response += f"{i}. {rec}\n"
            
            return response