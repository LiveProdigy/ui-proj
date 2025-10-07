"""
Outreach Agent - Drafts personalized emails or issue replies
"""

import os
from typing import Dict, Any, Optional, List
import openai
from app.agents.base import BaseAgent


class OutreachAgent(BaseAgent):
    """
    Outreach Agent specialized in drafting personalized emails or issue replies
    based on repository data and potential contributors
    """
    
    def __init__(self):
        """Initialize the Outreach agent"""
        super().__init__()
        
        # Load any templates if available
        self.templates = self._load_templates()
        
        # System prompt for the agent
        self.system_prompt = """
        You are an Outreach Agent specialized in crafting personalized, effective communications 
        for open source projects and technical teams.
        
        Your communications should be:
        1. Personalized - Reference specific contributions or interests
        2. Clear - Have a specific purpose and request
        3. Professional - Maintain appropriate tone and formality
        4. Actionable - Include specific next steps or calls to action
        
        Adapt your tone and content to the context and recipient.
        """
    
    def _load_templates(self) -> Dict[str, str]:
        """Load email and response templates"""
        # In a real implementation, these could be loaded from files or a database
        return {
            "contributor_invitation": """
            Subject: Invitation to Collaborate on {project_name}
            
            Hi {name},
            
            I noticed your excellent work on {related_project}, particularly your contributions to {specific_area}.
            
            We're currently developing {project_name}, which involves similar technologies and challenges. 
            Given your expertise in {expertise}, I thought you might be interested in collaborating.
            
            Our current focus is on {current_focus}, and we believe your skills would be valuable in helping us address {specific_challenge}.
            
            Would you be interested in discussing potential collaboration? If so, please {call_to_action}.
            
            Best regards,
            {sender_name}
            """,
            
            "issue_response": """
            Hi {name},
            
            Thank you for raising this issue about {issue_topic}.
            
            {personalized_acknowledgment}
            
            {issue_assessment}
            
            {proposed_solution}
            
            {next_steps}
            
            Thanks again for your contribution to improving {project_name}!
            
            Best,
            {sender_name}
            """,
            
            "pr_review": """
            Hi {name},
            
            Thank you for your pull request on {pr_topic}.
            
            {positive_feedback}
            
            {improvement_suggestions}
            
            {specific_questions}
            
            {next_steps}
            
            Thanks for your contribution to {project_name}!
            
            Best,
            {sender_name}
            """
        }
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the Outreach agent with the given query and context
        
        Args:
            query: User's query related to creating outreach content
            context: Optional context with recipient information
            
        Returns:
            Dictionary containing agent response and updated context
        """
        context = context or {}
        
        # Extract outreach parameters
        outreach_params = self._extract_outreach_parameters(query, context)
        
        # Determine the outreach type (email, issue reply, PR comment, etc)
        outreach_type = self._determine_outreach_type(query, outreach_params)
        
        # Generate the outreach content
        outreach_content = self._generate_outreach_content(outreach_type, outreach_params)
        
        # Create a response for the user
        response = self._format_response(outreach_content, outreach_type, outreach_params)
        
        # Update context with outreach information
        updated_context = context.copy()
        updated_context.update({
            "outreach": {
                "type": outreach_type,
                "params": outreach_params,
                "content": outreach_content
            }
        })
        
        return {
            "response": response,
            "context": updated_context,
            "complete": True
        }
    
    def _extract_outreach_parameters(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract outreach parameters from query and context"""
        # Check if we have lead generation insights in context
        lead_context = {}
        if context.get("lead_generation"):
            lead_context = context["lead_generation"]
        
        # Also check if we have GitHub context
        github_context = {}
        if context.get("github"):
            github_context = context["github"]
        
        # Use OpenAI to extract parameters
        try:
            context_str = f"Lead Generation Context: {str(lead_context)[:500]}...\nGitHub Context: {str(github_context)[:500]}..."
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extract parameters for an outreach message (email, issue reply, etc) from the query and context."},
                    {"role": "user", "content": f"Query: {query}\n\nContext: {context_str}\n\nExtract the following parameters for creating an outreach message:\n- recipient_name\n- recipient_background (skills, contributions)\n- project_name\n- outreach_purpose\n- specific_details\n- sender_name"}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            params = response.choices[0].message.content
            
            # Ensure we have minimal defaults
            if not params.get("recipient_name"):
                params["recipient_name"] = "there"
            if not params.get("project_name"):
                params["project_name"] = "our project"
            if not params.get("sender_name"):
                params["sender_name"] = "The Project Team"
                
            return params
        except Exception:
            # Return basic parameters if extraction fails
            return {
                "recipient_name": "there",
                "recipient_background": "your background in technology",
                "project_name": "our project",
                "outreach_purpose": "discuss collaboration",
                "specific_details": "the details you mentioned",
                "sender_name": "The Project Team"
            }
    
    def _determine_outreach_type(self, query: str, params: Dict[str, Any]) -> str:
        """Determine the type of outreach content to generate"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Determine the type of outreach content needed."},
                    {"role": "user", "content": f"Based on this query: '{query}', what type of outreach content is needed? Options are: 'email', 'issue_reply', 'pr_comment', 'general_outreach'. Return just one option."}
                ],
                temperature=0,
            )
            
            outreach_type = response.choices[0].message.content.strip().lower()
            
            # Map to template types
            type_mapping = {
                "email": "contributor_invitation",
                "issue_reply": "issue_response",
                "pr_comment": "pr_review",
                "general_outreach": "contributor_invitation"
            }
            
            return type_mapping.get(outreach_type, "contributor_invitation")
        except Exception:
            # Default to contributor invitation
            return "contributor_invitation"
    
    def _generate_outreach_content(self, outreach_type: str, params: Dict[str, Any]) -> str:
        """Generate the outreach content using templates and OpenAI"""
        try:
            # Get the template
            template = self.templates.get(outreach_type, "")
            
            # Create a prompt for OpenAI
            prompt = f"""
            Generate a personalized {outreach_type.replace('_', ' ')} using this information:
            
            Recipient: {params.get('recipient_name')}
            Recipient Background: {params.get('recipient_background')}
            Project: {params.get('project_name')}
            Purpose: {params.get('outreach_purpose')}
            Specific Details: {params.get('specific_details')}
            Sender: {params.get('sender_name')}
            
            Template to follow:
            {template}
            
            The output should be personalized, professional, clear, and actionable.
            """
            
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
            # Generate basic content if API call fails
            template = self.templates.get(outreach_type, "")
            
            # Perform basic template variable replacement
            for key, value in params.items():
                template = template.replace(f"{{{key}}}", str(value))
            
            # Replace any remaining template variables
            import re
            template = re.sub(r'\{[^}]*\}', '[...]', template)
            
            return template
    
    def _format_response(self, outreach_content: str, outreach_type: str, params: Dict[str, Any]) -> str:
        """Format the outreach content into a user-friendly response"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Format outreach content for presentation to the user."},
                    {"role": "user", "content": f"Here is the {outreach_type.replace('_', ' ')} I generated for {params.get('recipient_name')} about {params.get('project_name')}:\n\n{outreach_content}\n\nProvide this to the user with a brief explanation of how they can use or customize it."}
                ],
                temperature=0.5,
            )
            
            return response.choices[0].message.content
        except Exception:
            # Create a basic formatted response
            return f"""
            # Generated {outreach_type.replace('_', ' ').title()}
            
            I've created the following outreach content for {params.get('recipient_name')}:
            
            ---
            
            {outreach_content}
            
            ---
            
            You can customize this message before sending it to better match your specific needs.
            """