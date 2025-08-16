"""
Logging configuration for Phase 2A: Modular ADK Architecture.

This module provides structured logging configuration with correlation IDs,
performance tracking, and integration with monitoring systems.
"""

import logging
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import structlog
from structlog.stdlib import LoggerFactory
from structlog.processors import JSONRenderer, TimeStamper, add_log_level
from structlog.types import Processor

from .settings import get_settings


def setup_structured_logging() -> structlog.stdlib.BoundLogger:
    """
    Setup structured logging with correlation IDs and performance tracking.
    
    Returns:
        Configured structured logger instance
    """
    settings = get_settings()
    
    # Configure structlog processors
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add JSON renderer for structured logging
    if settings.logging.enable_structured_logging:
        processors.append(JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.logging.level.upper()),
    )
    
    return structlog.get_logger()


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance with the given name.
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)


class CorrelationContext:
    """Context manager for correlation IDs in logging."""
    
    def __init__(self, correlation_id: str):
        self.correlation_id = correlation_id
        self._previous_context = {}
    
    def __enter__(self):
        """Enter correlation context."""
        self._previous_context = structlog.contextvars.get_contextvars().copy()
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=self.correlation_id,
            timestamp=datetime.utcnow().isoformat()
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit correlation context."""
        structlog.contextvars.clear_contextvars()
        for key, value in self._previous_context.items():
            structlog.contextvars.bind_contextvars(**{key: value})


def log_agent_request(
    logger: structlog.stdlib.BoundLogger,
    agent_name: str,
    query: str,
    response_time: float,
    success: bool = True,
    error_message: Optional[str] = None,
    **kwargs: Any
) -> None:
    """
    Log agent request with performance metrics.
    
    Args:
        logger: Structured logger instance
        agent_name: Name of the agent
        query: User query
        response_time: Response time in seconds
        success: Whether the request was successful
        error_message: Error message if request failed
        **kwargs: Additional context data
    """
    log_data = {
        "event": "agent_request",
        "agent_name": agent_name,
        "query": query,
        "response_time": response_time,
        "success": success,
        **kwargs
    }
    
    if error_message:
        log_data["error_message"] = error_message
    
    if success:
        logger.info("Agent request completed", **log_data)
    else:
        logger.error("Agent request failed", **log_data)


def log_system_event(
    logger: structlog.stdlib.BoundLogger,
    event: str,
    component: str,
    message: str,
    level: str = "info",
    **kwargs: Any
) -> None:
    """
    Log system events with structured data.
    
    Args:
        logger: Structured logger instance
        event: Event type
        component: System component
        message: Event message
        level: Log level
        **kwargs: Additional context data
    """
    log_data = {
        "event": event,
        "component": component,
        "message": message,
        **kwargs
    }
    
    log_method = getattr(logger, level.lower())
    log_method("System event", **log_data)


def log_performance_metric(
    logger: structlog.stdlib.BoundLogger,
    metric_name: str,
    value: float,
    unit: str = "seconds",
    tags: Optional[Dict[str, str]] = None,
    **kwargs: Any
) -> None:
    """
    Log performance metrics for monitoring.
    
    Args:
        logger: Structured logger instance
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement
        tags: Metric tags
        **kwargs: Additional context data
    """
    log_data = {
        "event": "performance_metric",
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        **kwargs
    }
    
    if tags:
        log_data["tags"] = tags
    
    logger.info("Performance metric", **log_data)


def log_health_check(
    logger: structlog.stdlib.BoundLogger,
    component: str,
    status: str,
    details: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> None:
    """
    Log health check results.
    
    Args:
        logger: Structured logger instance
        component: Component being checked
        status: Health status (healthy, unhealthy, degraded)
        details: Health check details
        **kwargs: Additional context data
    """
    log_data = {
        "event": "health_check",
        "component": component,
        "status": status,
        **kwargs
    }
    
    if details:
        log_data["details"] = details
    
    if status == "healthy":
        logger.info("Health check passed", **log_data)
    elif status == "degraded":
        logger.warning("Health check degraded", **log_data)
    else:
        logger.error("Health check failed", **log_data)


# Global logger instance
logger = setup_structured_logging()


def get_system_logger() -> structlog.stdlib.BoundLogger:
    """Get the global system logger instance."""
    return logger
