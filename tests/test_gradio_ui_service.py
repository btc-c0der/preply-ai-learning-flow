"""
Tests for GradioUIService.
Following TDD principles - RED phase.
"""

import pytest
from src.models.learning_node import LearningNode, NodeType
from src.repositories.roadmap_repository import RoadmapRepository
from src.services.roadmap_service import RoadmapService
from src.ui.gradio_ui_service import GradioUIService


class TestGradioUIService:
    """Test cases for GradioUIService class."""
    
    def test_create_ui_service(self):
        """Test creating a UI service."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        roadmap_service = RoadmapService(repo)
        ui_service = GradioUIService(roadmap_service)
        assert ui_service is not None
    
    def test_format_node_display(self):
        """Test formatting a node for display."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        roadmap_service = RoadmapService(repo)
        ui_service = GradioUIService(roadmap_service)
        
        node = LearningNode(
            id="test-node",
            title="Test Node",
            description="Test description",
            node_type=NodeType.TOPIC,
            subtopics=["subtopic1", "subtopic2"],
            prerequisites=["prereq1"],
            estimated_hours=10,
            resources=["https://example.com"]
        )
        
        formatted = ui_service.format_node_display(node)
        assert "Test Node" in formatted
        assert "10 hours" in formatted
        assert "subtopic1" in formatted
        assert "https://example.com" in formatted
    
    def test_create_roadmap_overview_display(self):
        """Test creating roadmap overview display."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        roadmap_service = RoadmapService(repo)
        ui_service = GradioUIService(roadmap_service)
        
        overview_html = ui_service.create_roadmap_overview_display()
        assert "AI Engineering Learning Roadmap" in overview_html
        assert "Total Topics" in overview_html
        assert "Estimated Hours" in overview_html
    
    def test_create_learning_path_display(self):
        """Test creating learning path display."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        roadmap_service = RoadmapService(repo)
        ui_service = GradioUIService(roadmap_service)
        
        path_html = ui_service.create_learning_path_display("ai-engineer")
        assert "Learning Path" in path_html
        assert "Start" in path_html  # Should contain the start node
    
    def test_create_progress_tracker_display(self):
        """Test creating progress tracker display."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        roadmap_service = RoadmapService(repo)
        ui_service = GradioUIService(roadmap_service)
        
        completed_topics = ["start", "llm-apis"]
        progress_html = ui_service.create_progress_tracker_display(completed_topics)
        assert "Progress Tracker" in progress_html
        assert "Completed" in progress_html
        assert "Next Recommended" in progress_html
    
    def test_get_topic_choices(self):
        """Test getting topic choices for dropdowns."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        roadmap_service = RoadmapService(repo)
        ui_service = GradioUIService(roadmap_service)
        
        choices = ui_service.get_topic_choices()
        assert len(choices) > 0
        assert isinstance(choices, list)
        # Should contain tuples of (display_name, node_id)
        assert all(isinstance(choice, tuple) and len(choice) == 2 for choice in choices)
