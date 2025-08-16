"""
Agent Dispatcher for Phase 2A: Modular ADK Architecture.

This module provides the agent dispatcher for managing agent communication,
load balancing, and failover mechanisms.
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import structlog

from config.settings import get_settings
from config.logging_config import get_logger


class AgentStatus:
    """Represents the status of an agent."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.is_available = True
        self.last_health_check = datetime.utcnow()
        self.consecutive_failures = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.avg_response_time = 0.0
        self.last_response_time = 0.0
    
    def update_health(self, is_healthy: bool, response_time: float = 0.0) -> None:
        """Update agent health status."""
        self.last_health_check = datetime.utcnow()
        self.last_response_time = response_time
        
        if is_healthy:
            self.is_available = True
            self.consecutive_failures = 0
        else:
            self.consecutive_failures += 1
            if self.consecutive_failures >= 3:  # Mark as unavailable after 3 failures
                self.is_available = False
    
    def update_request_stats(self, success: bool, response_time: float) -> None:
        """Update request statistics."""
        self.total_requests += 1
        self.last_response_time = response_time
        
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        # Update average response time
        if self.total_requests == 1:
            self.avg_response_time = response_time
        else:
            self.avg_response_time = (
                (self.avg_response_time * (self.total_requests - 1) + response_time) / 
                self.total_requests
            )
    
    def get_success_rate(self) -> float:
        """Get success rate of the agent."""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "agent_name": self.agent_name,
            "is_available": self.is_available,
            "last_health_check": self.last_health_check.isoformat(),
            "consecutive_failures": self.consecutive_failures,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.get_success_rate(),
            "avg_response_time": self.avg_response_time,
            "last_response_time": self.last_response_time
        }


class AgentDispatcher:
    """
    Agent dispatcher for managing agent communication and load balancing.
    
    This class provides:
    - Agent health monitoring
    - Load balancing across available agents
    - Failover mechanisms
    - Performance tracking
    - Agent discovery and registration
    """
    
    def __init__(self):
        """Initialize the agent dispatcher."""
        self.logger = get_logger("agent_dispatcher")
        self.settings = get_settings()
        
        # Agent registry and status tracking
        self.agents: Dict[str, Any] = {}
        self.agent_status: Dict[str, AgentStatus] = {}
        
        # Load balancing configuration
        self.load_balancing_strategy = "round_robin"  # round_robin, least_connections, fastest_response
        self.current_agent_index = 0
        
        # Health check configuration
        self.health_check_interval = 30  # seconds
        self.health_check_task: Optional[asyncio.Task] = None
        
        self.logger.info("Agent dispatcher initialized")
    
    def register_agent(self, agent_name: str, agent_instance: Any) -> None:
        """
        Register an agent with the dispatcher.
        
        Args:
            agent_name: Name of the agent
            agent_instance: Agent instance
        """
        self.agents[agent_name] = agent_instance
        self.agent_status[agent_name] = AgentStatus(agent_name)
        
        self.logger.info(f"Agent '{agent_name}' registered with dispatcher")
    
    def unregister_agent(self, agent_name: str) -> None:
        """
        Unregister an agent from the dispatcher.
        
        Args:
            agent_name: Name of the agent to unregister
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            del self.agent_status[agent_name]
            self.logger.info(f"Agent '{agent_name}' unregistered from dispatcher")
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents."""
        return [
            agent_name for agent_name, status in self.agent_status.items()
            if status.is_available
        ]
    
    def select_agent(self, agent_names: List[str]) -> Optional[str]:
        """
        Select the best agent based on load balancing strategy.
        
        Args:
            agent_names: List of candidate agent names
            
        Returns:
            Selected agent name or None if no agents available
        """
        available_agents = [
            name for name in agent_names
            if name in self.agent_status and self.agent_status[name].is_available
        ]
        
        if not available_agents:
            return None
        
        if len(available_agents) == 1:
            return available_agents[0]
        
        if self.load_balancing_strategy == "round_robin":
            return self._round_robin_select(available_agents)
        elif self.load_balancing_strategy == "least_connections":
            return self._least_connections_select(available_agents)
        elif self.load_balancing_strategy == "fastest_response":
            return self._fastest_response_select(available_agents)
        else:
            return available_agents[0]  # Default to first available
    
    def _round_robin_select(self, available_agents: List[str]) -> str:
        """Select agent using round-robin strategy."""
        selected = available_agents[self.current_agent_index % len(available_agents)]
        self.current_agent_index += 1
        return selected
    
    def _least_connections_select(self, available_agents: List[str]) -> str:
        """Select agent with least connections (requests)."""
        return min(
            available_agents,
            key=lambda name: self.agent_status[name].total_requests
        )
    
    def _fastest_response_select(self, available_agents: List[str]) -> str:
        """Select agent with fastest average response time."""
        return min(
            available_agents,
            key=lambda name: self.agent_status[name].avg_response_time
        )
    
    async def dispatch_request(
        self,
        agent_name: str,
        query: str,
        correlation_id: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Dispatch a request to a specific agent.
        
        Args:
            agent_name: Name of the agent to dispatch to
            query: Query to process
            correlation_id: Request correlation ID
            
        Returns:
            Tuple of (response, response_time)
            
        Raises:
            Exception: If agent is unavailable or request fails
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found")
        
        agent_status = self.agent_status[agent_name]
        if not agent_status.is_available:
            raise Exception(f"Agent '{agent_name}' is not available")
        
        start_time = datetime.utcnow()
        
        try:
            # Dispatch request to agent
            agent = self.agents[agent_name]
            response = await agent.process_query(query, correlation_id)
            
            # Calculate response time
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Update agent status
            agent_status.update_request_stats(True, response_time)
            agent_status.update_health(True, response_time)
            
            self.logger.info(
                f"Request dispatched successfully to {agent_name}",
                response_time=response_time,
                correlation_id=correlation_id
            )
            
            return response, response_time
            
        except Exception as e:
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Update agent status
            agent_status.update_request_stats(False, response_time)
            agent_status.update_health(False, response_time)
            
            self.logger.error(
                f"Request failed for agent {agent_name}",
                error=str(e),
                response_time=response_time,
                correlation_id=correlation_id
            )
            
            raise
    
    async def dispatch_with_failover(
        self,
        primary_agent: str,
        backup_agents: List[str],
        query: str,
        correlation_id: Optional[str] = None
    ) -> Tuple[str, float, str]:
        """
        Dispatch request with failover to backup agents.
        
        Args:
            primary_agent: Primary agent to try first
            backup_agents: List of backup agents to try if primary fails
            query: Query to process
            correlation_id: Request correlation ID
            
        Returns:
            Tuple of (response, response_time, agent_used)
        """
        all_agents = [primary_agent] + backup_agents
        
        for agent_name in all_agents:
            if agent_name not in self.agents:
                self.logger.warning(f"Agent '{agent_name}' not found, skipping")
                continue
            
            if not self.agent_status[agent_name].is_available:
                self.logger.warning(f"Agent '{agent_name}' not available, trying next")
                continue
            
            try:
                response, response_time = await self.dispatch_request(
                    agent_name, query, correlation_id
                )
                return response, response_time, agent_name
                
            except Exception as e:
                self.logger.warning(
                    f"Agent '{agent_name}' failed, trying next agent",
                    error=str(e),
                    correlation_id=correlation_id
                )
                continue
        
        # All agents failed
        raise Exception(f"All agents failed: {', '.join(all_agents)}")
    
    async def health_check_all_agents(self) -> Dict[str, bool]:
        """
        Perform health check on all registered agents.
        
        Returns:
            Dictionary mapping agent names to health status
        """
        self.logger.info("Performing health check on all agents")
        
        health_results = {}
        health_tasks = []
        
        for agent_name, agent in self.agents.items():
            task = asyncio.create_task(self._health_check_agent(agent_name, agent))
            health_tasks.append((agent_name, task))
        
        # Wait for all health checks to complete
        for agent_name, task in health_tasks:
            try:
                is_healthy = await task
                health_results[agent_name] = is_healthy
            except Exception as e:
                self.logger.error(f"Health check failed for {agent_name}", error=str(e))
                health_results[agent_name] = False
        
        self.logger.info(
            "Health check completed",
            healthy_agents=sum(health_results.values()),
            total_agents=len(health_results)
        )
        
        return health_results
    
    async def _health_check_agent(self, agent_name: str, agent: Any) -> bool:
        """Perform health check on a single agent."""
        try:
            is_healthy = await agent.health_check()
            self.agent_status[agent_name].update_health(is_healthy)
            return is_healthy
        except Exception as e:
            self.logger.error(f"Health check failed for {agent_name}", error=str(e))
            self.agent_status[agent_name].update_health(False)
            return False
    
    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent."""
        if agent_name in self.agent_status:
            return self.agent_status[agent_name].to_dict()
        return None
    
    def get_all_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents."""
        return {
            agent_name: status.to_dict()
            for agent_name, status in self.agent_status.items()
        }
    
    def set_load_balancing_strategy(self, strategy: str) -> None:
        """
        Set the load balancing strategy.
        
        Args:
            strategy: Load balancing strategy (round_robin, least_connections, fastest_response)
        """
        if strategy not in ["round_robin", "least_connections", "fastest_response"]:
            raise ValueError(f"Invalid load balancing strategy: {strategy}")
        
        self.load_balancing_strategy = strategy
        self.logger.info(f"Load balancing strategy set to: {strategy}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide statistics."""
        total_agents = len(self.agents)
        available_agents = len(self.get_available_agents())
        
        total_requests = sum(status.total_requests for status in self.agent_status.values())
        total_successful = sum(status.successful_requests for status in self.agent_status.values())
        
        overall_success_rate = total_successful / total_requests if total_requests > 0 else 1.0
        
        return {
            "total_agents": total_agents,
            "available_agents": available_agents,
            "unavailable_agents": total_agents - available_agents,
            "total_requests": total_requests,
            "total_successful_requests": total_successful,
            "overall_success_rate": overall_success_rate,
            "load_balancing_strategy": self.load_balancing_strategy,
            "agent_status": self.get_all_agent_status()
        }
    
    def __str__(self) -> str:
        """String representation of the dispatcher."""
        available = len(self.get_available_agents())
        total = len(self.agents)
        return f"AgentDispatcher(agents={total}, available={available})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the dispatcher."""
        return (
            f"AgentDispatcher("
            f"agents={list(self.agents.keys())}, "
            f"available={self.get_available_agents()}, "
            f"strategy={self.load_balancing_strategy}"
            f")"
        )
