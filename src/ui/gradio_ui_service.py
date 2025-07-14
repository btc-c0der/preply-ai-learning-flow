"""
UI Service for Gradio interface.
Following SOLID principles with clear separation of concerns.
"""

from typing import List, Tuple
from src.models.learning_node import LearningNode, NodeType
from src.services.roadmap_service import RoadmapService


class GradioUIService:
    """
    Service for handling Gradio UI logic.
    
    Single Responsibility: Handles UI formatting and display logic.
    Dependency Inversion: Depends on RoadmapService abstraction.
    """
    
    def __init__(self, roadmap_service: RoadmapService):
        """
        Initialize the UI service.
        
        Args:
            roadmap_service: The roadmap service to use
        """
        self._roadmap_service = roadmap_service
    
    def format_node_display(self, node: LearningNode) -> str:
        """
        Format a learning node for display.
        
        Args:
            node: The learning node to format
            
        Returns:
            HTML-formatted string for display
        """
        subtopics_html = ""
        if node.subtopics:
            subtopics_list = "\n".join(f"• {topic}" for topic in node.subtopics)
            subtopics_html = f"""
            <div class="subtopics">
                <h4>📚 Topics Covered:</h4>
                <pre>{subtopics_list}</pre>
            </div>
            """
        
        resources_html = ""
        if node.resources:
            resources_list = "\n".join(f"• <a href='{resource}' target='_blank'>{resource}</a>" for resource in node.resources)
            resources_html = f"""
            <div class="resources">
                <h4>🔗 Resources:</h4>
                <div>{resources_list}</div>
            </div>
            """
        
        return f"""
        <div class="node-display">
            <h3>🎯 {node.title}</h3>
            <p><strong>Description:</strong> {node.description}</p>
            <p><strong>⏱️ Estimated Time:</strong> {node.estimated_hours} hours</p>
            {subtopics_html}
            {resources_html}
        </div>
        """
    
    def create_roadmap_overview_display(self) -> str:
        """
        Create the roadmap overview display.
        
        Returns:
            HTML-formatted overview
        """
        overview = self._roadmap_service.get_roadmap_overview()
        
        return f"""
        <div class="roadmap-overview">
            <h1>🚀 AI Engineering Learning Roadmap</h1>
            <div class="stats">
                <div class="stat-card">
                    <h3>📊 Total Topics</h3>
                    <p class="stat-number">{overview['total_nodes']}</p>
                </div>
                <div class="stat-card">
                    <h3>⏰ Estimated Hours</h3>
                    <p class="stat-number">{overview['estimated_total_hours']}</p>
                </div>
            </div>
            <p>Welcome to your comprehensive AI Engineering learning journey! This roadmap will guide you through all the essential topics to become a skilled AI Engineer.</p>
        </div>
        <style>
        .roadmap-overview {{
            text-align: center;
            padding: 20px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f0f0f0;
            padding: 15px;
            border-radius: 8px;
            min-width: 150px;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #007acc;
        }}
        .node-display {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .subtopics, .resources {{
            margin-top: 15px;
        }}
        .progress-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            margin: 10px 0;
        }}
        .progress-fill {{
            background: #007acc;
            height: 100%;
            transition: width 0.3s ease;
        }}
        </style>
        """
    
    def create_learning_path_display(self, target_node_id: str) -> str:
        """
        Create learning path display for a target node.
        
        Args:
            target_node_id: The target node ID
            
        Returns:
            HTML-formatted learning path
        """
        path = self._roadmap_service.get_learning_path(target_node_id)
        
        if not path:
            return "<p>❌ No learning path found for the specified target.</p>"
        
        path_html = "<h2>🗺️ Learning Path</h2>"
        
        for i, node in enumerate(path):
            icon = "🏁" if node.node_type == NodeType.END else "🏃‍♂️" if node.node_type == NodeType.START else "📖"
            arrow = " → " if i < len(path) - 1 else ""
            
            path_html += f"""
            <div class="path-step">
                <span class="step-number">{i + 1}</span>
                <span class="step-icon">{icon}</span>
                <span class="step-title">{node.title}</span>
                <span class="step-hours">({node.estimated_hours}h)</span>
                {arrow}
            </div>
            """
        
        total_hours = sum(node.estimated_hours for node in path)
        path_html += f"<p><strong>📊 Total Estimated Time: {total_hours} hours</strong></p>"
        
        return path_html
    
    def create_progress_tracker_display(self, completed_topics: List[str]) -> str:
        """
        Create progress tracker display.
        
        Args:
            completed_topics: List of completed topic IDs
            
        Returns:
            HTML-formatted progress tracker
        """
        overview = self._roadmap_service.get_roadmap_overview()
        remaining_hours = self._roadmap_service.calculate_remaining_hours(completed_topics)
        total_hours = overview["estimated_total_hours"]
        completed_hours = total_hours - remaining_hours
        progress_percentage = (completed_hours / total_hours * 100) if total_hours > 0 else 0
        
        next_topics = self._roadmap_service.get_next_recommended_topics(completed_topics)
        
        progress_html = f"""
        <div class="progress-tracker">
            <h2>📈 Progress Tracker</h2>
            
            <div class="progress-section">
                <h3>✅ Completed: {len(completed_topics)} topics ({completed_hours} hours)</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percentage:.1f}%"></div>
                </div>
                <p>{progress_percentage:.1f}% Complete</p>
            </div>
            
            <div class="remaining-section">
                <h3>⏳ Remaining: {remaining_hours} hours</h3>
            </div>
        """
        
        if next_topics:
            progress_html += "<div class='next-topics'><h3>🎯 Next Recommended Topics:</h3>"
            for topic in next_topics[:3]:  # Show top 3 recommendations
                progress_html += f"<div class='topic-recommendation'>• {topic.title} ({topic.estimated_hours}h)</div>"
            progress_html += "</div>"
        else:
            progress_html += "<div class='next-topics'><h3>🎉 Congratulations! No more topics available.</h3></div>"
        
        progress_html += "</div>"
        return progress_html
    
    def get_topic_choices(self) -> List[Tuple[str, str]]:
        """
        Get topic choices for dropdowns.
        
        Returns:
            List of (display_name, node_id) tuples
        """
        repo_nodes = self._roadmap_service._repository.get_all_nodes()
        choices = []
        
        for node in repo_nodes:
            if node.node_type == NodeType.TOPIC:
                display_name = f"{node.title} ({node.estimated_hours}h)"
                choices.append((display_name, node.id))
        
        return sorted(choices, key=lambda x: x[0])
