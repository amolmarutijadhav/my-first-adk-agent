#Import the Agent class from the ADK library
from google.adk.agents import Agent

# Define the agent with a name, model, and instruction.
# The 'instruction' tells the agent how it should behave.
hello_agent = Agent(
    name="hello_agent",
    model="gemini-2.0-flash-exp",  # Use a compatible Gemini model
    description="A simple agent that greets the user.",
    instruction="You are a friendly assistant. Your only job is to greet the user with 'Hello, World!' whenever they say hello. Do not perform any other tasks."
)

# Define the `root_agent` variable, which ADK will use to find your agent
root_agent = hello_agent

# For this simple example, we don't need any tools, but you can add them later.
# tools=[]
