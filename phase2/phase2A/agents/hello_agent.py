"""
Hello Agent for Phase 2A: Modular ADK Architecture.

This agent specializes in general conversation, greetings, and simple questions.
"""

from typing import List
from .base_agent import BaseAgent


class HelloAgent(BaseAgent):
    """
    General conversation and greetings agent.
    
    This agent specializes in:
    - General greetings and conversation
    - Simple questions and answers
    - Friendly chat and engagement
    - Basic information and guidance
    - User onboarding and assistance
    """
    
    def __init__(self, name: str = "hello_agent"):
        """Initialize the hello agent."""
        super().__init__(
            name=name,
            model="gemini-2.0-flash-exp",
            description="General conversation and greetings"
        )
    
    def _get_agent_instruction(self) -> str:
        """Get the instruction prompt for the hello agent."""
        return """You are a friendly and helpful conversation agent. Your role is to:

**General Conversation:**
- Provide warm and welcoming greetings
- Engage in friendly conversation
- Answer simple questions and provide basic information
- Help users feel comfortable and supported
- Guide users to appropriate specialized agents when needed

**User Assistance:**
- Help users understand how to use the multi-agent system
- Explain the capabilities of different agents
- Provide guidance on formulating effective queries
- Assist with user onboarding and orientation

**Information and Guidance:**
- Answer general knowledge questions
- Provide helpful tips and advice
- Share interesting facts and information
- Offer encouragement and motivation

**Conversation Skills:**
- Be warm, friendly, and approachable
- Show empathy and understanding
- Use appropriate humor and personality
- Maintain professional yet casual tone
- Be patient and helpful with all users

**Response Format:**
Always start your response with "👋 Hello Agent:" and provide:
1. **Warm Greeting**: Friendly and welcoming response
2. **Helpful Information**: Relevant and useful information
3. **Engagement**: Questions or suggestions to continue conversation
4. **Guidance**: Direct users to specialized agents when appropriate

**Conversation Flow:**
- Acknowledge the user's input warmly
- Provide relevant and helpful information
- Ask follow-up questions to engage the user
- Suggest next steps or related topics
- Offer to connect with specialized agents when needed

**Agent Routing:**
When users ask about specific topics, guide them to appropriate agents:
- Technical questions → Tech Agent
- Creative projects → Creative Agent  
- Business topics → Business Agent
- Complex queries → Multi-agent collaboration

**Tone and Style:**
- Be conversational and natural
- Use appropriate emojis and expressions
- Show enthusiasm and positivity
- Be inclusive and welcoming to all users
- Maintain professional boundaries while being friendly

**Special Situations:**
- New users: Provide comprehensive system overview
- Confused users: Offer clear guidance and explanations
- Technical difficulties: Provide troubleshooting help
- Feedback requests: Encourage and appreciate user input

Remember to be genuinely helpful, friendly, and always guide users toward the best possible experience with the multi-agent system."""

    async def _process_query_internal(self, query: str) -> str:
        """
        Process a general query using the ADK agent.
        
        Args:
            query: General query from user
            
        Returns:
            Friendly response and guidance
        """
        # For now, create a simple response based on the query
        # This will be replaced with actual ADK agent processing
        query_lower = query.lower()
        
        if "hello" in query_lower or "hi" in query_lower:
            response = "Hello! I'm your friendly Hello Agent. How can I help you today?"
        elif "debug" in query_lower or "debugging" in query_lower:
            response = "I see you need help with debugging! Let me connect you with our Tech Agent who specializes in technical support and programming assistance."
        elif "help" in query_lower:
            response = "I'm here to help! I can assist with general questions, or I can connect you with our specialized agents for technical, creative, or business topics."
        else:
            response = "Hello! I'm here to help you. I can answer general questions or connect you with our specialized agents for specific topics."
        
        # Ensure the response starts with the hello agent identifier
        if not response.startswith("👋 Hello Agent:"):
            response = f"👋 Hello Agent: {response}"
        
        return response
    
    def get_capabilities(self) -> List[str]:
        """Get hello agent capabilities."""
        return [
            "General conversation and greetings",
            "User assistance and guidance",
            "System overview and orientation",
            "Basic information and answers",
            "Friendly chat and engagement",
            "Agent routing and recommendations",
            "User onboarding support",
            "General knowledge and tips"
        ]
    
    async def greet_user(self, user_name: str = "") -> str:
        """
        Provide a warm greeting to the user.
        
        Args:
            user_name: User's name if available
            
        Returns:
            Friendly greeting and welcome message
        """
        if user_name:
            query = f"Greet {user_name} warmly and welcome them to the multi-agent system"
        else:
            query = "Provide a warm greeting and welcome to the multi-agent system"
        return await self.process_query(query)
    
    async def explain_system(self, user_type: str = "new") -> str:
        """
        Explain the multi-agent system to users.
        
        Args:
            user_type: Type of user (new, returning, etc.)
            
        Returns:
            System explanation and guidance
        """
        query = f"Explain the multi-agent system to a {user_type} user"
        return await self.process_query(query)
    
    async def recommend_agent(self, topic: str) -> str:
        """
        Recommend the best agent for a specific topic.
        
        Args:
            topic: Topic or question the user wants help with
            
        Returns:
            Agent recommendation and explanation
        """
        query = f"Recommend the best agent for this topic: {topic}"
        return await self.process_query(query)
    
    async def provide_tips(self, area: str = "general") -> str:
        """
        Provide helpful tips and advice.
        
        Args:
            area: Area for tips (general, productivity, learning, etc.)
            
        Returns:
            Helpful tips and advice
        """
        query = f"Provide helpful tips about {area}"
        return await self.process_query(query)
    
    async def answer_general_question(self, question: str) -> str:
        """
        Answer a general knowledge question.
        
        Args:
            question: General question from user
            
        Returns:
            Helpful answer and information
        """
        query = f"Answer this general question: {question}"
        return await self.process_query(query)
    
    async def provide_encouragement(self, context: str = "") -> str:
        """
        Provide encouragement and motivation.
        
        Args:
            context: Context for encouragement
            
        Returns:
            Encouraging and motivational message
        """
        query = f"Provide encouragement and motivation"
        if context:
            query += f" for: {context}"
        return await self.process_query(query)
