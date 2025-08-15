#Import the Agent class from the ADK library
from google.adk.agents import Agent

# Import the enhanced tools-based multi-agent coordinator from Phase 1
from .tools_multi_agent import tools_multi_agent_coordinator

# Define the `root_agent` variable, which ADK will use to find your agent
# This will use the enhanced tools-based multi-agent coordinator from Phase 1
root_agent = tools_multi_agent_coordinator

# For this enhanced example, we now have true multi-agent capabilities via tools
# tools=[tech_tool, creative_tool, business_tool, hello_tool, collaboration_tool]
