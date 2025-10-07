"""
Base Agent class that all specialized agents will inherit from
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self):
        """Initialize the agent"""
        self.name = self.__class__.__name__
    
    @abstractmethod
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the agent with the given query and context
        
        Args:
            query: User's input or query
            context: Optional context information
            
        Returns:
            Dictionary containing agent response and updated context
        """
        pass