"""
Repository for managing learning roadmap data.
Following SOLID principles with clear separation of concerns.
"""

from typing import List, Optional, Dict
from src.models.learning_node import LearningNode, NodeType


class RoadmapRepository:
    """
    Repository for managing learning nodes.
    
    Single Responsibility: Manages data storage and retrieval for learning nodes.
    Open/Closed: Can be extended for different storage backends.
    """
    
    def __init__(self):
        """Initialize an empty repository."""
        self._nodes: Dict[str, LearningNode] = {}
    
    def add_node(self, node: LearningNode) -> None:
        """
        Add a node to the repository.
        
        Args:
            node: The learning node to add
        """
        self._nodes[node.id] = node
    
    def get_node_by_id(self, node_id: str) -> Optional[LearningNode]:
        """
        Get a node by its ID.
        
        Args:
            node_id: The ID of the node to retrieve
            
        Returns:
            The node if found, None otherwise
        """
        return self._nodes.get(node_id)
    
    def get_all_nodes(self) -> List[LearningNode]:
        """
        Get all nodes in the repository.
        
        Returns:
            List of all learning nodes
        """
        return list(self._nodes.values())
    
    def load_default_roadmap(self) -> None:
        """Load the default AI engineering roadmap."""
        # Start node
        start_node = LearningNode(
            id="start",
            title="Start",
            description="Beginning of the AI Engineering journey",
            node_type=NodeType.START,
            subtopics=[],
            prerequisites=[],
            estimated_hours=0,
            resources=[]
        )
        self.add_node(start_node)
        
        # LLM APIs node
        llm_apis_node = LearningNode(
            id="llm-apis",
            title="LLM APIs",
            description="Understanding different types of LLMs and their APIs",
            node_type=NodeType.TOPIC,
            subtopics=["Types of LLMs", "Structured Outputs", "Prompt Caching", "Multi-modal models"],
            prerequisites=["start"],
            estimated_hours=20,
            resources=["https://platform.openai.com/docs", "https://docs.anthropic.com/claude/docs"]
        )
        self.add_node(llm_apis_node)
        
        # Model Adaptation node
        model_adaptation_node = LearningNode(
            id="model-adaptation",
            title="Model Adaptation",
            description="Techniques for adapting models to specific use cases",
            node_type=NodeType.TOPIC,
            subtopics=["Prompt Engineering", "Tool Use", "Finetuning"],
            prerequisites=["llm-apis"],
            estimated_hours=30,
            resources=["https://arxiv.org/abs/2005.14165", "https://huggingface.co/docs/transformers/training"]
        )
        self.add_node(model_adaptation_node)
        
        # Storage for Retrieval node
        storage_node = LearningNode(
            id="storage-retrieval",
            title="Storage for Retrieval",
            description="Database solutions for AI applications",
            node_type=NodeType.TOPIC,
            subtopics=["Vector Databases", "Graph Databases", "Hybrid retrieval"],
            prerequisites=["llm-apis"],
            estimated_hours=25,
            resources=["https://weaviate.io/developers/weaviate", "https://neo4j.com/docs/"]
        )
        self.add_node(storage_node)
        
        # Infrastructure node
        infrastructure_node = LearningNode(
            id="infrastructure",
            title="Infrastructure",
            description="Deployment and scaling of AI applications",
            node_type=NodeType.TOPIC,
            subtopics=["Kubernetes", "Cloud Services", "CI/CD", "Model Routing", "LLM deployment"],
            prerequisites=["model-adaptation", "storage-retrieval"],
            estimated_hours=40,
            resources=["https://kubernetes.io/docs/", "https://aws.amazon.com/sagemaker/"]
        )
        self.add_node(infrastructure_node)
        
        # AI Agents node
        ai_agents_node = LearningNode(
            id="ai-agents",
            title="AI Agents",
            description="Building intelligent autonomous agents",
            node_type=NodeType.TOPIC,
            subtopics=["AI Agent Design Patterns", "Multi-agent systems", "Memory + Tools", "Planning", "Finetuning", "ABL, AL, etc."],
            prerequisites=["model-adaptation", "storage-retrieval"],
            estimated_hours=50,
            resources=["https://github.com/microsoft/autogen", "https://langchain.com/"]
        )
        self.add_node(ai_agents_node)
        
        # RAG & Agentic RAG node
        rag_node = LearningNode(
            id="rag-agentic",
            title="RAG & Agentic RAG",
            description="Retrieval-Augmented Generation and agentic approaches",
            node_type=NodeType.TOPIC,
            subtopics=["Data retrieval and generation", "Vector + Graph", "MCP", "LLM Orchestration Frameworks"],
            prerequisites=["ai-agents", "storage-retrieval"],
            estimated_hours=35,
            resources=["https://arxiv.org/abs/2005.11401", "https://github.com/langchain-ai/langchain"]
        )
        self.add_node(rag_node)
        
        # Observability & Evaluation node
        observability_node = LearningNode(
            id="observability-evaluation",
            title="Observability & Evaluation",
            description="Monitoring and evaluating AI systems",
            node_type=NodeType.TOPIC,
            subtopics=["AI Agent instrumentation", "Observability platforms", "Evaluation techniques", "AI Agent Evaluation"],
            prerequisites=["ai-agents", "rag-agentic"],
            estimated_hours=30,
            resources=["https://weights-and-biases.github.io/", "https://docs.wandb.ai/"]
        )
        self.add_node(observability_node)
        
        # Security node
        security_node = LearningNode(
            id="security",
            title="Security",
            description="Security considerations for AI applications",
            node_type=NodeType.TOPIC,
            subtopics=["Guardrails", "Testing LLM-based applications", "Secure orchestration"],
            prerequisites=["infrastructure", "observability-evaluation"],
            estimated_hours=25,
            resources=["https://owasp.org/www-project-ai-security-and-privacy-guide/"]
        )
        self.add_node(security_node)
        
        # Forward looking elements node
        forward_looking_node = LearningNode(
            id="forward-looking",
            title="Forward looking elements",
            description="Emerging trends and future technologies",
            node_type=NodeType.TOPIC,
            subtopics=["Voice and Vision Agents", "Auto Agents", "Automated Prompt Engineering"],
            prerequisites=["security", "observability-evaluation"],
            estimated_hours=20,
            resources=["https://arxiv.org/abs/2310.12397"]
        )
        self.add_node(forward_looking_node)
        
        # End node
        end_node = LearningNode(
            id="ai-engineer",
            title="AI Engineer",
            description="Congratulations! You've completed the AI Engineering roadmap",
            node_type=NodeType.END,
            subtopics=[],
            prerequisites=["forward-looking"],
            estimated_hours=0,
            resources=[]
        )
        self.add_node(end_node)
