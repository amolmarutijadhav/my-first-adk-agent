"""
Configuration settings for Phase 2A: Modular ADK Architecture.

This module contains all configuration settings for the multi-agent system,
including agent configurations, message bus settings, and system parameters.
"""

from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict
import os


class AgentConfig(BaseSettings):
    """Configuration for individual agents."""
    
    name: str = Field(..., description="Agent name")
    model: str = Field(default="gemini-2.0-flash-exp", description="ADK model to use")
    description: str = Field(..., description="Agent description and capabilities")
    max_concurrent_requests: int = Field(default=10, description="Maximum concurrent requests")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    
    model_config = SettingsConfigDict(env_prefix="AGENT_")


class MessageBusConfig(BaseSettings):
    """Configuration for the message bus system."""
    
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout: int = Field(default=30, description="Message bus timeout in seconds")
    max_queue_size: int = Field(default=1000, description="Maximum message queue size")
    enable_persistence: bool = Field(default=True, description="Enable Redis persistence")
    
    model_config = SettingsConfigDict(env_prefix="MESSAGE_BUS_")


class LoggingConfig(BaseSettings):
    """Configuration for logging system."""
    
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(default="json", description="Log format (json or text)")
    file_path: Optional[str] = Field(default=None, description="Log file path")
    enable_structured_logging: bool = Field(default=True, description="Enable structured logging")
    
    model_config = SettingsConfigDict(env_prefix="LOGGING_")


class MonitoringConfig(BaseSettings):
    """Configuration for monitoring and metrics."""
    
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=8000, description="Metrics server port")
    health_check_interval: int = Field(default=30, description="Health check interval in seconds")
    enable_tracing: bool = Field(default=True, description="Enable distributed tracing")
    
    model_config = SettingsConfigDict(env_prefix="MONITORING_")


class CircuitBreakerConfig(BaseSettings):
    """Configuration for circuit breaker pattern."""
    
    failure_threshold: int = Field(default=5, description="Failure threshold before opening circuit")
    recovery_timeout: int = Field(default=60, description="Recovery timeout in seconds")
    expected_exception: str = Field(default="Exception", description="Expected exception type")
    
    model_config = SettingsConfigDict(env_prefix="CIRCUIT_BREAKER_")


class Settings(BaseSettings):
    """Main application settings."""
    
    # Environment
    environment: str = Field(default="development", description="Application environment")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # Agent configurations
    agents: Dict[str, AgentConfig] = Field(
        default={
            "tech_agent": AgentConfig(
                name="tech_agent",
                model="gemini-2.0-flash-exp",
                description="Technical support and programming assistance"
            ),
            "creative_agent": AgentConfig(
                name="creative_agent",
                model="gemini-2.0-flash-exp", 
                description="Creative writing and brainstorming"
            ),
            "business_agent": AgentConfig(
                name="business_agent",
                model="gemini-2.0-flash-exp",
                description="Business strategy and analysis"
            ),
            "hello_agent": AgentConfig(
                name="hello_agent",
                model="gemini-2.0-flash-exp",
                description="General conversation and greetings"
            )
        },
        description="Agent configurations"
    )
    
    # System configurations
    message_bus: MessageBusConfig = Field(default_factory=MessageBusConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    circuit_breaker: CircuitBreakerConfig = Field(default_factory=CircuitBreakerConfig)
    
    # Performance settings
    max_concurrent_requests: int = Field(default=100, description="Maximum concurrent requests")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    
    # Security settings
    enable_rate_limiting: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests: int = Field(default=100, description="Requests per minute")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent."""
        return self.agents.get(agent_name)
    
    def get_all_agent_names(self) -> list[str]:
        """Get list of all configured agent names."""
        return list(self.agents.keys())
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global settings
    settings = Settings()
    return settings
