"""
Base agent class for Phase 2A: Modular ADK Architecture.

This module provides the foundation for all agents in the multi-agent system,
including common functionality, error handling, and performance monitoring.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import structlog
from pybreaker import CircuitBreaker, CircuitBreakerError

from google.adk.agents import Agent as ADKAgent
from config.settings import get_settings, AgentConfig
from config.logging_config import get_logger, log_agent_request, CorrelationContext


class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass


class AgentTimeoutError(AgentError):
    """Exception raised when agent request times out."""
    pass


class AgentUnavailableError(AgentError):
    """Exception raised when agent is unavailable."""
    pass


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system.
    
    This class provides common functionality including:
    - ADK agent integration
    - Circuit breaker pattern
    - Performance monitoring
    - Error handling
    - Logging and metrics
    """
    
    def __init__(
        self,
        name: str,
        model: str = "gemini-2.0-flash-exp",
        description: str = "",
        config: Optional[AgentConfig] = None
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            model: ADK model to use
            description: Agent description
            config: Agent configuration
        """
        self.name = name
        self.model = model
        self.description = description
        self.config = config or self._get_default_config()
        
        # Initialize ADK agent (currently disabled to avoid 'gen' error)
        self.adk_agent = None  # self._create_adk_agent()
        
        # Initialize circuit breaker
        self.circuit_breaker = self._create_circuit_breaker()
        
        # Initialize logger
        self.logger = get_logger(f"agent.{name}")
        
        # Performance tracking
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        
        # Health status
        self.is_healthy = True
        self.last_health_check = datetime.utcnow()
        
        self.logger.info(
            "Agent initialized",
            agent_name=name,
            model=model,
            description=description
        )
    
    def _get_default_config(self) -> AgentConfig:
        """Get default configuration for this agent."""
        settings = get_settings()
        return settings.get_agent_config(self.name) or AgentConfig(
            name=self.name,
            model=self.model,
            description=self.description
        )
    
    def _create_adk_agent(self) -> None:
        """Create the underlying ADK agent."""
        # For now, we'll skip ADK agent creation to avoid the 'gen' error
        # This will be replaced with proper ADK integration later
        pass
    
    def _create_circuit_breaker(self) -> CircuitBreaker:
        """Create circuit breaker for fault tolerance."""
        settings = get_settings()
        config = settings.circuit_breaker
        
        return CircuitBreaker(
            fail_max=config.failure_threshold,
            reset_timeout=config.recovery_timeout,
            exclude=[Exception]
        )
    
    @abstractmethod
    def _get_agent_instruction(self) -> str:
        """
        Get the instruction prompt for this agent.
        
        Returns:
            Agent-specific instruction string
        """
        pass
    
    @abstractmethod
    def _process_query_internal(self, query: str) -> str:
        """
        Process a query using agent-specific logic.
        
        Args:
            query: User query
            
        Returns:
            Agent response
        """
        pass
    
    async def process_query(self, query: str, correlation_id: Optional[str] = None) -> str:
        """
        Process a query with full error handling and monitoring.
        
        Args:
            query: User query
            correlation_id: Request correlation ID for tracing
            
        Returns:
            Agent response
            
        Raises:
            AgentError: If processing fails
        """
        start_time = time.time()
        correlation_id = correlation_id or f"{self.name}_{int(start_time)}"
        
        with CorrelationContext(correlation_id):
            try:
                self.logger.info(
                    "Processing query",
                    query=query,
                    correlation_id=correlation_id
                )
                
                # Check circuit breaker
                if self.circuit_breaker.current_state == "open":
                    raise AgentUnavailableError(f"Agent {self.name} is temporarily unavailable")
                
                # Process query with circuit breaker
                response = await self.circuit_breaker.call_async(
                    self._process_query_with_timeout,
                    query
                )
                
                # Update metrics
                response_time = time.time() - start_time
                self._update_metrics(response_time, success=True)
                
                # Log success
                log_agent_request(
                    self.logger,
                    self.name,
                    query,
                    response_time,
                    success=True,
                    correlation_id=correlation_id
                )
                
                return response
                
            except CircuitBreakerError as e:
                self._update_metrics(time.time() - start_time, success=False)
                self.logger.error(
                    "Circuit breaker opened",
                    error=str(e),
                    correlation_id=correlation_id
                )
                raise AgentUnavailableError(f"Agent {self.name} is temporarily unavailable") from e
                
            except asyncio.TimeoutError:
                self._update_metrics(time.time() - start_time, success=False)
                self.logger.error(
                    "Query timeout",
                    correlation_id=correlation_id
                )
                raise AgentTimeoutError(f"Agent {self.name} request timed out")
                
            except Exception as e:
                self._update_metrics(time.time() - start_time, success=False)
                self.logger.error(
                    "Query processing failed",
                    error=str(e),
                    correlation_id=correlation_id
                )
                raise AgentError(f"Agent {self.name} processing failed: {str(e)}") from e
    
    async def _process_query_with_timeout(self, query: str) -> str:
        """Process query with timeout."""
        return await asyncio.wait_for(
            self._process_query_internal(query),
            timeout=self.config.timeout
        )
    
    def _update_metrics(self, response_time: float, success: bool) -> None:
        """Update agent performance metrics."""
        self.request_count += 1
        self.total_response_time += response_time
        
        if not success:
            self.error_count += 1
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get agent health status.
        
        Returns:
            Health status dictionary
        """
        error_rate = self.error_count / max(self.request_count, 1)
        avg_response_time = self.total_response_time / max(self.request_count, 1)
        
        return {
            "name": self.name,
            "is_healthy": self.is_healthy,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "circuit_breaker_state": self.circuit_breaker.current_state,
            "last_health_check": self.last_health_check.isoformat()
        }
    
    async def health_check(self) -> bool:
        """
        Perform health check for this agent.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple health check query
            test_query = "health check"
            await self.process_query(test_query, correlation_id="health_check")
            
            self.is_healthy = True
            self.last_health_check = datetime.utcnow()
            
            return True
            
        except Exception as e:
            self.is_healthy = False
            self.last_health_check = datetime.utcnow()
            
            self.logger.warning(
                "Health check failed",
                error=str(e)
            )
            
            return False
    
    def get_capabilities(self) -> List[str]:
        """
        Get agent capabilities.
        
        Returns:
            List of agent capabilities
        """
        return [self.description]
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}', model='{self.model}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"model='{self.model}', "
            f"description='{self.description}', "
            f"healthy={self.is_healthy}"
            f")"
        )
