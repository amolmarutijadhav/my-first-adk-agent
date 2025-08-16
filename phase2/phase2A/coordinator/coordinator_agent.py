"""
Coordinator Agent for Phase 2A: Modular ADK Architecture.

This module provides the main coordinator agent that manages the multi-agent system,
handles query routing, and orchestrates agent collaboration.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import structlog

from config.settings import get_settings
from config.logging_config import get_logger, log_agent_request, CorrelationContext
from .routing_logic import RoutingLogic, RoutingDecision, QueryType
from .agent_dispatcher import AgentDispatcher
from agents import TechAgent, CreativeAgent, BusinessAgent, HelloAgent


class CoordinatorError(Exception):
    """Base exception for coordinator-related errors."""
    pass


class CoordinatorAgent:
    """
    Main coordinator agent for the multi-agent system.
    
    This agent is responsible for:
    - Query analysis and routing
    - Agent management and health monitoring
    - Multi-agent collaboration
    - Performance monitoring and logging
    - System-wide error handling
    """
    
    def __init__(self):
        """Initialize the coordinator agent."""
        self.logger = get_logger("coordinator")
        self.settings = get_settings()
        
        # Initialize routing logic
        self.routing_logic = RoutingLogic()
        
        # Initialize agent dispatcher
        self.agent_dispatcher = AgentDispatcher()
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        # Performance tracking
        self.request_count = 0
        self.collaboration_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        
        # System health
        self.is_healthy = True
        self.last_health_check = datetime.utcnow()
        
        self.logger.info(
            "Coordinator agent initialized",
            agent_count=len(self.agents),
            available_agents=list(self.agents.keys())
        )
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all available agents."""
        agents = {}
        
        try:
            # Initialize specialized agents
            agents["tech_agent"] = TechAgent()
            agents["creative_agent"] = CreativeAgent()
            agents["business_agent"] = BusinessAgent()
            agents["hello_agent"] = HelloAgent()
            
            self.logger.info("All agents initialized successfully")
            
        except Exception as e:
            self.logger.error("Failed to initialize agents", error=str(e))
            raise CoordinatorError(f"Agent initialization failed: {str(e)}")
        
        return agents
    
    async def process_query(self, query: str, correlation_id: Optional[str] = None) -> str:
        """
        Process a user query through the multi-agent system.
        
        Args:
            query: User query to process
            correlation_id: Request correlation ID for tracing
            
        Returns:
            Coordinated response from appropriate agent(s)
            
        Raises:
            CoordinatorError: If processing fails
        """
        start_time = time.time()
        correlation_id = correlation_id or f"coord_{int(start_time)}"
        
        with CorrelationContext(correlation_id):
            try:
                self.logger.info(
                    "Processing query",
                    query=query,
                    correlation_id=correlation_id
                )
                
                # Analyze query and determine routing
                routing_decision = self.routing_logic.analyze_query(query)
                
                # Process based on query type
                if routing_decision.query_type == QueryType.COLLABORATION:
                    response = await self._handle_collaboration(query, routing_decision, correlation_id)
                else:
                    response = await self._handle_single_agent(query, routing_decision, correlation_id)
                
                # Update metrics
                response_time = time.time() - start_time
                self._update_metrics(response_time, success=True, collaboration=routing_decision.query_type == QueryType.COLLABORATION)
                
                # Log success
                log_agent_request(
                    self.logger,
                    "coordinator",
                    query,
                    response_time,
                    success=True,
                    correlation_id=correlation_id,
                    routing_decision=routing_decision.reasoning
                )
                
                return response
                
            except Exception as e:
                response_time = time.time() - start_time
                self._update_metrics(response_time, success=False)
                
                self.logger.error(
                    "Query processing failed",
                    error=str(e),
                    correlation_id=correlation_id
                )
                
                raise CoordinatorError(f"Query processing failed: {str(e)}") from e
    
    async def _handle_single_agent(self, query: str, routing_decision: RoutingDecision, correlation_id: str) -> str:
        """Handle query with a single agent."""
        agent_name = routing_decision.primary_agent
        agent = self.agents.get(agent_name)
        
        if not agent:
            raise CoordinatorError(f"Agent '{agent_name}' not found")
        
        self.logger.info(
            "Routing to single agent",
            agent=agent_name,
            confidence=routing_decision.confidence,
            correlation_id=correlation_id
        )
        
        return await agent.process_query(query, correlation_id)
    
    async def _handle_collaboration(self, query: str, routing_decision: RoutingDecision, correlation_id: str) -> str:
        """Handle query with multiple agents collaborating."""
        self.logger.info(
            "Initiating multi-agent collaboration",
            primary_agent=routing_decision.primary_agent,
            secondary_agents=routing_decision.secondary_agents,
            correlation_id=correlation_id
        )
        
        # Get all participating agents
        participating_agents = [routing_decision.primary_agent] + routing_decision.secondary_agents
        agent_responses = {}
        
        # Process query with all participating agents concurrently
        tasks = []
        for agent_name in participating_agents:
            agent = self.agents.get(agent_name)
            if agent:
                task = asyncio.create_task(
                    agent.process_query(query, f"{correlation_id}_{agent_name}")
                )
                tasks.append((agent_name, task))
        
        # Wait for all responses
        for agent_name, task in tasks:
            try:
                response = await task
                agent_responses[agent_name] = response
            except Exception as e:
                self.logger.warning(
                    f"Agent {agent_name} failed during collaboration",
                    error=str(e),
                    correlation_id=correlation_id
                )
                agent_responses[agent_name] = f"Agent {agent_name} unavailable: {str(e)}"
        
        # Combine responses
        combined_response = self._combine_agent_responses(agent_responses, query)
        
        return combined_response
    
    def _combine_agent_responses(self, agent_responses: Dict[str, str], original_query: str) -> str:
        """Combine responses from multiple agents."""
        if not agent_responses:
            return "🤝 Multi-Agent Collaboration: No agents were able to respond to your query."
        
        # Start with collaboration header
        combined = "🤝 Multi-Agent Collaboration:\n\n"
        combined += f"**Original Query:** {original_query}\n\n"
        combined += "**Combined Expertise:**\n\n"
        
        # Add each agent's response
        for agent_name, response in agent_responses.items():
            # Remove agent identifier from response if present
            clean_response = response
            for prefix in ["💻 Tech Agent:", "🎨 Creative Agent:", "💼 Business Agent:", "👋 Hello Agent:"]:
                if clean_response.startswith(prefix):
                    clean_response = clean_response[len(prefix):].strip()
                    break
            
            combined += f"**{agent_name.replace('_', ' ').title()}:**\n{clean_response}\n\n"
        
        # Add summary
        combined += "**Summary:** This collaborative response combines expertise from multiple specialized agents to provide comprehensive coverage of your query."
        
        return combined
    
    def _update_metrics(self, response_time: float, success: bool, collaboration: bool = False) -> None:
        """Update coordinator performance metrics."""
        self.request_count += 1
        self.total_response_time += response_time
        
        if collaboration:
            self.collaboration_count += 1
        
        if not success:
            self.error_count += 1
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of the system.
        
        Returns:
            Health status of all components
        """
        self.logger.info("Performing system health check")
        
        health_status = {
            "coordinator": {
                "is_healthy": self.is_healthy,
                "request_count": self.request_count,
                "error_count": self.error_count,
                "collaboration_count": self.collaboration_count,
                "avg_response_time": self.total_response_time / max(self.request_count, 1)
            },
            "agents": {},
            "overall_status": "healthy"
        }
        
        # Check each agent's health
        agent_health_tasks = []
        for agent_name, agent in self.agents.items():
            task = asyncio.create_task(agent.health_check())
            agent_health_tasks.append((agent_name, task))
        
        # Wait for all health checks
        for agent_name, task in agent_health_tasks:
            try:
                is_healthy = await task
                health_status["agents"][agent_name] = {
                    "is_healthy": is_healthy,
                    "health_details": await agent.get_health_status()
                }
                
                if not is_healthy:
                    health_status["overall_status"] = "degraded"
                    
            except Exception as e:
                self.logger.error(f"Health check failed for {agent_name}", error=str(e))
                health_status["agents"][agent_name] = {
                    "is_healthy": False,
                    "error": str(e)
                }
                health_status["overall_status"] = "unhealthy"
        
        # Update coordinator health
        self.is_healthy = health_status["overall_status"] in ["healthy", "degraded"]
        self.last_health_check = datetime.utcnow()
        
        self.logger.info(
            "Health check completed",
            overall_status=health_status["overall_status"],
            healthy_agents=sum(1 for agent in health_status["agents"].values() if agent["is_healthy"]),
            total_agents=len(health_status["agents"])
        )
        
        return health_status
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and statistics."""
        return {
            "coordinator": {
                "is_healthy": self.is_healthy,
                "request_count": self.request_count,
                "error_count": self.error_count,
                "collaboration_count": self.collaboration_count,
                "avg_response_time": self.total_response_time / max(self.request_count, 1),
                "error_rate": self.error_count / max(self.request_count, 1),
                "collaboration_rate": self.collaboration_count / max(self.request_count, 1)
            },
            "agents": {
                agent_name: agent.get_health_status()
                for agent_name, agent in self.agents.items()
            },
            "routing_logic": {
                "agent_capabilities": self.routing_logic.get_agent_capabilities()
            },
            "last_health_check": self.last_health_check.isoformat()
        }
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all available agents."""
        return self.routing_logic.get_agent_capabilities()
    
    async def register_custom_agent(self, agent_name: str, agent_instance: Any) -> None:
        """
        Register a custom agent with the coordinator.
        
        Args:
            agent_name: Name of the custom agent
            agent_instance: Custom agent instance
        """
        if agent_name in self.agents:
            self.logger.warning(f"Agent '{agent_name}' already exists, overwriting")
        
        self.agents[agent_name] = agent_instance
        self.logger.info(f"Custom agent '{agent_name}' registered successfully")
    
    def __str__(self) -> str:
        """String representation of the coordinator."""
        return f"CoordinatorAgent(agents={len(self.agents)}, healthy={self.is_healthy})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the coordinator."""
        return (
            f"CoordinatorAgent("
            f"agents={list(self.agents.keys())}, "
            f"healthy={self.is_healthy}, "
            f"requests={self.request_count}, "
            f"errors={self.error_count}"
            f")"
        )
