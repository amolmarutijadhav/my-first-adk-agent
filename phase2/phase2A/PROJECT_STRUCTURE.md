# Phase 2A: Project Structure

## 📁 Clean Architecture Organization

```
phase2A/
├── README.md                    # Main project documentation
├── PROJECT_STRUCTURE.md         # This file - project structure guide
├── requirements.txt             # Python dependencies
├── main.py                      # Main application entry point
├── start_web_ui.py             # Web UI startup script
├── run_tests.py                # Test runner script
│
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Base agent class
│   ├── tech_agent.py           # Technical support agent
│   ├── creative_agent.py       # Creative writing agent
│   ├── business_agent.py       # Business strategy agent
│   └── hello_agent.py          # General conversation agent
│
├── coordinator/                 # Coordination and routing
│   ├── __init__.py
│   ├── coordinator_agent.py    # Main coordinator
│   ├── routing_logic.py        # Intelligent query routing
│   └── agent_dispatcher.py     # Agent communication management
│
├── config/                      # Configuration management
│   ├── __init__.py
│   ├── settings.py             # Application settings
│   └── logging_config.py       # Logging configuration
│
├── web/                         # Web interface components
│   ├── __init__.py
│   ├── working_web_ui.py       # Production web UI (circuit breaker bypassed)
│   ├── web_ui.py               # Original web UI implementation
│   └── simple_web_test.py      # Simple web test
│
└── tests/                       # Comprehensive test suite
    ├── __init__.py
    ├── unit/                    # Unit tests
    │   ├── __init__.py
    │   ├── test_basic.py        # Basic functionality tests
    │   ├── test_simple.py       # Simple agent tests
    │   └── test_direct.py       # Direct agent method tests
    ├── integration/             # Integration tests
    │   ├── __init__.py
    │   └── test_production.py   # Production system tests
    └── e2e/                     # End-to-end tests
        ├── __init__.py
        └── test_web_api.py      # Web API tests
```

## 🎯 Clean Code Principles Applied

### **1. Separation of Concerns**
- **Agents**: Pure agent logic and capabilities
- **Coordinator**: Routing and orchestration
- **Config**: Settings and logging
- **Web**: UI and API endpoints
- **Tests**: Organized by test type

### **2. Single Responsibility Principle**
- Each module has one clear purpose
- Agents handle specific domains
- Coordinator handles routing decisions
- Config handles application settings

### **3. Dependency Inversion**
- Base agent class defines interface
- Specialized agents implement specific behaviors
- Coordinator depends on abstractions, not concretions

### **4. Open/Closed Principle**
- Easy to add new agents without modifying existing code
- Routing logic can be extended without changing core
- Web UI can be enhanced without affecting agents

## 🚀 Usage Guide

### **Running the Application**
```bash
# Start the main application
python main.py

# Start the web UI
python start_web_ui.py

# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py unit
python run_tests.py integration
python run_tests.py e2e
```

### **Testing Strategy**
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows

### **Web Interface**
- **Production UI**: `web/working_web_ui.py` (recommended)
- **Development UI**: `web/web_ui.py` (for debugging)
- **API Documentation**: http://localhost:8000/docs

## 📊 Benefits of This Structure

1. **Maintainability**: Clear separation makes code easy to understand and modify
2. **Testability**: Organized test structure enables comprehensive testing
3. **Scalability**: Easy to add new agents and features
4. **Reusability**: Components can be reused across different contexts
5. **Clarity**: Clear naming and organization reduces cognitive load

## 🔧 Development Workflow

1. **Add New Agent**: Create in `agents/` directory
2. **Update Routing**: Modify `coordinator/routing_logic.py`
3. **Add Tests**: Place in appropriate `tests/` subdirectory
4. **Update Config**: Modify `config/settings.py` if needed
5. **Test Changes**: Use `run_tests.py` to verify

This structure follows clean architecture principles and provides a solid foundation for the Phase 2A multi-agent system.
