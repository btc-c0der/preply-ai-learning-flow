"""
Tests for RoadmapService.
Following TDD principles - RED phase.
"""

import pytest
from src.models.learning_node import LearningNode, NodeType
from src.repositories.roadmap_repository import RoadmapRepository
from src.services.roadmap_service import RoadmapService


class TestRoadmapService:
    """Test cases for RoadmapService class."""
    
    def test_create_service_with_repository(self):
        """Test creating a service with a repository."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        service = RoadmapService(repo)
        assert service is not None
    
    def test_get_roadmap_overview(self):
        """Test getting a roadmap overview."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        service = RoadmapService(repo)
        
        overview = service.get_roadmap_overview()
        assert "total_nodes" in overview
        assert "estimated_total_hours" in overview
        assert overview["total_nodes"] > 0
        assert overview["estimated_total_hours"] > 0
    
    def test_get_learning_path(self):
        """Test getting a learning path from start to a target node."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        service = RoadmapService(repo)
        
        path = service.get_learning_path("ai-engineer")
        assert len(path) > 0
        assert path[0].id == "start"
        assert path[-1].id == "ai-engineer"
    
    def test_get_prerequisites_for_node(self):
        """Test getting prerequisites for a specific node."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        service = RoadmapService(repo)
        
        prerequisites = service.get_prerequisites("infrastructure")
        assert len(prerequisites) > 0
        # Infrastructure should have model-adaptation and storage-retrieval as prerequisites
        prereq_ids = [node.id for node in prerequisites]
        assert "model-adaptation" in prereq_ids
        assert "storage-retrieval" in prereq_ids
    
    def test_get_next_recommended_topics(self):
        """Test getting next recommended topics after completing certain prerequisites."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        service = RoadmapService(repo)
        
        completed_topics = ["start", "llm-apis"]
        next_topics = service.get_next_recommended_topics(completed_topics)
        
        assert len(next_topics) > 0
        # Should recommend topics that have their prerequisites met
        next_ids = [node.id for node in next_topics]
        assert "model-adaptation" in next_ids
        assert "storage-retrieval" in next_ids
    
    def test_calculate_remaining_hours(self):
        """Test calculating remaining hours for incomplete topics."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        service = RoadmapService(repo)
        
        completed_topics = ["start", "llm-apis"]
        remaining_hours = service.calculate_remaining_hours(completed_topics)
        
        # Should be total hours minus the hours for completed topics
        total_hours = service.get_roadmap_overview()["estimated_total_hours"]
        llm_apis_hours = repo.get_node_by_id("llm-apis").estimated_hours
        
        expected_remaining = total_hours - llm_apis_hours  # start has 0 hours
        assert remaining_hours == expected_remaining
