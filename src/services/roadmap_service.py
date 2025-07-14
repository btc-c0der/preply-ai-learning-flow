"""
Service layer for roadmap business logic.
Following SOLID principles with clear separation of concerns.
"""

from typing import List, Dict, Set
from src.models.learning_node import LearningNode, NodeType
from src.repositories.roadmap_repository import RoadmapRepository


class RoadmapService:
    """
    Service for handling roadmap business logic.
    
    Single Responsibility: Handles business logic for roadmap operations.
    Dependency Inversion: Depends on RoadmapRepository abstraction.
    """
    
    def __init__(self, repository: RoadmapRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository: The roadmap repository to use
        """
        self._repository = repository
    
    def get_roadmap_overview(self) -> Dict[str, int]:
        """
        Get an overview of the roadmap.
        
        Returns:
            Dictionary with roadmap statistics
        """
        nodes = self._repository.get_all_nodes()
        total_hours = sum(node.estimated_hours for node in nodes)
        
        return {
            "total_nodes": len(nodes),
            "estimated_total_hours": total_hours
        }
    
    def get_learning_path(self, target_node_id: str) -> List[LearningNode]:
        """
        Get the learning path from start to a target node.
        
        Args:
            target_node_id: The ID of the target node
            
        Returns:
            List of nodes representing the learning path
        """
        target_node = self._repository.get_node_by_id(target_node_id)
        if not target_node:
            return []
        
        # Build path using topological sort based on prerequisites
        path = []
        visited = set()
        
        def build_path(node_id: str):
            if node_id in visited:
                return
            
            node = self._repository.get_node_by_id(node_id)
            if not node:
                return
            
            visited.add(node_id)
            
            # Add prerequisites first
            for prereq_id in node.prerequisites:
                build_path(prereq_id)
            
            path.append(node)
        
        build_path(target_node_id)
        return path
    
    def get_prerequisites(self, node_id: str) -> List[LearningNode]:
        """
        Get all prerequisites for a specific node.
        
        Args:
            node_id: The ID of the node
            
        Returns:
            List of prerequisite nodes
        """
        node = self._repository.get_node_by_id(node_id)
        if not node:
            return []
        
        prerequisites = []
        for prereq_id in node.prerequisites:
            prereq_node = self._repository.get_node_by_id(prereq_id)
            if prereq_node:
                prerequisites.append(prereq_node)
        
        return prerequisites
    
    def get_next_recommended_topics(self, completed_topics: List[str]) -> List[LearningNode]:
        """
        Get next recommended topics based on completed prerequisites.
        
        Args:
            completed_topics: List of completed topic IDs
            
        Returns:
            List of recommended next topics
        """
        completed_set = set(completed_topics)
        all_nodes = self._repository.get_all_nodes()
        recommended = []
        
        for node in all_nodes:
            # Skip if already completed
            if node.id in completed_set:
                continue
            
            # Skip start and end nodes
            if node.node_type in [NodeType.START, NodeType.END]:
                continue
            
            # Check if all prerequisites are met
            prerequisites_met = all(
                prereq_id in completed_set
                for prereq_id in node.prerequisites
            )
            
            if prerequisites_met:
                recommended.append(node)
        
        return recommended
    
    def calculate_remaining_hours(self, completed_topics: List[str]) -> int:
        """
        Calculate remaining hours for incomplete topics.
        
        Args:
            completed_topics: List of completed topic IDs
            
        Returns:
            Total remaining hours
        """
        completed_set = set(completed_topics)
        all_nodes = self._repository.get_all_nodes()
        
        remaining_hours = 0
        for node in all_nodes:
            if node.id not in completed_set:
                remaining_hours += node.estimated_hours
        
        return remaining_hours
