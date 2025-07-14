"""
Tests for LearningNode model.
Following TDD principles - RED phase.
"""

import pytest
from src.models.learning_node import LearningNode, NodeType


class TestLearningNode:
    """Test cases for LearningNode class."""
    
    def test_create_valid_learning_node(self):
        """Test creating a valid learning node."""
        # RED: This test should pass after implementation
        node = LearningNode(
            id="llm-apis",
            title="LLM APIs",
            description="Understanding different types of LLMs and their APIs",
            node_type=NodeType.TOPIC,
            subtopics=["Types of LLMs", "Structured Outputs", "Prompt Caching", "Multi-modal models"],
            prerequisites=["basic-programming"],
            estimated_hours=20,
            resources=["https://example.com/llm-guide"]
        )
        
        assert node.id == "llm-apis"
        assert node.title == "LLM APIs"
        assert node.node_type == NodeType.TOPIC
        assert len(node.subtopics) == 4
        assert node.estimated_hours == 20
    
    def test_empty_id_raises_error(self):
        """Test that empty ID raises ValueError."""
        # RED: This test should fail initially
        with pytest.raises(ValueError, match="Node ID cannot be empty"):
            LearningNode(
                id="",
                title="Test Node",
                description="Test description",
                node_type=NodeType.TOPIC,
                subtopics=[],
                prerequisites=[],
                estimated_hours=10,
                resources=[]
            )
    
    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        # RED: This test should fail initially
        with pytest.raises(ValueError, match="Node title cannot be empty"):
            LearningNode(
                id="test-id",
                title="",
                description="Test description",
                node_type=NodeType.TOPIC,
                subtopics=[],
                prerequisites=[],
                estimated_hours=10,
                resources=[]
            )
