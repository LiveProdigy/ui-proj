"""
Agent Orchestrator module - Manages multiple AI agents, coordinates request flow, and tracks tool usage
"""

import uuid
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
import openai
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Import agents
from app.agents.github_agent import GithubAgent
from app.agents.proposal_validator import ProposalValidatorAgent
from app.agents.lead_generation import LeadGenerationAgent
from app.agents.outreach import OutreachAgent

# Import storage
from app.storage.context_store import ContextStore


class AgentState(BaseModel):
    """State of the agent workflow"""
    user_input: str
    context: Dict[str, Any]
    history: List[Dict[str, Any]]
    current_agent: Optional[str] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AgentOrchestrator:
    """Agent Orchestrator class to manage multiple AI agents and coordinate workflows"""
    
    def __init__(self):
        """Initialize the agent orchestrator with all available agents"""
        self.agents = {
            "github": GithubAgent(),
            "proposal_validator": ProposalValidatorAgent(),
            "lead_generation": LeadGenerationAgent(),
            "outreach": OutreachAgent(),
        }
        self.context_store = ContextStore()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for agent orchestration"""
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("parse_intent", self._parse_intent)
        workflow.add_node("github_agent", self._run_github_agent)
        workflow.add_node("proposal_validator", self._run_proposal_validator)
        workflow.add_node("lead_generation", self._run_lead_generation)
        workflow.add_node("outreach", self._run_outreach)
        
        # Define the edges - router pattern
        workflow.add_edge("parse_intent", "github_agent", self._should_route_to_github)
        workflow.add_edge("parse_intent", "proposal_validator", self._should_route_to_validator)
        workflow.add_edge("parse_intent", "lead_generation", self._should_route_to_lead_gen)
        workflow.add_edge("parse_intent", "outreach", self._should_route_to_outreach)
        
        # Add conditional returns to END
        workflow.add_conditional_edges(
            "github_agent",
            self._check_completion,
            {
                True: END,
                False: "parse_intent"  # Allow for chaining to other agents
            }
        )
        
        workflow.add_conditional_edges(
            "proposal_validator", 
            self._check_completion,
            {
                True: END,
                False: "parse_intent"
            }
        )
        
        workflow.add_conditional_edges(
            "lead_generation", 
            self._check_completion,
            {
                True: END,
                False: "parse_intent"
            }
        )
        
        workflow.add_conditional_edges(
            "outreach", 
            self._check_completion,
            {
                True: END,
                False: "parse_intent"
            }
        )
        
        # Set the entry point
        workflow.set_entry_point("parse_intent")
        
        return workflow.compile()
    
    def _parse_intent(self, state: AgentState) -> AgentState:
        """Parse the user's intent to determine which agent to use"""
        # Use OpenAI to classify the intent
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a classifier that determines which agent should handle a user request."},
                    {"role": "user", "content": f"User request: {state.user_input}\n\nClassify this as one of: github, proposal_validator, lead_generation, outreach"}
                ],
                temperature=0,
            )
            
            # Extract the agent name
            agent_name = response.choices[0].message.content.strip().lower()
            
            # If we can't determine a clear agent, default to None
            if agent_name not in self.agents:
                agent_name = None
                
            # Update state
            return AgentState(
                **state.dict(),
                current_agent=agent_name,
            )
        except Exception as e:
            return AgentState(
                **state.dict(),
                error=f"Error parsing intent: {str(e)}"
            )
    
    # Router conditions
    def _should_route_to_github(self, state: AgentState) -> bool:
        return state.current_agent == "github"
    
    def _should_route_to_validator(self, state: AgentState) -> bool:
        return state.current_agent == "proposal_validator"
    
    def _should_route_to_lead_gen(self, state: AgentState) -> bool:
        return state.current_agent == "lead_generation"
    
    def _should_route_to_outreach(self, state: AgentState) -> bool:
        return state.current_agent == "outreach"
    
    # Agent runners
    def _run_github_agent(self, state: AgentState) -> AgentState:
        """Run the GitHub agent"""
        try:
            agent_result = self.agents["github"].run(
                query=state.user_input,
                context=state.context
            )
            
            # Update context with the results
            updated_context = state.context.copy()
            updated_context.update(agent_result.get("context", {}))
            
            # Update history
            history = state.history.copy()
            history.append({
                "agent": "github",
                "input": state.user_input,
                "output": agent_result.get("response", "")
            })
            
            return AgentState(
                user_input=state.user_input,
                context=updated_context,
                history=history,
                output=agent_result,
                current_agent="github"
            )
        except Exception as e:
            return AgentState(
                **state.dict(),
                error=f"GitHub agent error: {str(e)}"
            )
    
    def _run_proposal_validator(self, state: AgentState) -> AgentState:
        """Run the Proposal Validator agent"""
        try:
            agent_result = self.agents["proposal_validator"].run(
                query=state.user_input,
                context=state.context
            )
            
            # Update context with the results
            updated_context = state.context.copy()
            updated_context.update(agent_result.get("context", {}))
            
            # Update history
            history = state.history.copy()
            history.append({
                "agent": "proposal_validator",
                "input": state.user_input,
                "output": agent_result.get("response", "")
            })
            
            return AgentState(
                user_input=state.user_input,
                context=updated_context,
                history=history,
                output=agent_result,
                current_agent="proposal_validator"
            )
        except Exception as e:
            return AgentState(
                **state.dict(),
                error=f"Proposal validator error: {str(e)}"
            )
    
    def _run_lead_generation(self, state: AgentState) -> AgentState:
        """Run the Lead Generation agent"""
        try:
            agent_result = self.agents["lead_generation"].run(
                query=state.user_input,
                context=state.context
            )
            
            # Update context with the results
            updated_context = state.context.copy()
            updated_context.update(agent_result.get("context", {}))
            
            # Update history
            history = state.history.copy()
            history.append({
                "agent": "lead_generation",
                "input": state.user_input,
                "output": agent_result.get("response", "")
            })
            
            return AgentState(
                user_input=state.user_input,
                context=updated_context,
                history=history,
                output=agent_result,
                current_agent="lead_generation"
            )
        except Exception as e:
            return AgentState(
                **state.dict(),
                error=f"Lead generation error: {str(e)}"
            )
    
    def _run_outreach(self, state: AgentState) -> AgentState:
        """Run the Outreach agent"""
        try:
            agent_result = self.agents["outreach"].run(
                query=state.user_input,
                context=state.context
            )
            
            # Update context with the results
            updated_context = state.context.copy()
            updated_context.update(agent_result.get("context", {}))
            
            # Update history
            history = state.history.copy()
            history.append({
                "agent": "outreach",
                "input": state.user_input,
                "output": agent_result.get("response", "")
            })
            
            return AgentState(
                user_input=state.user_input,
                context=updated_context,
                history=history,
                output=agent_result,
                current_agent="outreach"
            )
        except Exception as e:
            return AgentState(
                **state.dict(),
                error=f"Outreach agent error: {str(e)}"
            )
    
    def _check_completion(self, state: AgentState) -> bool:
        """Check if the workflow should end"""
        # If there's an error, end the workflow
        if state.error:
            return True
        
        # Check if the output indicates we're done
        if state.output and state.output.get("complete", False):
            return True
        
        # Otherwise, continue the workflow
        return False
    
    async def run_workflow(self, user_input: str, session_id: str = None) -> Dict[str, Any]:
        """Run the agent workflow"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create context for this session
        context = self.context_store.get_context(session_id) or {}
        
        # Initialize state
        initial_state = AgentState(
            user_input=user_input,
            context=context,
            history=[]
        )
        
        # Run the workflow
        try:
            final_state = self.workflow.invoke(initial_state)
            
            # Store updated context
            if final_state.context:
                self.context_store.store_context(session_id, final_state.context)
            
            # Return the result
            return {
                "session_id": session_id,
                "output": final_state.output.get("response", "") if final_state.output else None,
                "error": final_state.error,
                "agent_used": final_state.current_agent
            }
        except Exception as e:
            return {
                "session_id": session_id,
                "error": f"Workflow error: {str(e)}",
                "agent_used": None,
                "output": None
            }