"""
Main application entry point for Phase 2A: Modular ADK Architecture.

This module provides the main application that initializes and runs the
multi-agent system with proper error handling and monitoring.
"""

import asyncio
import signal
import sys
from typing import Optional
import structlog

from config.settings import get_settings
from config.logging_config import get_logger, get_system_logger, log_system_event
from coordinator import CoordinatorAgent


class MultiAgentSystem:
    """
    Main multi-agent system application.
    
    This class manages the lifecycle of the multi-agent system including
    initialization, running, graceful shutdown, and monitoring.
    """
    
    def __init__(self):
        """Initialize the multi-agent system."""
        self.logger = get_logger("main")
        self.settings = get_settings()
        
        # Initialize coordinator
        self.coordinator: Optional[CoordinatorAgent] = None
        
        # Shutdown flag
        self.shutdown_requested = False
        
        # Health check task
        self.health_check_task: Optional[asyncio.Task] = None
        
        self.logger.info("Multi-agent system initializing")
    
    async def initialize(self) -> None:
        """Initialize the multi-agent system."""
        try:
            self.logger.info("Starting system initialization")
            
            # Initialize coordinator agent
            self.coordinator = CoordinatorAgent()
            
            # Perform initial health check
            await self.coordinator.health_check()
            
            # Start health monitoring
            self.health_check_task = asyncio.create_task(self._health_monitoring_loop())
            
            self.logger.info("System initialization completed successfully")
            
        except Exception as e:
            self.logger.error("System initialization failed", error=str(e))
            raise
    
    async def run(self) -> None:
        """Run the multi-agent system."""
        try:
            self.logger.info("Starting multi-agent system")
            
            # Set up signal handlers for graceful shutdown
            self._setup_signal_handlers()
            
            # Main event loop
            while not self.shutdown_requested:
                try:
                    # Process any pending tasks
                    await asyncio.sleep(1)
                    
                except asyncio.CancelledError:
                    self.logger.info("Main loop cancelled")
                    break
                except Exception as e:
                    self.logger.error("Error in main loop", error=str(e))
                    await asyncio.sleep(5)  # Wait before retrying
            
            self.logger.info("Main loop exited")
            
        except Exception as e:
            self.logger.error("System runtime error", error=str(e))
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the system."""
        try:
            self.logger.info("Starting system shutdown")
            
            # Cancel health check task
            if self.health_check_task and not self.health_check_task.done():
                self.health_check_task.cancel()
                try:
                    await self.health_check_task
                except asyncio.CancelledError:
                    pass
            
            # Perform final health check
            if self.coordinator:
                await self.coordinator.health_check()
            
            self.logger.info("System shutdown completed")
            
        except Exception as e:
            self.logger.error("Error during shutdown", error=str(e))
    
    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating shutdown")
            self.shutdown_requested = True
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def _health_monitoring_loop(self) -> None:
        """Health monitoring loop."""
        while not self.shutdown_requested:
            try:
                if self.coordinator:
                    health_status = await self.coordinator.health_check()
                    
                    # Log health status
                    overall_status = health_status.get("overall_status", "unknown")
                    healthy_agents = sum(
                        1 for agent in health_status.get("agents", {}).values()
                        if agent.get("is_healthy", False)
                    )
                    total_agents = len(health_status.get("agents", {}))
                    
                    self.logger.info(
                        "Health check completed",
                        overall_status=overall_status,
                        healthy_agents=healthy_agents,
                        total_agents=total_agents
                    )
                    
                    # Alert if system is unhealthy
                    if overall_status == "unhealthy":
                        log_system_event(
                            self.logger,
                            "system_unhealthy",
                            "main",
                            "System health check failed",
                            level="error"
                        )
                
                # Wait for next health check
                await asyncio.sleep(self.settings.monitoring.health_check_interval)
                
            except asyncio.CancelledError:
                self.logger.info("Health monitoring loop cancelled")
                break
            except Exception as e:
                self.logger.error("Error in health monitoring loop", error=str(e))
                await asyncio.sleep(10)  # Wait before retrying
    
    def get_system_status(self) -> dict:
        """Get current system status."""
        if not self.coordinator:
            return {"status": "not_initialized"}
        
        return self.coordinator.get_system_status()


async def interactive_mode(system: MultiAgentSystem) -> None:
    """Run the system in interactive mode for testing."""
    print("\n🤖 Phase 2A: Modular ADK Architecture - Interactive Mode")
    print("=" * 60)
    print("Type 'quit' to exit, 'status' for system status, 'health' for health check")
    print("=" * 60)
    
    while True:
        try:
            # Get user input
            query = input("\n💬 Enter your query: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif query.lower() == 'status':
                status = system.get_system_status()
                print(f"\n📊 System Status:")
                print(f"   Coordinator: {'✅ Healthy' if status.get('coordinator', {}).get('is_healthy') else '❌ Unhealthy'}")
                print(f"   Total Requests: {status.get('coordinator', {}).get('request_count', 0)}")
                print(f"   Error Rate: {status.get('coordinator', {}).get('error_rate', 0):.2%}")
                print(f"   Collaboration Rate: {status.get('coordinator', {}).get('collaboration_rate', 0):.2%}")
                continue
            elif query.lower() == 'health':
                if system.coordinator:
                    health = await system.coordinator.health_check()
                    print(f"\n🏥 Health Check:")
                    print(f"   Overall Status: {health.get('overall_status', 'unknown')}")
                    for agent_name, agent_health in health.get('agents', {}).items():
                        status = "✅" if agent_health.get('is_healthy') else "❌"
                        print(f"   {agent_name}: {status}")
                continue
            
            # Process query
            if system.coordinator:
                print("\n🔄 Processing query...")
                response = await system.coordinator.process_query(query)
                print(f"\n📝 Response:\n{response}")
            else:
                print("❌ System not initialized")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


async def main() -> None:
    """Main application entry point."""
    # Initialize logging
    logger = get_system_logger()
    
    try:
        # Initialize system
        system = MultiAgentSystem()
        await system.initialize()
        
        # Check if running in interactive mode
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            await interactive_mode(system)
        else:
            # Run in server mode
            await system.run()
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error("Application failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    # Run the application
    asyncio.run(main())
