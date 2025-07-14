---
title: ai-learning-path-audio-sentiment
app_file: app.py
sdk: gradio
sdk_version: 5.36.2
---
# AI Engineering Learning Roadmap 🚀

A comprehensive, interactive learning roadmap for AI Engineering built with **Gradio** and featuring **audio sentiment analysis** powered by OpenAI.

## 🎯 Features

- **🎤 Audio Recording & Sentiment Analysis** - Record your learning questions and get AI responses based on your emotional state
- **💬 AI-Powered Chatbot** - Interactive assistant for learning guidance  
- **🗺️ Learning Path Explorer** - Navigate through AI engineering topics
- **📚 AI-Generated Study Guides** - Get comprehensive, personalized study plans for any topic
- **📈 Progress Tracking** - Track your learning journey through 275+ hours of content
- **🎯 Topic-Specific Help** - Get targeted assistance for specific AI engineering topics

## 🏗️ Architecture

Built following **SOLID** principles and **Test-Driven Development (TDD)**:

### Core Components

- **`LearningNode`** - Data model for roadmap topics
- **`RoadmapRepository`** - Data storage and retrieval
- **`RoadmapService`** - Business logic layer
- **`GradioUIService`** - UI presentation layer
- **`app.py`** - Main Gradio application

### Design Principles Applied

✅ **Single Responsibility** - Each class has one clear purpose  
✅ **Open/Closed** - Extensible without modification  
✅ **Liskov Substitution** - Interchangeable implementations  
✅ **Interface Segregation** - Focused interfaces  
✅ **Dependency Inversion** - Depends on abstractions  
✅ **DRY** - No code duplication  
✅ **100% Test Coverage** - All logic tested first  

## 🛣️ Learning Roadmap

### 1. **LLM APIs** (20h)
- Types of LLMs
- Structured Outputs
- Prompt Caching
- Multi-modal models

### 2. **Model Adaptation** (30h)
- Prompt Engineering
- Tool Use
- Finetuning

### 3. **Storage for Retrieval** (25h)
- Vector Databases
- Graph Databases
- Hybrid retrieval

### 4. **Infrastructure** (40h)
- Kubernetes
- Cloud Services
- CI/CD
- Model Routing
- LLM deployment

### 5. **AI Agents** (50h)
- AI Agent Design Patterns
- Multi-agent systems
- Memory + Tools
- Planning
- Finetuning

### 6. **RAG & Agentic RAG** (35h)
- Data retrieval and generation
- Vector + Graph
- MCP
- LLM Orchestration Frameworks

### 7. **Observability & Evaluation** (30h)
- AI Agent instrumentation
- Observability platforms
- Evaluation techniques

### 8. **Security** (25h)
- Guardrails
- Testing LLM-based applications
- Secure orchestration

### 9. **Forward looking elements** (20h)
- Voice and Vision Agents
- Auto Agents
- Automated Prompt Engineering

## � AI-Generated Study Guides

The application now offers comprehensive, personalized study guides for each topic:

- **Learning Objectives** - Clear, measurable goals for each topic
- **Week-by-Week Study Plan** - Structured timeline based on topic's estimated hours
- **Core Concepts & Theory** - Key topics to master with explanations
- **Hands-On Projects** - Practical exercises to apply your knowledge
- **Essential Resources** - Recommended books, courses, and documentation
- **Assessment Criteria** - Ways to measure your progress
- **Common Pitfalls & Solutions** - Tips to avoid typical challenges
- **Topic Connections** - How each topic connects to others in the roadmap

Simply select any topic in the Learning Path Explorer tab and click "Generate Study Guide" to create a personalized learning plan tailored to your progress.

## �🚀 Quick Start

### Prerequisites
- Python 3.11+ (3.13 has compatibility issues with Gradio)
- pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd preply-ai-learning-flow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Alternative: Test Core Services

If you encounter Gradio compatibility issues:

```bash
# Run tests to see the application working
python -m pytest tests/ -v --cov=src

# Run the core services demo
python run.py
```

## 🧪 Testing

This project follows **Test-Driven Development (TDD)**:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_roadmap_service.py -v
```

**Test Coverage: 95%+** (excluding Gradio UI due to Python 3.13 compatibility)

## 🚢 Deployment on Hugging Face Spaces

This application is ready to deploy on Hugging Face Spaces:

1. **Create a new Space** on Hugging Face with Gradio SDK
2. **Set your OpenAI API Key** as a repository secret (name: `OPENAI_API_KEY`)
3. **Upload files** maintaining the directory structure
4. **Rename files**:
   - Use `requirements-hf.txt` as your `requirements.txt`
   - Use `README-HF.md` as your `README.md` (optional)

See `HF_QUICK_DEPLOY.md` for detailed deployment instructions.

## 📁 Project Structure

```
src/
├── models/
│   └── learning_node.py      # Data models
├── repositories/
│   └── roadmap_repository.py # Data layer
├── services/
│   └── roadmap_service.py    # Business logic
├── ui/
│   └── gradio_ui_service.py  # UI layer
└── app.py                    # Main application

tests/
├── test_learning_node.py
├── test_roadmap_repository.py
├── test_roadmap_service.py
├── test_gradio_ui_service.py
└── test_app.py

requirements.txt
run.py
README.md
```

## 🎨 Features

### 🗺️ Learning Path Explorer
- Select any target topic
- See the complete prerequisite path
- Visualize step-by-step progression

### 📚 Topic Explorer
- Detailed topic information
- Subtopics breakdown
- Curated resources and links

### 📈 Progress Tracker
- Mark topics as completed
- Track learning progress
- Get personalized recommendations
- Calculate remaining hours

## 🛠️ Development

This project demonstrates:

- **Clean Architecture** with separated concerns
- **SOLID principles** in practice
- **Test-Driven Development** workflow
- **Dependency Injection** pattern
- **Repository pattern** for data access
- **Service layer** for business logic
- **Modern Python** development practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests first (TDD)
4. Implement the feature
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

Based on the original roadmap work by **Aurimas Griciūnas**.

## 🎉 Acknowledgments

- **Aurimas Griciūnas** for the original AI Engineering roadmap
- **Gradio** team for the amazing UI framework
- **TDD/SOLID** community for the development principles

---

*Built with ❤️ using TDD and SOLID principles*
