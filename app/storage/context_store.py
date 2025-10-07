"""
Context Store - In-memory or Redis-based store for session context
"""

import os
import json
import time
from typing import Dict, Any, Optional, Union
import redis


class ContextStore:
    """
    Context Store for maintaining session state and agent context
    Can use either in-memory storage or Redis
    """
    
    def __init__(self):
        """Initialize the context store"""
        self.use_redis = os.getenv("USE_REDIS", "false").lower() == "true"
        self.context_ttl = int(os.getenv("CONTEXT_TTL_SECONDS", 3600))  # 1 hour default
        
        # Initialize storage
        if self.use_redis:
            self._init_redis()
        else:
            self._init_memory_store()
    
    def _init_redis(self):
        """Initialize Redis connection"""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = redis.from_url(redis_url)
    
    def _init_memory_store(self):
        """Initialize in-memory storage"""
        self.memory_store = {}
        self.memory_timestamps = {}  # For TTL handling
    
    def store_context(self, session_id: str, context: Dict[str, Any]) -> bool:
        """
        Store context for a session
        
        Args:
            session_id: Unique identifier for the session
            context: Context data to store
            
        Returns:
            Success status
        """
        try:
            if self.use_redis:
                self.redis_client.setex(
                    f"context:{session_id}",
                    self.context_ttl,
                    json.dumps(context)
                )
            else:
                self.memory_store[session_id] = context
                self.memory_timestamps[session_id] = time.time()
                
                # Clean old sessions occasionally
                if len(self.memory_store) % 10 == 0:
                    self._clean_expired_sessions()
            
            return True
        except Exception as e:
            print(f"Error storing context: {str(e)}")
            return False
    
    def get_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get context for a session
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            Context data or None if not found
        """
        try:
            if self.use_redis:
                data = self.redis_client.get(f"context:{session_id}")
                if data:
                    # Refresh TTL
                    self.redis_client.expire(f"context:{session_id}", self.context_ttl)
                    return json.loads(data)
                return None
            else:
                # Check if session exists and hasn't expired
                if session_id in self.memory_store:
                    timestamp = self.memory_timestamps[session_id]
                    if time.time() - timestamp <= self.context_ttl:
                        # Refresh timestamp
                        self.memory_timestamps[session_id] = time.time()
                        return self.memory_store[session_id]
                    else:
                        # Session expired
                        del self.memory_store[session_id]
                        del self.memory_timestamps[session_id]
                
                return None
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return None
    
    def update_context(self, session_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update parts of a session's context
        
        Args:
            session_id: Unique identifier for the session
            update_data: Context data to update
            
        Returns:
            Success status
        """
        try:
            # Get existing context
            existing_context = self.get_context(session_id) or {}
            
            # Update with new data
            existing_context.update(update_data)
            
            # Store updated context
            return self.store_context(session_id, existing_context)
        except Exception as e:
            print(f"Error updating context: {str(e)}")
            return False
    
    def delete_context(self, session_id: str) -> bool:
        """
        Delete a session's context
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            Success status
        """
        try:
            if self.use_redis:
                self.redis_client.delete(f"context:{session_id}")
            else:
                if session_id in self.memory_store:
                    del self.memory_store[session_id]
                if session_id in self.memory_timestamps:
                    del self.memory_timestamps[session_id]
            
            return True
        except Exception as e:
            print(f"Error deleting context: {str(e)}")
            return False
    
    def _clean_expired_sessions(self) -> None:
        """Clean up expired sessions from memory store"""
        if not self.use_redis:
            current_time = time.time()
            expired_sessions = []
            
            for session_id, timestamp in self.memory_timestamps.items():
                if current_time - timestamp > self.context_ttl:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                if session_id in self.memory_store:
                    del self.memory_store[session_id]
                if session_id in self.memory_timestamps:
                    del self.memory_timestamps[session_id]