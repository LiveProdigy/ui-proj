"""
Tests for the Agent Orchestrator
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json

from app.orchestrator.agent_orchestrator import AgentOrchestrator, AgentState


@pytest.fixture
def mock_github_agent():
    """Create a mock GitHub agent"""
    mock = MagicMock()
    mock.run.return_value = {
        "response": "GitHub agent response",
        "context": {"github_data": "test_data"},
        "complete": True
    }
    return mock


@pytest.fixture
def mock_proposal_validator():
    """Create a mock Proposal Validator agent"""
    mock = MagicMock()
    mock.run.return_value = {
        "response": "Proposal validator response",
        "context": {"validation_data": "test_data"},
        "complete": True
    }
    return mock


@pytest.fixture
def mock_context_store():
    """Create a mock context store"""
    mock = MagicMock()
    mock.get_context.return_value = {"test_key": "test_value"}
    return mock


@pytest.fixture
def orchestrator(mock_github_agent, mock_proposal_validator, mock_context_store):
    """Create an orchestrator with mock dependencies"""
    with patch("app.orchestrator.agent_orchestrator.GithubAgent", return_value=mock_github_agent), \
         patch("app.orchestrator.agent_orchestrator.ProposalValidatorAgent", return_value=mock_proposal_validator), \
         patch("app.orchestrator.agent_orchestrator.ContextStore", return_value=mock_context_store):
        
        orchestrator = AgentOrchestrator()
        
        # Replace the _parse_intent method with a mock that directly returns GitHub agent
        async def mock_parse_intent(state):
            return AgentState(
                user_input=state.user_input,
                context=state.context,
                history=state.history,
                current_agent="github"
            )
        
        orchestrator._parse_intent = mock_parse_intent
        yield orchestrator


@pytest.mark.asyncio
async def test_run_workflow_github_agent(orchestrator, mock_context_store):
    """Test running the workflow with GitHub agent"""
    # Run the workflow
    result = await orchestrator.run_workflow("Check my repository", "test_session")
    
    # Verify that context store was called to get initial context
    mock_context_store.get_context.assert_called_once_with("test_session")
    
    # Verify that context store was called to store updated context
    mock_context_store.store_context.assert_called_once()
    
    # Verify the result
    assert result["session_id"] == "test_session"
    assert result["agent_used"] == "github"
    assert result["output"] == "GitHub agent response"
    assert result["error"] is None