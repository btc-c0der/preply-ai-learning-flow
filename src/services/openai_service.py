"""
OpenAI service for speech-to-text and AI-powered learning assistance.
Integrates with OpenAI's API for transcription and chat completion.
"""

import openai
from typing import Optional, Dict, Any
import os


class OpenAIService:
    """
    Service for OpenAI API integration.
    
    Single Responsibility: Handles OpenAI API interactions for transcription and chat.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize OpenAI service with API key.
        
        Args:
            api_key: OpenAI API key
            
        Raises:
            ValueError: If API key is empty or None
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("OpenAI API key is required")
        
        self.api_key = api_key
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text
            
        Raises:
            RuntimeError: If transcription fails
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            raise RuntimeError(f"Error transcribing audio: {str(e)}")
    
    def process_learning_query(self, query: str, sentiment_context: str = "", user_progress: Optional[Dict] = None) -> str:
        """
        Process a learning query with AI assistance.
        
        Args:
            query: User's learning question or request
            sentiment_context: Context about user's emotional state
            user_progress: Optional user progress information
            
        Returns:
            AI-generated response with learning guidance
        """
        try:
            # Build context-aware prompt
            system_prompt = self._build_system_prompt(sentiment_context, user_progress)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm sorry, I encountered an error while processing your request: {str(e)}. Please try again or check your OpenAI API key."
    
    def get_topic_specific_help(self, topic_id: str, user_question: str) -> str:
        """
        Get specific help for a learning topic.
        
        Args:
            topic_id: ID of the learning topic
            user_question: User's specific question
            
        Returns:
            Topic-specific guidance
        """
        try:
            # Map topic IDs to detailed descriptions
            topic_descriptions = {
                "llm-apis": "Large Language Model APIs, including types of LLMs, structured outputs, prompt caching, and multi-modal models",
                "model-adaptation": "Model adaptation techniques including prompt engineering, tool use, and fine-tuning",
                "storage-retrieval": "Storage solutions for AI applications including vector databases, graph databases, and hybrid retrieval",
                "infrastructure": "AI infrastructure including Kubernetes, cloud services, CI/CD, model routing, and LLM deployment",
                "ai-agents": "AI agent development including design patterns, multi-agent systems, memory, tools, and planning",
                "rag-agentic": "Retrieval-Augmented Generation and agentic RAG including data retrieval, vector+graph approaches, and LLM orchestration",
                "observability-evaluation": "AI system observability and evaluation including instrumentation, platforms, and evaluation techniques",
                "security": "AI security including guardrails, testing LLM applications, and secure orchestration",
                "forward-looking": "Emerging AI technologies including voice and vision agents, auto agents, and automated prompt engineering"
            }
            
            topic_description = topic_descriptions.get(topic_id, f"AI Engineering topic: {topic_id}")
            
            system_prompt = f"""You are an expert AI Engineering tutor specializing in {topic_description}. 
            Provide clear, practical guidance that helps students understand and apply the concepts. 
            Be encouraging and provide specific next steps when possible."""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=400,
                temperature=0.6
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm having trouble accessing the AI assistant right now: {str(e)}. Please check your internet connection and API key."
    
    def _build_system_prompt(self, sentiment_context: str, user_progress: Optional[Dict] = None) -> str:
        """
        Build a context-aware system prompt.
        
        Args:
            sentiment_context: User's emotional context
            user_progress: User's learning progress
            
        Returns:
            Formatted system prompt
        """
        base_prompt = """You are an expert AI Engineering learning assistant and mentor. You help students navigate the AI Engineering learning roadmap, which includes:

1. LLM APIs (Types, Structured Outputs, Prompt Caching, Multi-modal)
2. Model Adaptation (Prompt Engineering, Tool Use, Fine-tuning)
3. Storage for Retrieval (Vector DBs, Graph DBs, Hybrid retrieval)
4. Infrastructure (Kubernetes, Cloud, CI/CD, Model Routing)
5. AI Agents (Design Patterns, Multi-agent, Memory, Planning)
6. RAG & Agentic RAG (Data retrieval, Vector+Graph, MCP)
7. Observability & Evaluation (Instrumentation, Platforms, Techniques)
8. Security (Guardrails, Testing, Secure orchestration)
9. Forward-looking (Voice/Vision Agents, Auto Agents, Automated Prompt Engineering)

Provide personalized, encouraging guidance. Be specific about next steps and resources."""
        
        # Add sentiment context
        if sentiment_context:
            base_prompt += f"\n\nUser's current emotional state: {sentiment_context}. Adjust your response tone and recommendations accordingly."
        
        # Add progress context
        if user_progress:
            completed = user_progress.get("completed_topics", [])
            if completed:
                base_prompt += f"\n\nUser has completed: {', '.join(completed)}. Build on their existing knowledge."
        
        return base_prompt
    
    def generate_study_guide(self, topic_id: str, user_progress: Optional[Dict] = None) -> str:
        """
        Generate a comprehensive AI-powered study guide for a specific topic.
        
        Args:
            topic_id: ID of the learning topic
            user_progress: User's learning progress information
            
        Returns:
            Detailed study guide content
        """
        try:
            # Enhanced topic descriptions with detailed context
            topic_descriptions = {
                "llm-apis": {
                    "title": "Large Language Model APIs",
                    "overview": "Master LLM APIs including types of LLMs, structured outputs, prompt caching, and multi-modal models",
                    "hours": "20 hours",
                    "focus_areas": ["API Integration", "Model Selection", "Optimization Techniques", "Multi-modal Capabilities"]
                },
                "model-adaptation": {
                    "title": "Model Adaptation Techniques", 
                    "overview": "Learn model adaptation through prompt engineering, tool use, and fine-tuning strategies",
                    "hours": "30 hours",
                    "focus_areas": ["Prompt Engineering", "Tool Integration", "Fine-tuning", "Model Customization"]
                },
                "storage-retrieval": {
                    "title": "Storage for Retrieval Systems",
                    "overview": "Understand storage solutions including vector databases, graph databases, and hybrid retrieval systems",
                    "hours": "25 hours", 
                    "focus_areas": ["Vector Databases", "Graph Storage", "Retrieval Strategies", "Hybrid Systems"]
                },
                "infrastructure": {
                    "title": "AI Infrastructure & Deployment",
                    "overview": "Build robust AI infrastructure with Kubernetes, cloud services, CI/CD, and model routing",
                    "hours": "35 hours",
                    "focus_areas": ["Kubernetes", "Cloud Deployment", "CI/CD Pipelines", "Model Routing"]
                },
                "ai-agents": {
                    "title": "AI Agent Development",
                    "overview": "Design and implement AI agents with patterns, multi-agent systems, memory, and planning",
                    "hours": "40 hours",
                    "focus_areas": ["Agent Architecture", "Multi-agent Systems", "Memory Management", "Planning Algorithms"]
                },
                "rag-agentic": {
                    "title": "RAG & Agentic RAG Systems", 
                    "overview": "Build advanced retrieval-augmented generation with vector+graph approaches and LLM orchestration",
                    "hours": "30 hours",
                    "focus_areas": ["RAG Architecture", "Vector+Graph Hybrid", "LLM Orchestration", "Agentic Patterns"]
                },
                "observability-evaluation": {
                    "title": "Observability & Evaluation",
                    "overview": "Implement comprehensive monitoring, instrumentation, and evaluation for AI systems",
                    "hours": "25 hours",
                    "focus_areas": ["System Monitoring", "Performance Metrics", "Evaluation Frameworks", "Debugging Tools"]
                },
                "security": {
                    "title": "AI Security & Safety",
                    "overview": "Secure AI applications with guardrails, testing frameworks, and secure orchestration",
                    "hours": "20 hours",
                    "focus_areas": ["Security Guardrails", "Vulnerability Testing", "Secure Deployment", "Compliance"]
                },
                "forward-looking": {
                    "title": "Emerging AI Technologies",
                    "overview": "Explore cutting-edge developments in voice/vision agents, auto agents, and automated prompt engineering",
                    "hours": "15 hours",
                    "focus_areas": ["Voice Agents", "Vision Systems", "Autonomous Agents", "Automated Engineering"]
                }
            }
            
            topic_info = topic_descriptions.get(topic_id, {
                "title": f"AI Engineering Topic: {topic_id}",
                "overview": f"Study guide for {topic_id}",
                "hours": "Variable",
                "focus_areas": ["Core Concepts", "Practical Applications", "Best Practices"]
            })
            
            # Build progress context
            progress_context = ""
            if user_progress:
                completed = user_progress.get("completed_topics", [])
                if completed:
                    progress_context = f"The user has already completed: {', '.join(completed)}. Build upon this knowledge and suggest connections."
            
            system_prompt = f"""You are an expert AI Engineering curriculum designer. Generate a comprehensive, actionable study guide for the topic: {topic_info['title']}.

Topic Overview: {topic_info['overview']}
Estimated Time: {topic_info['hours']}
Key Focus Areas: {', '.join(topic_info['focus_areas'])}

{progress_context}

Create a detailed study guide with:
1. Learning Objectives (3-5 specific, measurable goals)
2. Prerequisites & Background Knowledge
3. Week-by-Week Study Plan (break down the hours logically)
4. Core Concepts & Theory (key topics to master)
5. Hands-On Projects (2-3 practical exercises)
6. Essential Resources (books, courses, documentation)
7. Assessment Criteria (how to measure progress)
8. Common Pitfalls & How to Avoid Them
9. Connection to Other Topics in the roadmap
10. Next Steps & Advanced Topics

Format as HTML for better readability with headers, bullet points, and emphasis. Make it comprehensive but practical - someone should be able to follow this guide to mastery."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a comprehensive study guide for {topic_info['title']}. Make it detailed, practical, and actionable for someone wanting to master this topic as part of their AI Engineering journey."}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"""
            <div style="color: red; padding: 20px; border: 1px solid red; border-radius: 5px;">
                <h3>❌ Error Generating Study Guide</h3>
                <p>I encountered an error while generating the study guide: {str(e)}</p>
                <p>Please check your OpenAI API key and internet connection, then try again.</p>
            </div>
            """
