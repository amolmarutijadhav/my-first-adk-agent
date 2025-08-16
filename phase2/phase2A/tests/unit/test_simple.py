"""
Simple test to verify agent functionality without ADK dependency.
"""

import asyncio
import sys
import os
import pytest

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents import TechAgent, CreativeAgent, BusinessAgent, HelloAgent


@pytest.mark.asyncio
async def test_agents():
    """Test that agents can process queries."""
    print("🧪 Testing Agent Query Processing")
    print("=" * 50)

    # Create agents
    tech_agent = TechAgent()
    creative_agent = CreativeAgent()
    business_agent = BusinessAgent()
    hello_agent = HelloAgent()

    # Test queries
    test_cases = [
        (tech_agent, "How do I debug Python code?", "Tech Agent"),
        (creative_agent, "Write a creative story", "Creative Agent"),
        (business_agent, "Business strategy for startup", "Business Agent"),
        (hello_agent, "Hello, how are you?", "Hello Agent"),
    ]

    for agent, query, agent_name in test_cases:
        try:
            print(f"\n🔍 Testing {agent_name}...")
            print(f"Query: {query}")

            # Use direct method to bypass circuit breaker
            response = await agent._process_query_internal(query)
            print(f"✅ Response: {response}")
            assert response is not None
            assert len(response) > 0

        except Exception as e:
            print(f"❌ Error: {e}")
            assert False, f"Agent {agent_name} failed: {e}"

    print("\n🎉 Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_agents())
