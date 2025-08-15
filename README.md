# Multi-Agent ADK System

This project demonstrates a working multi-agent system using Google's Agent Development Toolkit (ADK) where different specialized agents respond based on the topic of discussion. Each agent clearly identifies itself in responses.

## 🎯 **How It Works**

The system uses an **enhanced tools-based multi-agent coordinator** that:
1. **Analyzes user input** to understand the topic and intent
2. **Calls appropriate agent tools** based on content using ADK tools
3. **Returns responses with clear agent identification** (emojis + labels)
4. **Provides expert responses** from specialized agent functions
5. **Enables multi-agent collaboration** for complex queries

## 🤖 **Available Agents**

### 1. 👋 Hello Agent
- **Purpose**: General greetings and casual conversation
- **Best for**: Welcoming users, small talk, general questions
- **Implementation**: Available in both Phase 0 and Phase 1
- **Response Format**: `👋 Hello Agent: [response]`

### 2. 💻 Tech Agent
- **Purpose**: Technical support and programming help
- **Best for**: Programming questions, debugging, technical explanations
- **Implementation**: Available in both Phase 0 and Phase 1
- **Response Format**: `💻 Tech Agent: [response]`

### 3. 🎨 Creative Agent
- **Purpose**: Creative writing and artistic projects
- **Best for**: Storytelling, brainstorming, creative writing, artistic concepts
- **Implementation**: Available in both Phase 0 and Phase 1
- **Response Format**: `🎨 Creative Agent: [response]`

### 4. 💼 Business Agent
- **Purpose**: Business strategy and professional advice
- **Best for**: Business planning, career advice, professional development
- **Implementation**: Available in both Phase 0 and Phase 1
- **Response Format**: `💼 Business Agent: [response]`

### 5. 🔀 Multi-Agent Coordinators
- **Phase 0**: Smart prompt-based coordinator (simulated multi-agent)
- **Phase 1**: Function-based coordinator (enhanced multi-agent capabilities)
- **Best for**: Primary agents for all conversations with multi-agent capabilities
- **Response Format**: `[Agent Emoji] [Agent Name]: [response]`

## 🚀 **Quick Start**

### 1. Setup Environment
```bash
# Ensure your .env file has your Google AI API key
GOOGLE_API_KEY=your_api_key_here
```

### 2. Activate Virtual Environment
```bash
.venv\Scripts\Activate.ps1
```

### 3. Run the Multi-Agent System
```bash
# To run Phase 1 (current default)
adk web

# Or use the phase switcher to choose your phase
python switch_phase.py
```

**That's it!** The system will automatically route conversations to the appropriate agent.

### 4. Phase-Specific Information
- **Current Phase**: Phase 1 (Enhanced Function-Based Multi-Agent)
- **Phase 0 Documentation**: See `phase0/README.md` (Smart Prompt-Based)
- **Phase 1 Documentation**: See `phase1/README.md` (Function-Based)
- **Testing Guide**: See `phase1/TESTING_GUIDE.md`
- **Phase Switching**: Use `python switch_phase.py` to switch between phases

## 🎯 **Topic Routing Examples**

The system automatically detects topics and routes accordingly:

| **User Input** | **Agent Response** | **Specialization** |
|----------------|-------------------|-------------------|
| "Hello there!" | `👋 Hello Agent: [response]` | General conversation |
| "How do I debug this Python code?" | `💻 Tech Agent: [response]` | Programming help |
| "Help me brainstorm a story idea" | `🎨 Creative Agent: [response]` | Creative writing |
| "What's the best business strategy?" | `💼 Business Agent: [response]` | Business advice |

## 🔧 **Development & Customization**

### Adding New Agents
1. Create a new agent file in the appropriate phase directory
2. Define the agent with appropriate instructions
3. Update the coordinator's routing logic
4. Restart the server: `adk web`

### Modifying Agent Behavior
1. Edit the agent's instruction in its file
2. Restart the server to apply changes
3. Test with relevant topics

### Testing Individual Phases
```bash
# Test Phase 0 (Smart Prompt-Based)
python switch_phase.py  # Select option 0
adk web

# Test Phase 1 (Function-Based)
python switch_phase.py  # Select option 1
adk web
```

## 📁 **Project Structure**

```
my-first-adk-agent/
├── phase0/                         # Phase 0: Smart Prompt-Based Multi-Agent
│   ├── agent.py                   # Phase 0 coordinator (smart prompt-based)
│   ├── multi_agent_orchestrator.py # Smart prompt-based coordinator
│   ├── tech_agent.py              # Technical support agent
│   ├── creative_agent.py          # Creative writing agent
│   ├── business_agent.py          # Business strategy agent
│   └── README.md                  # Phase 0 documentation
├── phase1/                         # Phase 1: Enhanced Function-Based Multi-Agent
│   ├── agent.py                   # Phase 1 coordinator (function-based)
│   ├── tools_multi_agent.py       # Enhanced function-based coordinator
│   ├── README.md                  # Phase 1 documentation
│   ├── MULTI_AGENT_PROGRESSION.md # Development path documentation
│   └── TESTING_GUIDE.md          # Testing guide for Phase 1
├── switch_phase.py                # Easy phase switching utility
├── .env                           # Environment variables
├── requirements.txt               # Dependencies
└── README.md                      # This file (main project documentation)
```

## ⚠️ **Important Notes**

- **Server Restart Required**: Changes to agent code require restarting `adk web`
- **Agent Identification**: Each response clearly shows which agent is responding
- **Automatic Routing**: No manual agent selection needed
- **Context Awareness**: Agents maintain conversation context

## 🎉 **Current Status**

✅ **Working Features:**
- Enhanced function-based multi-agent system
- True agent separation via specialized functions
- Clear agent identification in responses
- Topic-based conversation routing
- Specialized agent expertise
- Automatic agent selection
- Multi-agent collaboration capabilities
- Easy phase switching between implementations

🚀 **Ready for:**
- Adding more specialized agent tools
- Advanced conversation flows
- Custom routing logic
- Phase 2: API-based multi-agent system
- Phase 3: Message queue multi-agent system
