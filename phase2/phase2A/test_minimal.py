"""
Minimal test to isolate the 'gen' error.
"""

import asyncio


async def simple_test():
    """Simple test without any agent dependencies."""
    print("🧪 Minimal Test")
    print("=" * 30)
    
    try:
        # Test basic async functionality
        await asyncio.sleep(0.1)
        print("✅ Basic async works")
        
        # Test string operations
        test_string = "Hello, world!"
        if "Hello" in test_string:
            print("✅ String operations work")
        
        print("🎉 Minimal test passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(simple_test())
