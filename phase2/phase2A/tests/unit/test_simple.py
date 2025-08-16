"""
Simple test to verify agent functionality without ADK dependency.
"""

import asyncio
from agents import TechAgent, CreativeAgent, BusinessAgent, HelloAgent


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
            
            response = await agent.process_query(query)
            print(f"✅ Response: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(test_agents())
