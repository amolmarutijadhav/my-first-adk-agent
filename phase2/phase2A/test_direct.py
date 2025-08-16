"""
Direct test to bypass circuit breaker and other complex logic.
"""

import asyncio
from agents import TechAgent, CreativeAgent, BusinessAgent, HelloAgent


async def direct_test():
    """Test agents directly without circuit breaker."""
    print("🧪 Direct Agent Test")
    print("=" * 40)
    
    # Create agents
    tech_agent = TechAgent()
    creative_agent = CreativeAgent()
    business_agent = BusinessAgent()
    hello_agent = HelloAgent()
    
    # Test queries directly
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
            
            # Call the internal method directly
            response = await agent._process_query_internal(query)
            print(f"✅ Response: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 Direct testing completed!")


if __name__ == "__main__":
    asyncio.run(direct_test())
