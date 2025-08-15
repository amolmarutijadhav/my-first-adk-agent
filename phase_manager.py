#!/usr/bin/env python3
"""
Phase Manager for Multi-Agent ADK System

This tool provides information about available phases and how to access them.
"""

import os
import sys

def show_phase_info():
    """Show information about available phases."""
    print("🎯 Multi-Agent ADK System - Phase Manager")
    print("=" * 60)
    
    print("\n📁 **Available Phases:**")
    print()
    
    # Phase 0 Info
    print("🔹 **Phase 0: Smart Prompt-Based Multi-Agent**")
    print("   📂 Directory: phase0/")
    print("   🎯 Type: Smart prompt-based simulation")
    print("   🌐 Access: http://localhost:8000/apps/phase0/")
    print("   📋 Features: Intelligent prompt engineering, simulated multi-agent behavior")
    print("   📊 Complexity: ⭐⭐ Low")
    print()
    
    # Phase 1 Info
    print("🔹 **Phase 1: Enhanced Function-Based Multi-Agent**")
    print("   📂 Directory: phase1/")
    print("   🎯 Type: Function-based enhanced system")
    print("   🌐 Access: http://localhost:8000/apps/phase1/")
    print("   📋 Features: True agent separation via specialized functions")
    print("   📊 Complexity: ⭐⭐⭐ Medium")
    print()

def show_usage_instructions():
    """Show how to use the different phases."""
    print("🚀 **How to Use:**")
    print()
    print("1. **Start the ADK Server:**")
    print("   ```bash")
    print("   adk web")
    print("   ```")
    print()
    print("2. **Access Different Phases:**")
    print("   - Phase 0: http://localhost:8000/apps/phase0/")
    print("   - Phase 1: http://localhost:8000/apps/phase1/")
    print()
    print("3. **Test Each Phase:**")
    print("   Try these queries in each phase:")
    print("   - 'Hello there!' (Hello Agent)")
    print("   - 'How do I debug this Python code?' (Tech Agent)")
    print("   - 'Help me brainstorm a story idea' (Creative Agent)")
    print("   - 'What's the best business strategy?' (Business Agent)")
    print()

def show_phase_comparison():
    """Show comparison between phases."""
    print("📊 **Phase Comparison:**")
    print()
    print("| Aspect | Phase 0 | Phase 1 |")
    print("|--------|---------|---------|")
    print("| **Implementation** | Smart prompt-based | Function-based |")
    print("| **Agent Separation** | Simulated | Real separation |")
    print("| **Complexity** | ⭐⭐ Low | ⭐⭐⭐ Medium |")
    print("| **Performance** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐ Medium |")
    print("| **Scalability** | ⭐⭐ Low | ⭐⭐⭐ Medium |")
    print("| **True Multi-Agent** | ❌ No | ⚠️ Partial |")
    print()

def show_testing_guide():
    """Show testing guide for both phases."""
    print("🧪 **Testing Guide:**")
    print()
    print("**Phase 0 Testing:**")
    print("1. Go to: http://localhost:8000/apps/phase0/")
    print("2. Test smart prompt-based routing")
    print("3. Observe simulated multi-agent behavior")
    print()
    print("**Phase 1 Testing:**")
    print("1. Go to: http://localhost:8000/apps/phase1/")
    print("2. Test function-based agent calls")
    print("3. Observe enhanced multi-agent capabilities")
    print()
    print("**Comparison Testing:**")
    print("1. Test same queries in both phases")
    print("2. Compare response quality and speed")
    print("3. Observe differences in agent identification")
    print()

def main():
    """Main function to handle phase management."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "info":
            show_phase_info()
        elif command == "usage":
            show_usage_instructions()
        elif command == "compare":
            show_phase_comparison()
        elif command == "test":
            show_testing_guide()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: info, usage, compare, test")
    else:
        # Show all information
        show_phase_info()
        show_usage_instructions()
        show_phase_comparison()
        show_testing_guide()
        
        print("💡 **Quick Commands:**")
        print("   python phase_manager.py info     - Show phase information")
        print("   python phase_manager.py usage    - Show usage instructions")
        print("   python phase_manager.py compare  - Show phase comparison")
        print("   python phase_manager.py test     - Show testing guide")

if __name__ == "__main__":
    main()
