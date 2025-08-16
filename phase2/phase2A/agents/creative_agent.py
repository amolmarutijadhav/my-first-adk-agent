"""
Creative Agent for Phase 2A: Modular ADK Architecture.

This agent specializes in creative writing, brainstorming, artistic projects,
and storytelling.
"""

from typing import List
from .base_agent import BaseAgent


class CreativeAgent(BaseAgent):
    """
    Creative writing and brainstorming agent.
    
    This agent specializes in:
    - Creative writing and storytelling
    - Brainstorming and ideation
    - Artistic projects and design
    - Content creation and marketing
    - Creative problem solving
    """
    
    def __init__(self, name: str = "creative_agent"):
        """Initialize the creative agent."""
        super().__init__(
            name=name,
            model="gemini-2.0-flash-exp",
            description="Creative writing and brainstorming"
        )
    
    def _get_agent_instruction(self) -> str:
        """Get the instruction prompt for the creative agent."""
        return """You are a creative writing and brainstorming agent. Your expertise includes:

**Creative Writing:**
- Storytelling and narrative development
- Character creation and development
- Plot structure and story arcs
- Dialogue writing and character voice
- Poetry and creative expression
- Screenwriting and script development

**Brainstorming & Ideation:**
- Creative problem solving
- Innovation and out-of-the-box thinking
- Concept development and refinement
- Creative project planning
- Artistic direction and vision

**Content Creation:**
- Marketing copy and advertising
- Social media content
- Blog posts and articles
- Brand storytelling
- Creative presentations

**Artistic Projects:**
- Visual art concepts and descriptions
- Design thinking and user experience
- Creative direction and mood boards
- Artistic collaboration ideas
- Portfolio development

**Response Format:**
Always start your response with "🎨 Creative Agent:" and provide:
1. **Creative Analysis**: Understanding of the creative challenge
2. **Ideas & Concepts**: Multiple creative approaches and solutions
3. **Implementation**: Practical steps to bring ideas to life
4. **Inspiration**: Additional creative resources and references

**Creative Process:**
- Encourage experimentation and risk-taking
- Provide multiple perspectives and approaches
- Focus on originality and authenticity
- Consider emotional impact and audience engagement
- Balance creativity with practicality

**Storytelling Elements:**
When working with narratives, consider:
- Character motivation and development
- Plot structure and pacing
- Setting and atmosphere
- Theme and symbolism
- Conflict and resolution

**Brainstorming Techniques:**
- Mind mapping and free association
- Reverse thinking and perspective shifting
- Analogies and metaphors
- Random word association
- Constraint-based creativity

Remember to be inspiring, imaginative, and always encourage creative exploration while providing practical guidance."""

    async def _process_query_internal(self, query: str) -> str:
        """
        Process a creative query using the ADK agent.
        
        Args:
            query: Creative query from user
            
        Returns:
            Creative response with ideas and inspiration
        """
        # For now, create a simple response based on the query
        # This will be replaced with actual ADK agent processing
        query_lower = query.lower()
        
        if "story" in query_lower or "creative" in query_lower:
            response = "I love creative storytelling! I can help you develop characters, plot ideas, and creative narratives. What kind of story are you working on?"
        elif "brainstorm" in query_lower or "ideas" in query_lower:
            response = "Let's brainstorm together! I can help generate creative ideas, explore different angles, and spark your imagination."
        elif "art" in query_lower or "design" in query_lower:
            response = "Art and design are wonderful creative outlets! I can help with creative concepts, design ideas, and artistic inspiration."
        else:
            response = "I'm your Creative Agent, ready to help with storytelling, brainstorming, artistic projects, and creative writing!"
        
        # Ensure the response starts with the creative agent identifier
        if not response.startswith("🎨 Creative Agent:"):
            response = f"🎨 Creative Agent: {response}"
        
        return response
    
    def get_capabilities(self) -> List[str]:
        """Get creative agent capabilities."""
        return [
            "Creative writing and storytelling",
            "Character development and narrative",
            "Brainstorming and ideation",
            "Content creation and marketing",
            "Artistic direction and design",
            "Creative problem solving",
            "Poetry and creative expression",
            "Screenwriting and script development",
            "Brand storytelling",
            "Creative collaboration"
        ]
    
    async def brainstorm_ideas(self, topic: str, constraints: str = "") -> str:
        """
        Brainstorm creative ideas for a topic.
        
        Args:
            topic: Topic to brainstorm about
            constraints: Any constraints or requirements
            
        Returns:
            Creative ideas and approaches
        """
        query = f"Brainstorm creative ideas for: {topic}"
        if constraints:
            query += f"\n\nConstraints: {constraints}"
        return await self.process_query(query)
    
    async def develop_story(self, concept: str, genre: str = "general") -> str:
        """
        Develop a story from a concept.
        
        Args:
            concept: Story concept or premise
            genre: Story genre
            
        Returns:
            Story development and structure
        """
        query = f"Develop a {genre} story from this concept: {concept}"
        return await self.process_query(query)
    
    async def create_character(self, description: str, story_context: str = "") -> str:
        """
        Create a character for a story.
        
        Args:
            description: Character description or role
            story_context: Context of the story
            
        Returns:
            Character development and background
        """
        query = f"Create a character: {description}"
        if story_context:
            query += f"\n\nStory context: {story_context}"
        return await self.process_query(query)
    
    async def write_content(self, purpose: str, audience: str, tone: str = "professional") -> str:
        """
        Write creative content for a specific purpose.
        
        Args:
            purpose: Purpose of the content
            audience: Target audience
            tone: Desired tone
            
        Returns:
            Creative content and copy
        """
        query = f"Write {tone} content for {purpose} targeting {audience}"
        return await self.process_query(query)
    
    async def solve_creative_problem(self, problem: str, context: str = "") -> str:
        """
        Solve a problem using creative thinking.
        
        Args:
            problem: Problem to solve
            context: Problem context
            
        Returns:
            Creative solutions and approaches
        """
        query = f"Solve this problem creatively: {problem}"
        if context:
            query += f"\n\nContext: {context}"
        return await self.process_query(query)
