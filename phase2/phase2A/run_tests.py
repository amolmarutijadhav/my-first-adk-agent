"""
Test runner for Phase 2A: Modular ADK Architecture.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_tests(test_type: str = "all"):
    """Run tests based on type."""
    test_dir = Path(__file__).parent / "tests"
    
    if test_type == "unit":
        test_path = test_dir / "unit"
        print("🧪 Running Unit Tests...")
    elif test_type == "integration":
        test_path = test_dir / "integration"
        print("🔗 Running Integration Tests...")
    elif test_type == "e2e":
        test_path = test_dir / "e2e"
        print("🌐 Running End-to-End Tests...")
    else:
        test_path = test_dir
        print("🚀 Running All Tests...")
    
    # Run pytest on the test directory
    result = subprocess.run([
        sys.executable, "-m", "pytest", str(test_path), "-v"
    ], cwd=Path(__file__).parent)
    
    return result.returncode


def main():
    """Main test runner."""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "all"
    
    print("🤖 Phase 2A Test Runner")
    print("=" * 40)
    
    exit_code = run_tests(test_type)
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
