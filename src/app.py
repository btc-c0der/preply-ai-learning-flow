"""
Main Gradio application for AI Engineering Learning Roadmap.
Following SOLID principles with dependency injection.
"""

import gradio as gr
import os
import sys
from typing import Dict, Any, List, Optional

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.repositories.roadmap_repository import RoadmapRepository
from src.services.roadmap_service import RoadmapService
from src.ui.gradio_ui_service import GradioUIService
from src.services.openai_service import OpenAIService
from src.services.audio_sentiment_service import AudioSentimentService
from src.services.audio_ui_service import AudioUIService


def get_app_services() -> Dict[str, Any]:
    """
    Create and configure all application services.
    
    Returns:
        Dictionary containing all configured services
    """
    # Initialize repository and load data
    repository = RoadmapRepository()
    repository.load_default_roadmap()
    
    # Initialize services
    roadmap_service = RoadmapService(repository)
    ui_service = GradioUIService(roadmap_service)
    
    # Initialize AI services if OpenAI API key is available
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_service = None
    audio_ui_service = None
    
    if openai_api_key:
        try:
            openai_service = OpenAIService(openai_api_key)
            sentiment_service = AudioSentimentService()
            audio_ui_service = AudioUIService(openai_service, sentiment_service)
        except Exception as e:
            print(f"Warning: Could not initialize AI services: {e}")
    
    return {
        "repository": repository,
        "roadmap_service": roadmap_service,
        "ui_service": ui_service,
        "openai_service": openai_service,
        "audio_ui_service": audio_ui_service
    }


def create_gradio_app():
    """
    Create and configure the Gradio application.
    
    Returns:
        Gradio Interface object
    """
    services = get_app_services()
    ui_service = services["ui_service"]
    roadmap_service = services["roadmap_service"]
    audio_ui_service = services["audio_ui_service"]
    openai_service = services["openai_service"]
    
    # State management for progress tracking
    completed_topics = []
    
    def update_progress_display():
        """Update the progress display based on completed topics."""
        return ui_service.create_progress_tracker_display(completed_topics)
    
    def add_completed_topic(topic_id: str):
        """Add a topic to the completed list."""
        if topic_id and topic_id not in completed_topics:
            completed_topics.append(topic_id)
        return update_progress_display()
    
    def remove_completed_topic(topic_id: str):
        """Remove a topic from the completed list."""
        if topic_id in completed_topics:
            completed_topics.remove(topic_id)
        return update_progress_display()
    
    def show_learning_path(target_topic: str):
        """Show the learning path for a target topic."""
        return ui_service.create_learning_path_display(target_topic)
    
    def show_topic_details(topic_id: str):
        """Show details for a specific topic."""
        node = roadmap_service._repository.get_node_by_id(topic_id)
        if node:
            return ui_service.format_node_display(node)
        return "Topic not found."
    
    def reset_progress():
        """Reset all progress."""
        completed_topics.clear()
        return update_progress_display()
    
    def process_audio_recording(audio_file):
        """Process recorded audio through the AI pipeline."""
        if not audio_ui_service:
            return (
                "❌ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.",
                "❌ Audio sentiment analysis requires OpenAI integration.",
                "❌ AI responses require OpenAI integration."
            )
        
        if audio_file is None:
            return (
                "❌ No audio recorded. Please record your question.",
                "❌ No audio to analyze.",
                "❌ No audio to process."
            )
        
        try:
            # Process audio input
            user_progress = {"completed_topics": completed_topics}
            result = audio_ui_service.process_audio_input(audio_file, user_progress)
            
            # Format results for display
            transcription_html, sentiment_html, response_html = audio_ui_service.format_audio_response(result)
            
            return transcription_html, sentiment_html, response_html
            
        except Exception as e:
            error_msg = f"Error processing audio: {str(e)}"
            return f"❌ {error_msg}", f"❌ {error_msg}", f"❌ {error_msg}"
    
    def chatbot_respond(message, history):
        """Handle chatbot conversation."""
        if not openai_service:
            bot_response = "❌ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable to use the AI assistant."
        else:
            try:
                user_progress = {"completed_topics": completed_topics}
                bot_response = audio_ui_service.create_chatbot_response(message, "", user_progress)
            except Exception as e:
                bot_response = f"❌ Error: {str(e)}"
        
        history.append([message, bot_response])
        return history, ""
    
    def get_topic_help_response(topic_id: str, question: str):
        """Get topic-specific help."""
        if not openai_service:
            return "❌ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        if not topic_id or not question:
            return "Please select a topic and ask a specific question."
        
        try:
            return audio_ui_service.get_topic_help(topic_id, question)
        except Exception as e:
            return f"❌ Error getting topic help: {str(e)}"
    
    # Get topic choices for dropdowns
    topic_choices = ui_service.get_topic_choices()
    all_topic_choices = [("Start", "start")] + topic_choices + [("AI Engineer", "ai-engineer")]
    
    # Create the Gradio interface
    with gr.Blocks(title="AI Engineering Learning Roadmap") as app:
        # Header
        gr.HTML(ui_service.create_roadmap_overview_display())
        
        # OpenAI API Key status
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        api_status = "✅ OpenAI API Key Configured" if openai_api_key else "❌ OpenAI API Key Not Set"
        gr.Markdown(f"**AI Features Status:** {api_status}")
        
        if not openai_api_key:
            gr.Markdown("""
            **🔑 To enable AI features:**
            1. Get an OpenAI API key from https://platform.openai.com/account/api-keys
            2. Set environment variable: `export OPENAI_API_KEY="your-key-here"`
            3. Restart the application
            """)
        
        with gr.Tabs():
            # Tab 1: Audio Recording & Sentiment Analysis
            with gr.Tab("🎤 Voice + Sentiment Analysis"):
                gr.Markdown("### 🎙️ Voice-Powered AI Learning with Real-Time Sentiment Analysis")
                gr.Markdown("""
                **🧠 How it works:**
                1. 🎤 **Record** your learning question or express your confusion
                2. 🗣️ **Speech-to-text** converts your voice to text using OpenAI Whisper
                3. 😊 **Sentiment analysis** identifies your emotional state from voice patterns
                4. 🤖 **AI responds** with personalized help based on your mood and question
                5. 💡 **Smart recommendations** tailored to your emotional state and learning progress
                
                **🎯 Tip:** Speak naturally and let your emotions show - the AI will adapt its response to help you better!
                """)
                
                # Audio recording section
                with gr.Row():
                    with gr.Column(scale=2):
                        audio_input = gr.Audio(
                            sources=["microphone"],
                            type="filepath",
                            label="🎙️ Record Your Learning Question (speak naturally!)",
                            interactive=True
                        )
                        
                        with gr.Row():
                            process_btn = gr.Button("🚀 Analyze Audio & Get AI Help", variant="primary")
                            clear_btn = gr.Button("🗑️ Clear Recording", variant="secondary")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        **💡 For better sentiment analysis:**
                        - Speak clearly and naturally
                        - Don't hide your emotions (confusion, excitement, stress)
                        - Ask specific questions about AI topics
                        - Mention if you're struggling or excited about a topic
                        
                        **🎭 Emotions detected:**
                        - 😄 Excited - Perfect for challenging topics
                        - 😊 Positive - Good for structured learning
                        - 😌 Calm - Ideal for detailed reading
                        - 😐 Neutral - Great for methodical progress
                        - 😰 Stressed - Suggests easier topics
                        - 😞 Negative - Recommends motivational content
                        """)
                
                # Output sections
                with gr.Row():
                    transcription_output = gr.HTML(
                        label="📝 What You Said (Speech-to-Text)"
                    )
                
                with gr.Row():
                    sentiment_output = gr.HTML(
                        label="😊 Your Emotional State Analysis"
                    )
                
                with gr.Row():
                    ai_response_output = gr.HTML(
                        label="🤖 Personalized AI Learning Response"
                    )
                
                # Event handlers
                def clear_audio_interface():
                    return None, "", "", ""
                
                process_btn.click(
                    fn=process_audio_recording,
                    inputs=[audio_input],
                    outputs=[transcription_output, sentiment_output, ai_response_output]
                )
                
                clear_btn.click(
                    fn=clear_audio_interface,
                    inputs=[],
                    outputs=[audio_input, transcription_output, sentiment_output, ai_response_output]
                )
            
            # Tab 2: AI Chatbot
            with gr.Tab("💬 AI Chatbot"):
                gr.Markdown("### Text-Based AI Learning Assistant")
                gr.Markdown("Chat with your AI learning assistant about any AI engineering topic!")
                
                chatbot = gr.Chatbot(
                    label="🤖 AI Learning Assistant",
                    height=400
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="💬 Your Message",
                        placeholder="Ask about AI engineering topics, get study advice, or request explanations...",
                        lines=2
                    )
                    send_btn = gr.Button("Send", variant="primary")
                
                msg.submit(
                    fn=chatbot_respond,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, msg]
                )
                
                send_btn.click(
                    fn=chatbot_respond,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, msg]
                )
            
            # Tab 3: Topic-Specific Help
            with gr.Tab("🎯 Topic-Specific Help"):
                gr.Markdown("### Get Targeted Help for Specific Topics")
                gr.Markdown("Select a topic and ask specific questions to get detailed, contextual assistance.")
                
                with gr.Row():
                    with gr.Column():
                        topic_select = gr.Dropdown(
                            choices=topic_choices,
                            label="📚 Select Topic",
                            interactive=True
                        )
                        
                        topic_question = gr.Textbox(
                            label="❓ Your Question",
                            placeholder="What specific aspect would you like help with?",
                            lines=3
                        )
                        
                        topic_help_btn = gr.Button("Get Help", variant="primary")
                
                topic_help_output = gr.HTML(label="💡 Topic-Specific Guidance")
                
                topic_help_btn.click(
                    fn=get_topic_help_response,
                    inputs=[topic_select, topic_question],
                    outputs=[topic_help_output]
                )
            # Tab 4: Learning Path Explorer
            with gr.Tab("🗺️ Learning Path Explorer"):
                gr.Markdown("### Explore Learning Paths")
                gr.Markdown("Select a target topic to see the complete learning path from start to that topic.")
                
                with gr.Row():
                    target_dropdown = gr.Dropdown(
                        choices=all_topic_choices,
                        label="Select Target Topic",
                        value="ai-engineer",
                        interactive=True
                    )
                    path_button = gr.Button("Show Learning Path", variant="primary")
                
                path_output = gr.HTML(value=ui_service.create_learning_path_display("ai-engineer"))
                
                path_button.click(
                    fn=show_learning_path,
                    inputs=[target_dropdown],
                    outputs=[path_output]
                )
            
            # Tab 5: Topic Explorer
            with gr.Tab("📚 Topic Explorer"):
                gr.Markdown("### Explore Individual Topics")
                gr.Markdown("Select any topic to see detailed information including subtopics and resources.")
                
                with gr.Row():
                    topic_dropdown = gr.Dropdown(
                        choices=topic_choices,
                        label="Select Topic",
                        interactive=True
                    )
                    details_button = gr.Button("Show Details", variant="primary")
                
                details_output = gr.HTML()
                
                details_button.click(
                    fn=show_topic_details,
                    inputs=[topic_dropdown],
                    outputs=[details_output]
                )
            
            # Tab 6: Progress Tracker
            with gr.Tab("📈 Progress Tracker"):
                gr.Markdown("### Track Your Learning Progress")
                gr.Markdown("Mark topics as completed to track your progress and get recommendations for next steps.")
                
                with gr.Row():
                    with gr.Column():
                        completed_dropdown = gr.Dropdown(
                            choices=all_topic_choices,
                            label="Mark Topic as Completed",
                            interactive=True
                        )
                        with gr.Row():
                            add_button = gr.Button("✅ Mark Complete", variant="primary")
                            remove_button = gr.Button("❌ Remove", variant="secondary")
                            reset_button = gr.Button("🔄 Reset All", variant="stop")
                
                progress_output = gr.HTML(value=update_progress_display())
                
                add_button.click(
                    fn=add_completed_topic,
                    inputs=[completed_dropdown],
                    outputs=[progress_output]
                )
                
                remove_button.click(
                    fn=remove_completed_topic,
                    inputs=[completed_dropdown],
                    outputs=[progress_output]
                )
                
                reset_button.click(
                    fn=reset_progress,
                    inputs=[],
                    outputs=[progress_output]
                )
        
        # Footer
        gr.Markdown("---")
        gr.Markdown("**📝 Based on the work from:** 👤 **Aurimas Griciūnas**")
        gr.Markdown("*Built with ❤️ using Gradio and following TDD/SOLID principles*")
        
        # Technical details
        gr.Markdown("""
        **🔧 Audio Features Explained:**
        - **Speech-to-Text:** Uses OpenAI Whisper for accurate transcription
        - **Sentiment Analysis:** Analyzes audio wave characteristics (energy, tempo, spectral features)
        - **AI Responses:** Context-aware responses using GPT-4 with sentiment information
        - **Learning Recommendations:** Personalized suggestions based on emotional state
        """)
    
    return app


if __name__ == "__main__":
    app = create_gradio_app()
    app.launch(share=True, debug=True)
