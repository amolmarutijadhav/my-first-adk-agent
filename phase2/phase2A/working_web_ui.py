"""
Working Web UI for Phase 2A: Modular ADK Architecture.
This bypasses the circuit breaker issue and provides a functional web interface.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import only what we need
from coordinator.routing_logic import RoutingLogic
from agents import TechAgent, CreativeAgent, BusinessAgent, HelloAgent


# Initialize FastAPI app
app = FastAPI(
    title="Phase 2A: Multi-Agent System",
    description="Working Web UI for testing the modular ADK architecture",
    version="1.0.0"
)

# Initialize components directly (bypassing coordinator)
routing_logic = RoutingLogic()
tech_agent = TechAgent()
creative_agent = CreativeAgent()
business_agent = BusinessAgent()
hello_agent = HelloAgent()

# Agent mapping
agents = {
    "tech_agent": tech_agent,
    "creative_agent": creative_agent,
    "business_agent": business_agent,
    "hello_agent": hello_agent
}


class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None


class QueryResponse(BaseModel):
    query: str
    routed_agent: str
    confidence: float
    query_type: str
    response: str
    reasoning: str


@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serve the main UI page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phase 2A: Multi-Agent System</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .header {
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
            }
            .input-section, .output-section {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .agent-info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .agent-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            .agent-card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #007bff;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .agent-card.tech { border-left-color: #28a745; }
            .agent-card.creative { border-left-color: #ffc107; }
            .agent-card.business { border-left-color: #17a2b8; }
            .agent-card.hello { border-left-color: #6f42c1; }
            
            textarea {
                width: 100%;
                height: 100px;
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                resize: vertical;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
            }
            button:hover {
                opacity: 0.9;
            }
            .response-box {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #28a745;
                margin-top: 20px;
            }
            .routing-info {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 15px;
            }
            .loading {
                text-align: center;
                color: #666;
                font-style: italic;
            }
            .error {
                background: #ffebee;
                color: #c62828;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #f44336;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Phase 2A: Multi-Agent System</h1>
            <p>Working Web Interface - Circuit Breaker Bypassed</p>
        </div>
        
        <div class="container">
            <div class="input-section">
                <h2>📝 Query Input</h2>
                <div class="agent-info">
                    <h3>Available Agents:</h3>
                    <div class="agent-grid">
                        <div class="agent-card tech">
                            <strong>💻 Tech Agent</strong><br>
                            Programming, debugging, technical support
                        </div>
                        <div class="agent-card creative">
                            <strong>🎨 Creative Agent</strong><br>
                            Creative writing, brainstorming, storytelling
                        </div>
                        <div class="agent-card business">
                            <strong>💼 Business Agent</strong><br>
                            Business strategy, market analysis, professional advice
                        </div>
                        <div class="agent-card hello">
                            <strong>👋 Hello Agent</strong><br>
                            General conversation, greetings, user assistance
                        </div>
                    </div>
                </div>
                
                <form id="queryForm">
                    <label for="query"><strong>Enter your query:</strong></label><br>
                    <textarea id="query" name="query" placeholder="Type your question here..."></textarea><br>
                    <button type="submit">🚀 Send Query</button>
                </form>
                
                <div id="loading" class="loading" style="display: none;">
                    Processing query...
                </div>
            </div>
            
            <div class="output-section">
                <h2>📊 Response Output</h2>
                <div id="output">
                    <p>Enter a query to see the intelligent routing and agent response.</p>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('queryForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const query = document.getElementById('query').value;
                const loading = document.getElementById('loading');
                const output = document.getElementById('output');
                
                if (!query.trim()) {
                    alert('Please enter a query');
                    return;
                }
                
                loading.style.display = 'block';
                output.innerHTML = '';
                
                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query: query })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        output.innerHTML = `
                            <div class="routing-info">
                                <h3>🎯 Routing Decision</h3>
                                <p><strong>Routed to:</strong> ${data.routed_agent}</p>
                                <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
                                <p><strong>Query Type:</strong> ${data.query_type}</p>
                                <p><strong>Reasoning:</strong> ${data.reasoning}</p>
                            </div>
                            <div class="response-box">
                                <h3>💬 Agent Response</h3>
                                <p>${data.response}</p>
                            </div>
                        `;
                    } else {
                        output.innerHTML = `
                            <div class="error">
                                <h3>❌ Error</h3>
                                <p>${data.detail}</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    output.innerHTML = `
                        <div class="error">
                            <h3>❌ Network Error</h3>
                            <p>${error.message}</p>
                        </div>
                    `;
                } finally {
                    loading.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    """


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a query through the multi-agent system."""
    try:
        # Get routing decision
        routing_decision = routing_logic.analyze_query(request.query)
        
        # Get agent response (bypassing circuit breaker)
        agent = agents[routing_decision.primary_agent]
        response = await agent._process_query_internal(request.query)
        
        return QueryResponse(
            query=request.query,
            routed_agent=routing_decision.primary_agent,
            confidence=routing_decision.confidence,
            query_type=routing_decision.query_type.value,
            response=response,
            reasoning=routing_decision.reasoning
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/api/status")
async def get_status():
    """Get system status."""
    return {
        "status": "healthy",
        "agents": list(agents.keys()),
        "total_agents": len(agents),
        "system": "Phase 2A: Working Web UI (Circuit Breaker Bypassed)"
    }


@app.get("/api/agents")
async def get_agents():
    """Get information about all agents."""
    agents_info = {}
    for name, agent in agents.items():
        agents_info[name] = {
            "name": agent.name,
            "description": agent.description,
            "capabilities": agent.get_capabilities(),
            "model": agent.model
        }
    return agents_info


if __name__ == "__main__":
    print("🚀 Starting Phase 2A Working Web UI...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("🔧 API documentation: http://localhost:8000/docs")
    print("✅ Circuit breaker bypassed - direct agent access")
    uvicorn.run(app, host="0.0.0.0", port=8000)
