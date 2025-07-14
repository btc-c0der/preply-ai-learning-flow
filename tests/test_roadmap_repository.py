"""
Tests for RoadmapRepository.
Following TDD principles - RED phase.
"""

import pytest
from src.models.learning_node import LearningNode, NodeType
from src.repositories.roadmap_repository import RoadmapRepository


class TestRoadmapRepository:
    """Test cases for RoadmapRepository class."""
    
    def test_create_empty_repository(self):
        """Test creating an empty repository."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        assert len(repo.get_all_nodes()) == 0
    
    def test_add_node_to_repository(self):
        """Test adding a node to the repository."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        node = LearningNode(
            id="test-node",
            title="Test Node",
            description="Test description",
            node_type=NodeType.TOPIC,
            subtopics=["subtopic1"],
            prerequisites=[],
            estimated_hours=10,
            resources=[]
        )
        
        repo.add_node(node)
        nodes = repo.get_all_nodes()
        assert len(nodes) == 1
        assert nodes[0].id == "test-node"
    
    def test_get_node_by_id(self):
        """Test retrieving a node by its ID."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        node = LearningNode(
            id="test-node",
            title="Test Node",
            description="Test description",
            node_type=NodeType.TOPIC,
            subtopics=[],
            prerequisites=[],
            estimated_hours=10,
            resources=[]
        )
        
        repo.add_node(node)
        retrieved_node = repo.get_node_by_id("test-node")
        assert retrieved_node is not None
        assert retrieved_node.id == "test-node"
    
    def test_get_nonexistent_node_returns_none(self):
        """Test that getting a non-existent node returns None."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        node = repo.get_node_by_id("nonexistent")
        assert node is None
        
    def test_load_default_roadmap(self):
        """Test loading the default AI engineering roadmap."""
        # RED: This test should fail initially
        repo = RoadmapRepository()
        repo.load_default_roadmap()
        nodes = repo.get_all_nodes()
        assert len(nodes) > 0
        
        # Check that we have the start node
        start_node = repo.get_node_by_id("start")
        assert start_node is not None
        assert start_node.node_type == NodeType.START
