"""
Technical Agent for Phase 2A: Modular ADK Architecture.

This agent specializes in technical support, programming assistance,
debugging, and system-related queries.
"""

import asyncio
from typing import List
from .base_agent import BaseAgent


class TechAgent(BaseAgent):
    """
    Technical support and programming assistance agent.
    
    This agent specializes in:
    - Programming and code assistance
    - Debugging and troubleshooting
    - Technical architecture and design
    - System administration
    - Development best practices
    """
    
    def __init__(self, name: str = "tech_agent"):
        """Initialize the tech agent."""
        super().__init__(
            name=name,
            model="gemini-2.0-flash-exp",
            description="Technical support and programming assistance"
        )
    
    def _get_agent_instruction(self) -> str:
        """Get the instruction prompt for the tech agent."""
        return """You are a technical support and programming assistance agent. Your expertise includes:

**Programming Languages & Frameworks:**
- Python, JavaScript, TypeScript, Java, C++, Go, Rust
- Web frameworks (React, Angular, Vue, Django, Flask, FastAPI)
- Mobile development (React Native, Flutter, iOS, Android)
- Database technologies (SQL, NoSQL, ORMs)

**Technical Domains:**
- Software architecture and design patterns
- API development and integration
- DevOps and CI/CD pipelines
- Cloud platforms (AWS, GCP, Azure)
- Containerization and orchestration (Docker, Kubernetes)
- System administration and infrastructure

**Problem Solving:**
- Code debugging and troubleshooting
- Performance optimization
- Security best practices
- Testing strategies
- Code review and refactoring

**Response Format:**
Always start your response with "💻 Tech Agent:" and provide:
1. **Technical Analysis**: Clear explanation of the technical concepts
2. **Practical Solutions**: Step-by-step guidance or code examples
3. **Best Practices**: Industry standards and recommendations
4. **Additional Resources**: Links to documentation or learning materials

**Code Examples:**
When providing code, ensure it's:
- Well-commented and documented
- Following best practices
- Production-ready when appropriate
- Include error handling

**Troubleshooting:**
For debugging requests, provide:
- Systematic approach to problem identification
- Common causes and solutions
- Diagnostic steps and tools
- Prevention strategies

Remember to be precise, practical, and always consider security and performance implications."""

    async def _process_query_internal(self, query: str) -> str:
        """
        Process a technical query using the ADK agent.
        
        Args:
            query: Technical query from user
            
        Returns:
            Technical response with analysis and solutions
        """
        # For now, create a simple response based on the query
        # This will be replaced with actual ADK agent processing
        query_lower = query.lower()
        
        if "debug" in query_lower or "debugging" in query_lower:
            response = "I can help you with debugging! Here are some general debugging steps: 1) Check for syntax errors, 2) Use print statements or a debugger, 3) Review the error messages carefully, 4) Test with smaller inputs."
        elif "python" in query_lower:
            response = "Python is a great language! I can help with Python programming, debugging, best practices, and more. What specific Python question do you have?"
        elif "code" in query_lower:
            response = "I'm here to help with your coding questions! I can assist with debugging, code review, best practices, and technical guidance."
        else:
            response = "I'm your Tech Agent, ready to help with technical questions, programming, debugging, and system-related issues."
        
        # Ensure the response starts with the tech agent identifier
        if not response.startswith("💻 Tech Agent:"):
            response = f"💻 Tech Agent: {response}"
        
        return response
    
    def get_capabilities(self) -> List[str]:
        """Get tech agent capabilities."""
        return [
            "Programming and code assistance",
            "Debugging and troubleshooting", 
            "Software architecture and design",
            "API development and integration",
            "DevOps and CI/CD",
            "Cloud platforms and infrastructure",
            "System administration",
            "Performance optimization",
            "Security best practices",
            "Testing strategies"
        ]
    
    async def analyze_code(self, code: str, language: str = "python") -> str:
        """
        Analyze code for issues and improvements.
        
        Args:
            code: Code to analyze
            language: Programming language
            
        Returns:
            Code analysis and recommendations
        """
        query = f"Please analyze this {language} code and provide feedback:\n\n```{language}\n{code}\n```"
        return await self.process_query(query)
    
    async def debug_issue(self, error_message: str, context: str = "") -> str:
        """
        Help debug a technical issue.
        
        Args:
            error_message: Error message or description
            context: Additional context about the issue
            
        Returns:
            Debugging guidance and solutions
        """
        query = f"Help me debug this issue:\n\nError: {error_message}\n\nContext: {context}"
        return await self.process_query(query)
    
    async def explain_concept(self, concept: str, level: str = "intermediate") -> str:
        """
        Explain a technical concept.
        
        Args:
            concept: Technical concept to explain
            level: Explanation level (beginner, intermediate, advanced)
            
        Returns:
            Technical explanation
        """
        query = f"Explain the concept of '{concept}' at a {level} level with practical examples."
        return await self.process_query(query)
    
    async def provide_best_practices(self, topic: str) -> str:
        """
        Provide best practices for a technical topic.
        
        Args:
            topic: Technical topic for best practices
            
        Returns:
            Best practices and recommendations
        """
        query = f"What are the best practices for {topic}? Include security, performance, and maintainability considerations."
        return await self.process_query(query)
