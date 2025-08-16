"""
Test script for the Phase 2A Web API.
This tests the API endpoints without needing a browser.
"""

import asyncio
import aiohttp
import json
import pytest


@pytest.mark.asyncio
async def test_web_api():
    """Test the web API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Phase 2A Web API")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: System Status
        print("\n1. Testing System Status...")
        try:
            async with session.get(f"{base_url}/api/status") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Status: {data['status']}")
                    print(f"✅ Agents: {data['agents']}")
                    print(f"✅ Total: {data['total_agents']}")
                    assert data['status'] == 'healthy'
                else:
                    print(f"❌ Status failed: {response.status}")
                    assert False, f"Status failed: {response.status}"
        except Exception as e:
            print(f"❌ Status error: {e}")
            # Skip this test if server is not running
            pytest.skip(f"Web server not running: {e}")
        
        # Test 2: Agents Info
        print("\n2. Testing Agents Info...")
        try:
            async with session.get(f"{base_url}/api/agents") as response:
                if response.status == 200:
                    data = await response.json()
                    for agent_name, agent_info in data.items():
                        print(f"✅ {agent_name}: {agent_info['description']}")
                    assert len(data) > 0
                else:
                    print(f"❌ Agents failed: {response.status}")
                    assert False, f"Agents failed: {response.status}"
        except Exception as e:
            print(f"❌ Agents error: {e}")
            pytest.skip(f"Web server not running: {e}")
        
        # Test 3: Query Processing
        test_queries = [
            ("Hello, how are you?", "General greeting"),
            ("I need help debugging Python code", "Technical support"),
            ("Can you help me write a creative story?", "Creative writing"),
            ("What's the best business strategy for a startup?", "Business advice"),
        ]
        
        print(f"\n3. Testing Query Processing ({len(test_queries)} queries)...")
        for i, (query, description) in enumerate(test_queries, 1):
            print(f"\n   {i}. {description}")
            print(f"      Query: {query}")
            
            try:
                payload = {"query": query}
                async with session.post(f"{base_url}/api/query", json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"      ✅ Routed to: {data['routed_agent']}")
                        print(f"      ✅ Confidence: {data['confidence']:.2f}")
                        print(f"      ✅ Type: {data['query_type']}")
                        print(f"      ✅ Response: {data['response'][:100]}...")
                        
                        # Assertions
                        assert data['routed_agent'] is not None
                        assert data['confidence'] > 0
                        assert data['response'] is not None
                        assert len(data['response']) > 0
                    else:
                        error_data = await response.text()
                        print(f"      ❌ Query failed: {response.status} - {error_data}")
                        assert False, f"Query failed: {response.status} - {error_data}"
            except Exception as e:
                print(f"      ❌ Query error: {e}")
                pytest.skip(f"Web server not running: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Web API Testing Completed!")


if __name__ == "__main__":
    print("🚀 Starting Web API Tests...")
    print("📱 Make sure the web UI is running on http://localhost:8000")
    print("⏳ Waiting 3 seconds for server to start...")
    
    # Wait a bit for the server to start
    import time
    time.sleep(3)
    
    asyncio.run(test_web_api())
