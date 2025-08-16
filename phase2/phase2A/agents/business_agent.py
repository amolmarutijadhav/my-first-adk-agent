"""
Business Agent for Phase 2A: Modular ADK Architecture.

This agent specializes in business strategy, analysis, professional advice,
and career guidance.
"""

from typing import List
from .base_agent import BaseAgent


class BusinessAgent(BaseAgent):
    """
    Business strategy and analysis agent.
    
    This agent specializes in:
    - Business strategy and planning
    - Market analysis and research
    - Financial planning and analysis
    - Professional development and career guidance
    - Business operations and management
    """
    
    def __init__(self, name: str = "business_agent"):
        """Initialize the business agent."""
        super().__init__(
            name=name,
            model="gemini-2.0-flash-exp",
            description="Business strategy and analysis"
        )
    
    def _get_agent_instruction(self) -> str:
        """Get the instruction prompt for the business agent."""
        return """You are a business strategy and analysis agent. Your expertise includes:

**Business Strategy:**
- Strategic planning and business models
- Market analysis and competitive intelligence
- Business development and growth strategies
- Innovation and digital transformation
- Risk management and mitigation

**Financial Analysis:**
- Financial planning and budgeting
- Investment analysis and portfolio management
- Cost-benefit analysis and ROI calculations
- Financial modeling and forecasting
- Funding strategies and capital raising

**Market Research:**
- Market sizing and opportunity assessment
- Customer segmentation and persona development
- Competitive analysis and positioning
- Industry trends and market dynamics
- Product-market fit analysis

**Professional Development:**
- Career planning and advancement strategies
- Leadership development and management skills
- Networking and relationship building
- Personal branding and professional presence
- Work-life balance and productivity

**Business Operations:**
- Process optimization and efficiency
- Supply chain and operations management
- Quality management and continuous improvement
- Change management and organizational development
- Performance measurement and KPIs

**Response Format:**
Always start your response with "💼 Business Agent:" and provide:
1. **Strategic Analysis**: Understanding of the business context and challenges
2. **Market Insights**: Relevant market data and competitive landscape
3. **Strategic Recommendations**: Actionable business strategies and solutions
4. **Implementation Plan**: Practical steps and timeline for execution
5. **Risk Assessment**: Potential risks and mitigation strategies

**Business Framework:**
Use established business frameworks such as:
- SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
- Porter's Five Forces
- PESTEL Analysis (Political, Economic, Social, Technological, Environmental, Legal)
- Business Model Canvas
- Value Chain Analysis
- Balanced Scorecard

**Financial Considerations:**
- Always consider financial implications and ROI
- Provide realistic cost estimates and timelines
- Include risk assessment and contingency planning
- Consider cash flow and funding requirements

**Market Perspective:**
- Analyze market trends and competitive landscape
- Consider customer needs and market demand
- Evaluate market entry and expansion opportunities
- Assess regulatory and compliance requirements

**Professional Guidance:**
- Provide evidence-based recommendations
- Consider industry best practices and benchmarks
- Include case studies and real-world examples
- Offer actionable next steps and follow-up actions

Remember to be strategic, analytical, and always provide practical, implementable business solutions."""

    async def _process_query_internal(self, query: str) -> str:
        """
        Process a business query using the ADK agent.
        
        Args:
            query: Business query from user
            
        Returns:
            Business analysis and strategic recommendations
        """
        # For now, create a simple response based on the query
        # This will be replaced with actual ADK agent processing
        query_lower = query.lower()
        
        if "strategy" in query_lower or "business" in query_lower:
            response = "I can help with business strategy! I can assist with market analysis, competitive intelligence, business models, and strategic planning."
        elif "startup" in query_lower or "entrepreneur" in query_lower:
            response = "Startups are exciting! I can help with business planning, funding strategies, market validation, and growth tactics."
        elif "analysis" in query_lower or "market" in query_lower:
            response = "Business analysis is crucial! I can help with market research, competitive analysis, financial modeling, and strategic insights."
        else:
            response = "I'm your Business Agent, ready to help with business strategy, analysis, professional advice, and career guidance!"
        
        # Ensure the response starts with the business agent identifier
        if not response.startswith("💼 Business Agent:"):
            response = f"💼 Business Agent: {response}"
        
        return response
    
    def get_capabilities(self) -> List[str]:
        """Get business agent capabilities."""
        return [
            "Business strategy and planning",
            "Market analysis and research",
            "Financial planning and analysis",
            "Professional development",
            "Career guidance and advancement",
            "Business operations and management",
            "Investment analysis",
            "Risk management",
            "Competitive intelligence",
            "Strategic consulting"
        ]
    
    async def analyze_market(self, industry: str, region: str = "global") -> str:
        """
        Analyze market opportunities and trends.
        
        Args:
            industry: Industry to analyze
            region: Geographic region
            
        Returns:
            Market analysis and insights
        """
        query = f"Provide a comprehensive market analysis for the {industry} industry in {region}"
        return await self.process_query(query)
    
    async def develop_strategy(self, business_context: str, goals: str) -> str:
        """
        Develop business strategy for specific goals.
        
        Args:
            business_context: Business context and current situation
            goals: Business goals and objectives
            
        Returns:
            Strategic plan and recommendations
        """
        query = f"Develop a business strategy for:\n\nContext: {business_context}\n\nGoals: {goals}"
        return await self.process_query(query)
    
    async def financial_analysis(self, scenario: str, timeframe: str = "1 year") -> str:
        """
        Perform financial analysis for a business scenario.
        
        Args:
            scenario: Business scenario to analyze
            timeframe: Analysis timeframe
            
        Returns:
            Financial analysis and recommendations
        """
        query = f"Provide financial analysis for: {scenario}\n\nTimeframe: {timeframe}"
        return await self.process_query(query)
    
    async def career_guidance(self, current_role: str, career_goals: str) -> str:
        """
        Provide career guidance and development advice.
        
        Args:
            current_role: Current professional role
            career_goals: Career goals and aspirations
            
        Returns:
            Career development plan and advice
        """
        query = f"Provide career guidance for:\n\nCurrent Role: {current_role}\n\nCareer Goals: {career_goals}"
        return await self.process_query(query)
    
    async def competitive_analysis(self, company: str, industry: str) -> str:
        """
        Perform competitive analysis for a company.
        
        Args:
            company: Company to analyze
            industry: Industry context
            
        Returns:
            Competitive analysis and positioning
        """
        query = f"Perform competitive analysis for {company} in the {industry} industry"
        return await self.process_query(query)
    
    async def business_plan_review(self, business_plan: str) -> str:
        """
        Review and provide feedback on a business plan.
        
        Args:
            business_plan: Business plan content
            
        Returns:
            Business plan review and recommendations
        """
        query = f"Review this business plan and provide feedback:\n\n{business_plan}"
        return await self.process_query(query)
