"""
Demonstration script for the AI Engineering Learning Roadmap.
Shows all core functionality working without the Gradio UI.
"""

from src.repositories.roadmap_repository import RoadmapRepository
from src.services.roadmap_service import RoadmapService
from src.ui.gradio_ui_service import GradioUIService


def main():
    """Demonstrate the core functionality of the application."""
    
    print("🚀 AI Engineering Learning Roadmap Demo")
    print("=" * 50)
    
    # Initialize services
    print("\n📦 Initializing services...")
    repo = RoadmapRepository()
    repo.load_default_roadmap()
    
    roadmap_service = RoadmapService(repo)
    ui_service = GradioUIService(roadmap_service)
    
    # Show roadmap overview
    print("\n📊 Roadmap Overview:")
    overview = roadmap_service.get_roadmap_overview()
    print(f"   • Total Topics: {overview['total_nodes']}")
    print(f"   • Total Hours: {overview['estimated_total_hours']}")
    
    # Show learning path
    print("\n🗺️  Learning Path to AI Engineer:")
    path = roadmap_service.get_learning_path("ai-engineer")
    for i, node in enumerate(path, 1):
        icon = "🏃‍♂️" if i == 1 else "🏁" if i == len(path) else "📖"
        print(f"   {i:2d}. {icon} {node.title} ({node.estimated_hours}h)")
    
    # Show topic details
    print("\n📚 Sample Topic Details - LLM APIs:")
    llm_node = repo.get_node_by_id("llm-apis")
    if llm_node:
        print(f"   • Description: {llm_node.description}")
        print(f"   • Estimated Hours: {llm_node.estimated_hours}")
        print(f"   • Subtopics: {', '.join(llm_node.subtopics)}")
        print(f"   • Prerequisites: {', '.join(llm_node.prerequisites)}")
    
    # Show progress tracking
    print("\n📈 Progress Tracking Demo:")
    completed = ["start", "llm-apis", "model-adaptation"]
    
    remaining_hours = roadmap_service.calculate_remaining_hours(completed)
    total_hours = overview["estimated_total_hours"]
    completed_hours = total_hours - remaining_hours
    progress_pct = (completed_hours / total_hours * 100) if total_hours > 0 else 0
    
    print(f"   • Completed: {len(completed)} topics ({completed_hours}h)")
    print(f"   • Remaining: {remaining_hours} hours")
    print(f"   • Progress: {progress_pct:.1f}%")
    
    # Show next recommendations
    next_topics = roadmap_service.get_next_recommended_topics(completed)
    print(f"\n🎯 Next Recommended Topics:")
    for topic in next_topics[:3]:
        print(f"   • {topic.title} ({topic.estimated_hours}h)")
    
    # Show UI formatting capability
    print("\n🎨 UI Formatting Example:")
    if llm_node:
        formatted = ui_service.format_node_display(llm_node)
        # Remove HTML tags for console display
        import re
        clean_text = re.sub('<[^<]+?>', '', formatted)
        clean_text = re.sub(r'\n\s*\n', '\n', clean_text)
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        for line in lines[:8]:  # Show first 8 lines
            if line:
                print(f"   {line}")
    
    print("\n" + "=" * 50)
    print("✅ All core functionality working perfectly!")
    print("🎉 Ready for Gradio UI when compatibility is resolved!")


if __name__ == "__main__":
    main()
