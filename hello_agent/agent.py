#Import the Agent class from the ADK library
from google.adk.agents import Agent

# Import the multi-agent orchestrator
from .multi_agent_orchestrator import multi_agent_orchestrator

# Define the `root_agent` variable, which ADK will use to find your agent
# This will use the multi-agent orchestrator that routes to appropriate specialized agents
root_agent = multi_agent_orchestrator

# For this simple example, we don't need any tools, but you can add them later.
# tools=[]
