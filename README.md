# Multi-Agent ADK System

This project demonstrates a working multi-agent system using Google's Agent Development Toolkit (ADK) where different specialized agents respond based on the topic of discussion. Each agent clearly identifies itself in responses.

## 🎯 **How It Works**

The system uses a **multi-agent orchestrator** that:
1. **Analyzes user input** to understand the topic and intent
2. **Routes to the appropriate specialized agent** based on content
3. **Returns responses with clear agent identification** (emojis + labels)
4. **Provides expert responses** from the most suitable agent

## 🤖 **Available Agents**

### 1. 👋 Hello Agent
- **Purpose**: General greetings and casual conversation
- **Best for**: Welcoming users, small talk, general questions
- **File**: `hello_agent/agent.py` (main orchestrator)
- **Response Format**: `👋 Hello Agent: [response]`

### 2. 💻 Tech Agent
- **Purpose**: Technical support and programming help
- **Best for**: Programming questions, debugging, technical explanations
- **File**: `hello_agent/tech_agent.py`
- **Response Format**: `💻 Tech Agent: [response]`

### 3. 🎨 Creative Agent
- **Purpose**: Creative writing and artistic projects
- **Best for**: Storytelling, brainstorming, creative writing, artistic concepts
- **File**: `hello_agent/creative_agent.py`
- **Response Format**: `🎨 Creative Agent: [response]`

### 4. 💼 Business Agent
- **Purpose**: Business strategy and professional advice
- **Best for**: Business planning, career advice, professional development
- **File**: `hello_agent/business_agent.py`
- **Response Format**: `💼 Business Agent: [response]`

### 5. 🔀 Multi-Agent Orchestrator
- **Purpose**: Main coordinator that routes to appropriate agents
- **Best for**: Primary agent for all conversations
- **File**: `hello_agent/multi_agent_orchestrator.py`
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
adk web
```

**That's it!** The system will automatically route conversations to the appropriate agent.

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
1. Create a new agent file (e.g., `hello_agent/math_agent.py`)
2. Define the agent with appropriate instructions
3. Update the orchestrator's routing logic
4. Restart the server: `adk web`

### Modifying Agent Behavior
1. Edit the agent's instruction in its file
2. Restart the server to apply changes
3. Test with relevant topics

### Testing Individual Agents
```bash
# Test specific agents directly
adk web --agent tech_agent
adk web --agent creative_agent
adk web --agent business_agent
```

## 📁 **Project Structure**

```
my-first-adk-agent/
├── hello_agent/
│   ├── agent.py                    # Main orchestrator (root agent)
│   ├── multi_agent_orchestrator.py # Multi-agent coordinator
│   ├── tech_agent.py              # Technical support agent
│   ├── creative_agent.py          # Creative writing agent
│   ├── business_agent.py          # Business strategy agent
│   └── router_agent.py            # Topic router (optional)
├── .env                           # Environment variables
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## ⚠️ **Important Notes**

- **Server Restart Required**: Changes to agent code require restarting `adk web`
- **Agent Identification**: Each response clearly shows which agent is responding
- **Automatic Routing**: No manual agent selection needed
- **Context Awareness**: Agents maintain conversation context

## 🎉 **Current Status**

✅ **Working Features:**
- Multi-agent routing system
- Clear agent identification in responses
- Topic-based conversation routing
- Specialized agent expertise
- Automatic agent selection

🚀 **Ready for:**
- Adding more specialized agents
- Implementing agent tools
- Advanced conversation flows
- Custom routing logic
