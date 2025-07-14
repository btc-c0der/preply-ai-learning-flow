"""
Tests for the main Gradio application.
Following TDD principles - RED phase.
"""

import pytest
from src.repositories.roadmap_repository import RoadmapRepository
from src.services.roadmap_service import RoadmapService
from src.ui.gradio_ui_service import GradioUIService


class TestGradioApp:
    """Test cases for the main Gradio application."""
    
    def test_app_services_creation(self):
        """Test creating the app services without Gradio."""
        # Since Gradio has import issues on Python 3.13, let's test the service creation
        repository = RoadmapRepository()
        repository.load_default_roadmap()
        
        roadmap_service = RoadmapService(repository)
        ui_service = GradioUIService(roadmap_service)
        
        # Verify services are created correctly
        assert isinstance(repository, RoadmapRepository)
        assert isinstance(roadmap_service, RoadmapService)
        assert isinstance(ui_service, GradioUIService)
        
        # Test that services work together
        overview = roadmap_service.get_roadmap_overview()
        assert overview["total_nodes"] > 0
        
        overview_html = ui_service.create_roadmap_overview_display()
        assert "AI Engineering Learning Roadmap" in overview_html
