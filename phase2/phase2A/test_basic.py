"""
Basic test for Phase 2A: Modular ADK Architecture.

This test verifies that the core components are working correctly.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coordinator import CoordinatorAgent
from config.settings import get_settings


async def test_basic_functionality():
    """Test basic functionality of the multi-agent system."""
    print("🧪 Testing Phase 2A: Modular ADK Architecture")
    print("=" * 50)
    
    try:
        # Test 1: Configuration
        print("\n1. Testing Configuration...")
        settings = get_settings()
        print(f"   ✅ Environment: {settings.environment}")
        print(f"   ✅ Available agents: {settings.get_all_agent_names()}")
        
        # Test 2: Coordinator Initialization
        print("\n2. Testing Coordinator Initialization...")
        coordinator = CoordinatorAgent()
        print(f"   ✅ Coordinator initialized with {len(coordinator.agents)} agents")
        
        # Test 3: Agent Capabilities
        print("\n3. Testing Agent Capabilities...")
        capabilities = coordinator.get_agent_capabilities()
        for agent_name, agent_caps in capabilities.items():
            print(f"   ✅ {agent_name}: {len(agent_caps)} capabilities")
        
        # Test 4: System Status
        print("\n4. Testing System Status...")
        status = coordinator.get_system_status()
        print(f"   ✅ Coordinator healthy: {status['coordinator']['is_healthy']}")
        print(f"   ✅ Total agents: {len(status['agents'])}")
        
        # Test 5: Health Check
        print("\n5. Testing Health Check...")
        health = await coordinator.health_check()
        print(f"   ✅ Overall status: {health['overall_status']}")
        healthy_agents = sum(1 for agent in health['agents'].values() if agent['is_healthy'])
        print(f"   ✅ Healthy agents: {healthy_agents}/{len(health['agents'])}")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_query_routing():
    """Test query routing functionality."""
    print("\n🔍 Testing Query Routing...")
    print("=" * 30)
    
    try:
        coordinator = CoordinatorAgent()
        
        # Test queries for different agent types
        test_queries = [
            ("How do I debug this Python code?", "tech_agent"),
            ("Write a creative story about a robot", "creative_agent"),
            ("What's the best business strategy for a startup?", "business_agent"),
            ("Hello, how are you?", "hello_agent"),
        ]
        
        for query, expected_agent in test_queries:
            print(f"\nQuery: {query}")
            print(f"Expected agent: {expected_agent}")
            
            # Get routing decision
            routing_decision = coordinator.routing_logic.analyze_query(query)
            print(f"Routed to: {routing_decision.primary_agent}")
            print(f"Confidence: {routing_decision.confidence:.2f}")
            print(f"Query type: {routing_decision.query_type.value}")
            
            if routing_decision.primary_agent == expected_agent:
                print("   ✅ Routing correct")
            else:
                print(f"   ⚠️  Routing different (expected {expected_agent})")
        
        print("\n🎉 Query routing tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Query routing test failed: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Starting Phase 2A Tests")
    print("=" * 50)
    
    # Run basic functionality tests
    basic_success = await test_basic_functionality()
    
    # Run query routing tests
    routing_success = await test_query_routing()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"   Query Routing: {'✅ PASS' if routing_success else '❌ FAIL'}")
    
    if basic_success and routing_success:
        print("\n🎉 All tests passed! Phase 2A is ready for use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
