#Import the Agent class from the ADK library
from google.adk.agents import Agent

# Import the smart prompt-based multi-agent orchestrator from Phase 0
from .multi_agent_orchestrator import multi_agent_orchestrator

# Define the `root_agent` variable, which ADK will use to find your agent
# This will use the smart prompt-based multi-agent orchestrator from Phase 0
root_agent = multi_agent_orchestrator

# For this phase, we have smart prompt-based multi-agent simulation
# The orchestrator uses intelligent prompt engineering to simulate multiple agents
