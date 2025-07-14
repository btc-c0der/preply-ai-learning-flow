"""
AI Engineering Learning Roadmap Data Model

This module defines the data structures for the AI learning roadmap.
Following SOLID principles with clear separation of concerns.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class NodeType(Enum):
    """Types of nodes in the learning roadmap."""
    START = "start"
    TOPIC = "topic"
    END = "end"


@dataclass
class LearningNode:
    """
    Represents a single node in the learning roadmap.
    
    Single Responsibility: Holds node data only.
    """
    id: str
    title: str
    description: str
    node_type: NodeType
    subtopics: List[str]
    prerequisites: List[str]
    estimated_hours: int
    resources: List[str]
    
    def __post_init__(self):
        """Validate node data after initialization."""
        if not self.id:
            raise ValueError("Node ID cannot be empty")
        if not self.title:
            raise ValueError("Node title cannot be empty")
