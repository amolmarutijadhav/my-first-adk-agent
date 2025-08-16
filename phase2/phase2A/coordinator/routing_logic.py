"""
Intelligent routing logic for Phase 2A: Modular ADK Architecture.

This module provides intelligent routing logic to determine which agent(s)
should handle a given query based on content analysis and agent capabilities.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import structlog

from config.settings import get_settings
from config.logging_config import get_logger


class QueryType(Enum):
    """Types of queries that can be routed."""
    TECHNICAL = "technical"
    CREATIVE = "creative"
    BUSINESS = "business"
    GENERAL = "general"
    COLLABORATION = "collaboration"


@dataclass
class RoutingDecision:
    """Represents a routing decision for a query."""
    primary_agent: str
    secondary_agents: List[str]
    confidence: float
    query_type: QueryType
    reasoning: str


class RoutingLogic:
    """
    Intelligent routing logic for query distribution.
    
    This class analyzes queries and determines the best agent(s) to handle them
    based on content analysis, keyword matching, and agent capabilities.
    """
    
    def __init__(self):
        """Initialize the routing logic."""
        self.logger = get_logger("routing_logic")
        self.settings = get_settings()
        
        # Define keyword patterns for each agent type
        self.tech_keywords = [
            r'\b(?:python|javascript|java|c\+\+|go|rust|typescript|react|angular|vue|django|flask|fastapi)\b',
            r'\b(?:debug|code|programming|development|software|api|database|sql|nosql|docker|kubernetes)\b',
            r'\b(?:error|bug|issue|problem|fix|optimize|performance|security|testing|deployment)\b',
            r'\b(?:algorithm|data structure|design pattern|architecture|framework|library|package)\b',
            r'\b(?:git|version control|ci/cd|devops|cloud|aws|gcp|azure|server|client)\b'
        ]
        
        self.creative_keywords = [
            r'\b(?:story|creative|writing|art|design|brainstorm|idea|concept|character|plot|narrative)\b',
            r'\b(?:poem|poetry|script|screenplay|novel|fiction|creative writing|content|copy)\b',
            r'\b(?:inspiration|imagination|artistic|visual|brand|marketing|advertising|social media)\b',
            r'\b(?:mood board|design thinking|user experience|portfolio|collaboration|innovation)\b',
            r'\b(?:storytelling|narrative|character development|world building|creative process)\b'
        ]
        
        self.business_keywords = [
            r'\b(?:business|strategy|market|financial|investment|revenue|profit|cost|budget|planning)\b',
            r'\b(?:company|startup|enterprise|corporate|management|leadership|career|professional)\b',
            r'\b(?:analysis|research|competitive|industry|trend|opportunity|risk|compliance)\b',
            r'\b(?:sales|marketing|customer|product|service|operations|efficiency|optimization)\b',
            r'\b(?:funding|capital|investment|portfolio|roi|kpi|performance|growth|scaling)\b'
        ]
        
        self.general_keywords = [
            r'\b(?:hello|hi|greeting|welcome|help|assist|guide|explain|overview|introduction)\b',
            r'\b(?:how to|what is|when|where|why|who|which|general|basic|simple)\b',
            r'\b(?:thank|thanks|appreciate|good|great|nice|wonderful|excellent|awesome)\b',
            r'\b(?:question|query|information|knowledge|fact|tip|advice|suggestion)\b'
        ]
        
        # Compile regex patterns
        self.tech_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.tech_keywords]
        self.creative_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.creative_keywords]
        self.business_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.business_keywords]
        self.general_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.general_keywords]
    
    def analyze_query(self, query: str) -> RoutingDecision:
        """
        Analyze a query and determine the best routing decision.
        
        Args:
            query: User query to analyze
            
        Returns:
            Routing decision with agent recommendations
        """
        self.logger.info("Analyzing query for routing", query=query)
        
        # Calculate scores for each agent type
        tech_score = self._calculate_tech_score(query)
        creative_score = self._calculate_creative_score(query)
        business_score = self._calculate_business_score(query)
        general_score = self._calculate_general_score(query)
        
        # Determine query type and primary agent
        scores = {
            "tech_agent": tech_score,
            "creative_agent": creative_score,
            "business_agent": business_score,
            "hello_agent": general_score
        }
        
        # Find the highest scoring agent
        primary_agent = max(scores, key=scores.get)
        max_score = scores[primary_agent]
        
        # Determine if collaboration is needed
        secondary_agents = self._determine_secondary_agents(scores, max_score)
        query_type = self._determine_query_type(scores, max_score)
        
        # Calculate confidence
        confidence = self._calculate_confidence(scores, max_score)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(scores, primary_agent, secondary_agents)
        
        decision = RoutingDecision(
            primary_agent=primary_agent,
            secondary_agents=secondary_agents,
            confidence=confidence,
            query_type=query_type,
            reasoning=reasoning
        )
        
        self.logger.info(
            "Routing decision made",
            primary_agent=primary_agent,
            secondary_agents=secondary_agents,
            confidence=confidence,
            query_type=query_type.value,
            reasoning=reasoning
        )
        
        return decision
    
    def _calculate_tech_score(self, query: str) -> float:
        """Calculate technical relevance score."""
        score = 0.0
        for pattern in self.tech_patterns:
            matches = pattern.findall(query)
            score += len(matches) * 0.5
        
        # Bonus for technical question words
        tech_question_words = ["how to", "debug", "fix", "implement", "optimize", "deploy"]
        for word in tech_question_words:
            if word.lower() in query.lower():
                score += 1.0
        
        return min(score, 10.0)  # Cap at 10.0
    
    def _calculate_creative_score(self, query: str) -> float:
        """Calculate creative relevance score."""
        score = 0.0
        for pattern in self.creative_patterns:
            matches = pattern.findall(query)
            score += len(matches) * 0.5
        
        # Bonus for creative question words
        creative_question_words = ["create", "design", "write", "brainstorm", "develop", "imagine"]
        for word in creative_question_words:
            if word.lower() in query.lower():
                score += 1.0
        
        return min(score, 10.0)
    
    def _calculate_business_score(self, query: str) -> float:
        """Calculate business relevance score."""
        score = 0.0
        for pattern in self.business_patterns:
            matches = pattern.findall(query)
            score += len(matches) * 0.5
        
        # Bonus for business question words
        business_question_words = ["strategy", "market", "financial", "business", "career", "investment"]
        for word in business_question_words:
            if word.lower() in query.lower():
                score += 1.0
        
        return min(score, 10.0)
    
    def _calculate_general_score(self, query: str) -> float:
        """Calculate general relevance score."""
        score = 0.0
        for pattern in self.general_patterns:
            matches = pattern.findall(query)
            score += len(matches) * 0.3
        
        # Bonus for general question words
        general_question_words = ["hello", "hi", "help", "what", "how", "when", "where", "why"]
        for word in general_question_words:
            if word.lower() in query.lower():
                score += 0.5
        
        return min(score, 10.0)
    
    def _determine_secondary_agents(self, scores: Dict[str, float], max_score: float) -> List[str]:
        """Determine secondary agents for collaboration."""
        secondary_agents = []
        threshold = max_score * 0.7  # 70% of max score
        
        for agent, score in scores.items():
            if score >= threshold and score < max_score:
                secondary_agents.append(agent)
        
        return secondary_agents
    
    def _determine_query_type(self, scores: Dict[str, float], max_score: float) -> QueryType:
        """Determine the type of query based on scores."""
        # Check if multiple agents have high scores (collaboration needed)
        high_score_count = sum(1 for score in scores.values() if score >= max_score * 0.8)
        
        if high_score_count > 1:
            return QueryType.COLLABORATION
        
        # Determine primary type
        if scores["tech_agent"] == max_score:
            return QueryType.TECHNICAL
        elif scores["creative_agent"] == max_score:
            return QueryType.CREATIVE
        elif scores["business_agent"] == max_score:
            return QueryType.BUSINESS
        else:
            return QueryType.GENERAL
    
    def _calculate_confidence(self, scores: Dict[str, float], max_score: float) -> float:
        """Calculate confidence in the routing decision."""
        if max_score == 0:
            return 0.0
        
        # Calculate how much the max score dominates
        total_score = sum(scores.values())
        dominance = max_score / total_score if total_score > 0 else 0
        
        # Normalize to 0-1 range
        confidence = min(dominance * 2, 1.0)
        
        return confidence
    
    def _generate_reasoning(self, scores: Dict[str, float], primary_agent: str, secondary_agents: List[str]) -> str:
        """Generate reasoning for the routing decision."""
        reasoning_parts = []
        
        # Primary agent reasoning
        primary_score = scores[primary_agent]
        reasoning_parts.append(f"Primary agent '{primary_agent}' selected with score {primary_score:.2f}")
        
        # Secondary agents reasoning
        if secondary_agents:
            secondary_reasons = []
            for agent in secondary_agents:
                score = scores[agent]
                secondary_reasons.append(f"'{agent}' (score: {score:.2f})")
            reasoning_parts.append(f"Secondary agents for collaboration: {', '.join(secondary_reasons)}")
        
        # Score distribution
        score_distribution = [f"{agent}: {score:.2f}" for agent, score in scores.items()]
        reasoning_parts.append(f"Score distribution: {', '.join(score_distribution)}")
        
        return "; ".join(reasoning_parts)
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all available agents."""
        return {
            "tech_agent": [
                "Programming and code assistance",
                "Debugging and troubleshooting",
                "Software architecture and design",
                "API development and integration",
                "DevOps and CI/CD"
            ],
            "creative_agent": [
                "Creative writing and storytelling",
                "Brainstorming and ideation",
                "Content creation and marketing",
                "Artistic direction and design",
                "Creative problem solving"
            ],
            "business_agent": [
                "Business strategy and planning",
                "Market analysis and research",
                "Financial planning and analysis",
                "Professional development",
                "Career guidance and advancement"
            ],
            "hello_agent": [
                "General conversation and greetings",
                "User assistance and guidance",
                "System overview and orientation",
                "Basic information and answers",
                "Agent routing and recommendations"
            ]
        }
