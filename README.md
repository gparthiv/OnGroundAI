# OnGroundAI - Field Workforce Supervisor Agent

<div align="center"> <img src="frontend/assets/logos/onground-logo.png" width="200"/>

**AI-Powered Multi-Agent System for Real-Time Field Workforce Management**

[![Built with Google ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-4285F4?style=flat-square&logo=google)](https://github.com/google/agent-development-kit)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.5-34A853?style=flat-square)](https://ai.google.dev/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[Live Demo](https://ongroundai.vercel.app) • [Video Demo](https://youtu.be/1NvneSqpSeA)

</div>

---

## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Architecture](#%EF%B8%8F-architecture)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Setup Instructions](#-setup-instructions)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Future Enhancements](#-future-enhancements)
- [Acknowledgments](#-acknowledgments)

---

## 🚨 Problem Statement

### The Challenge

Across India and Southeast Asia, **over 50 million field workers** operate outside traditional offices daily—delivery agents, utility inspectors, construction workers, telecom technicians, and rural service operators. Yet enterprises still manage them using outdated manual methods:

#### Current Pain Points

- 📞 **100+ daily supervisor calls** asking "Where are you?"
- 📸 **Unverified WhatsApp photos** without GPS metadata
- 🎤 **Voice notes pile up** unheard and unanalyzed
- ⏰ **Delays discovered hours later** after SLA breaches
- 🚨 **Safety incidents manually reported** causing response delays
- 📝 **No centralized audit trail** for compliance
- ❌ **Task fraud undetected** (fake updates, reused images)

#### Business Impact

| Metric | Impact |
|--------|--------|
| Task Completion Delays | **30-40%** due to poor visibility |
| Cost per Missed Delivery | **$2-5** from SLA breaches |
| Supervisor Time Wasted | **15-20%** on manual coordination |
| Safety Response Time | **Hours** instead of minutes |
| Fraud Detection Rate | **Near zero** without automation |

### Why AI Agents?

Traditional automation fails because field operations require:

✅ **Multi-modal reasoning** (text + images + audio)  
✅ **Context-aware decisions** (same message means different things at different times)  
✅ **Autonomous tool orchestration** (decide which tools to call when)  
✅ **Real-time processing** (can't wait for batch jobs)  
✅ **Human-in-the-loop approval** (for critical actions like task reassignment)

This is where **agentic AI systems** excel.

---

## 💡 Solution Overview

**OnGroundAI** is an enterprise-grade, multi-agent AI system that acts as a **24/7 digital field operations supervisor**. Instead of manual monitoring, the system:

1. **Interprets** unstructured worker updates (text, images, audio)
2. **Reasons** about operational state (delays, safety, fraud)
3. **Acts** autonomously (flagging, escalation, logging)
4. **Reports** decision-ready intelligence to supervisors

### How It Works
```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                             │
│            ("who is delayed?" / "run analysis")             │
└────────────────────────┬────────────────────────────────────┘
                         ↓
                   ┌─────────────┐
                   │  CoreAgent  │ (Router)
                   │  + Tools    │
                   └──────┬──────┘
                          │
         ┌────────────────┴────────────────┐
         │                                  │
    Simple Query                    Full Analysis
    (instant)                       (multi-agent)
         │                                  │
         ↓                                  ↓
    Direct Response              ┌──────────────────┐
                                 │ DataIngestAgent  │
                                 │ (Load all data)  │
                                 └────────┬─────────┘
                                          ↓
                         ┌────────────────────────────┐
                         │   PARALLEL EXECUTION       │
                         ├────────────────────────────┤
                         │  DelayAgent   SafetyAgent  │
                         │  - Messages   - Incidents  │
                         │  - Calendar   - Audio      │
                         │  - Images     - Images     │
                         └────────┬───────────────────┘
                                  ↓
                          ┌───────────────┐
                          │ ReportAgent   │
                          │ (Synthesize)  │
                          └───────┬───────┘
                                  ↓
                       Operational Report + Actions
```

---

## 🏗️ Architecture

### System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Vercel)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Dashboard   │  │  Chat UI     │  │  Agent       │       │
│  │  Worker Cards│  │  Real-time   │  │  Visualizer  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (HTTPS)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (Render)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               FastAPI Server                         │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐      │   │
│  │  │ /run_agent │  │ /api/data  │  │ /api/tools │      │   │
│  │  └────────────┘  └────────────┘  └────────────┘      │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │           Google ADK Runner                          │   │
│  │  ┌──────────────────────────────────────────┐        │   │
│  │  │  CoreAgent (Router)                      │        │   │
│  │  │  + Tools: load_messages, load_calendar   │        │   │
│  │  └──────────────────┬───────────────────────┘        │   │
│  │                     │                                │   │
│  │       ┌─────────────┴─────────────┐                  │   │
│  │       │                           │                  │   │
│  │       ▼                           ▼                  │   │
│  │  Simple Query              Full Workflow             │   │
│  │       │                           │                  │   │
│  │       │                  ┌────────▼────────┐         │   │
│  │       │                  │ DataIngestAgent │         │   │
│  │       │                  └────────┬────────┘         │   │
│  │       │                           │                  │   │
│  │       │                  ┌────────▼────────┐         │   │
│  │       │                  │ Parallel Agent  │         │   │
│  │       │                  │ ┌─────┐ ┌─────┐ │         │   │
│  │       │                  │ │Delay│ │Safe │ │         │   │
│  │       │                  │ └─────┘ └─────┘ │         │   │
│  │       │                  └────────┬────────┘         │   │
│  │       │                           │                  │   │
│  │       │                  ┌────────▼────────┐         │   │
│  │       │                  │  ReportAgent    │         │   │
│  │       │                  └────────┬────────┘         │   │
│  │       └──────────────────────────►│                  │   │
│  │                                   │                  │   │
│  │  ┌─────────────────────────────────▼──────────────┐  │   │
│  │  │         Evaluation System (LLM-as-Judge)       │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ Gemini API
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  Google Gemini 2.5 Flash Lite               │
└─────────────────────────────────────────────────────────────┘
```

### Agent Workflow Diagram

```
START: User Message
      │
      ▼
  ┌─────────────┐
  │ CoreAgent   │ ◄─── Tools: load_messages()
  │ (Router)    │           load_calendar()
  └──────┬──────┘           load_tasks()
         │
    ┌────┴─────┐
    │          │
Simple      Complex
Query       Analysis
    │          │
    ▼          ▼
 Direct   ┌──────────────────┐
 Answer   │ DataIngestAgent  │
          └────────┬─────────┘
                   │
                   ▼
          ┌────────────────────┐
          │ PARALLEL EXECUTION │
          ├────────┬───────────┤
          │        │           │
          ▼        ▼           │
    ┌─────────┐ ┌──────────┐   │
    │ Delay   │ │ Safety   │   │
    │ Agent   │ │ Agent    │   │
    └────┬────┘ └────┬─────┘   │
         │           │         │
         │ Tools:    │ Tools:  │
         │ • analyze_│ • trans │
         │   image   │   scribe│
         │ • trans-  │ •analyze│
         │   scribe  │   _image│
         └─────┬─────┴────┘    │
               │               │
               ▼               │
         ┌───────────┐         │
         │  Evaluate │         │
         │  Outputs  │◄────────┘
         └─────┬─────┘
               │
               ▼
         ┌────────────┐
         │   Report   │
         │   Agent    │
         └──────┬─────┘
                │
                ▼
         Final Report
         + UI Updates
                │
                ▼
              END
```

### Multi-Agent Orchestration
```python
Sequential Agent
├── DataIngestAgent (loads messages, calendar, tasks)
│   └── Tools: load_messages(), load_calendar(), load_tasks()
│
├── Parallel Agent
│   ├── DelayAgent (detects delays + fraud)
│   │   └── Tools: analyze_image_mock(), transcribe_audio_mock()
│   │
│   └── SafetyAgent (identifies incidents)
│       └── Tools: transcribe_audio_mock(), analyze_image_mock()
│
└── ReportAgent (synthesizes findings)
    └── Output: Structured operational report
```

### Data Flow

1. **Input:** Worker sends message/image/audio
2. **Ingestion:** DataIngestAgent loads all operational data
3. **Analysis:** Parallel agents process different aspects simultaneously
4. **Synthesis:** ReportAgent combines findings
5. **Output:** Supervisor receives actionable intelligence + updated UI

---

## ✨ Key Features

### Core Capabilities

| Feature | Description | Technology |
|---------|-------------|------------|
| 🔍 **Real-Time Delay Detection** | Compares message timestamps with scheduled calendar times | DelayAgent + ADK Tools |
| 🖼️ **Image Fraud Detection** | Extracts GPS/timestamp metadata, detects reused photos (92% accuracy) | analyze_image_mock() |
| 🎤 **Audio Transcription** | Converts Hindi/English audio to text, detects urgency levels | transcribe_audio_mock() |
| 🚨 **Safety Incident Detection** | Scans for keywords (accident, shock, danger) + audio urgency | SafetyAgent |
| 🔄 **Human-in-the-Loop Reassignment** | Pauses for supervisor approval before task reassignment | approve_reassignment() |
| 📊 **Operational Reporting** | Synthesizes all findings into structured, actionable reports | ReportAgent |
| 🤖 **Conversational Interface** | Natural language queries with context awareness | CoreAgent + Gemini |
| 📈 **Agent Quality Scoring** | LLM-as-a-Judge evaluates each agent's output (Day 4 pattern) | evaluate_agent_output() |

### User Interface
**Dashboard Features:**
- 📊 Real-time worker status cards
- 💬 Interactive chat with CoreAgent
- 🔄 Live agent execution visualization
- 🛠️ Tool registry with execution tracking
- 📝 Complete execution logs with timestamps
- 🎯 Agent quality metrics (evaluation scores)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (async REST API)
- **Agent Framework:** [Google ADK](https://github.com/google/agent-development-kit) (Agent Development Kit)
- **LLM:** Gemini 2.5 Flash Lite
- **Session Management:** InMemorySessionService
- **Observability:** LoggingPlugin + custom execution logs

### Frontend
- **UI:** Vanilla JavaScript + HTML5/CSS3
- **Design:** Google Material Design-inspired
- **Real-time Updates:** Async Fetch API
- **Visualization:** Dynamic worker cards, agent status indicators

### Deployment
- **Backend:** [Render](https://render.com) (Cloud runtime)
- **Frontend:** [Vercel](https://vercel.com) (CDN-optimized)
- **Architecture:** Decoupled microservices

### Key Dependencies
```
google-adk>=0.1.0
google-genai>=0.2.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-dotenv>=1.0.0
```

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Google AI Studio API Key ([Get one here](https://aistudio.google.com/app/apikey))
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/gparthiv/ongroundai.git
cd ongroundai
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the Backend
```bash
# Option 1: Using uvicorn directly
uvicorn backend.main:app --reload --port 8000

# Option 2: Using the start script
chmod +x start.sh
./start.sh
```

The backend will be available at `http://localhost:8000`

### 5. Run the Frontend

#### Option A: Simple HTTP Server
```bash
cd frontend
python -m http.server 3000
```

Visit `http://localhost:3000` in your browser.

#### Option B: Use Live Server (VS Code)

1. Install the "Live Server" extension in VS Code
2. Right-click on `frontend/index.html`
3. Select "Open with Live Server"
If running frontend locally, update frontend/script.js:
```bash
const API_BASE_URL = "http://localhost:8000";
```

### 6. Verify Installation

Test the backend API:
```bash
curl http://localhost:8000/api/data
```

You should see JSON data with workers, tasks, and messages.

---

## 📖 Usage

### Quick Start

1. **Open the dashboard** at `http://localhost:3000` (or your deployment URL)

2. **Try a quick query:**
```
   who is delayed?
```
   CoreAgent responds instantly with delay information.

3. **Run full analysis:**
```
   run analysis
```
   Watch the multi-agent workflow execute in real-time.

### Example Queries

#### Simple Queries (CoreAgent)
- `who is delayed?`
- `any safety issues?`
- `scan worker messages`
- `show me worker W101 status`
- `what tasks are pending?`

#### Complex Analysis (Full Workflow)
- `run analysis`
- `run workflow`
- `full analysis`
- `complete scan`

#### Follow-up Queries
- `what should I do about W101?`
- `which workers need immediate help?`
- `summarize the safety issues`

### API Endpoints

#### **POST** `/run_agent`
Executes the agent system with a user message.

**Request:**
```json
{
  "message": "who is delayed?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Worker W101 (Rajesh Kumar) is delayed...",
  "workflow_triggered": false,
  "session_id": "chat-session"
}
```

#### **GET** `/api/data`
Returns all operational data (workers, tasks, messages, calendar).

#### **GET** `/api/tools`
Returns tool registry with execution metadata.

---

## 📂 Project Structure
```
ongroundai/
├── agents/                      # Agent definitions
│   ├── __init__.py
│   ├── core_agent.py           # Router agent with tools
│   ├── data_ingest_agent.py    # Data loading agent
│   ├── delay_agent.py          # Delay detection agent
│   ├── safety_agent.py         # Safety incident agent
│   ├── report_agent.py         # Report synthesis agent
│   └── orchestrator.py         # Sequential workflow
│
├── backend/                     # FastAPI backend
│   ├── __init__.py
│   ├── main.py                 # API routes + evaluation logic
│   ├── shared_runner.py        # ADK runner configuration
│   └── agent_runner.py         # Agent execution logic
│
├── tools/                       # Custom tools
│   ├── __init__.py
│   ├── data_loader.py          # Load messages, calendar, tasks
│   ├── analyze_image_mock.py   # Image metadata extraction
│   ├── transcribe_audio_mock.py # Audio transcription + urgency
│   ├── approve_reassignment.py # Long-running operation (HITL)
│   └── evaluate_agent.py       # LLM-as-a-Judge (Day 4)
│
├── data/                        # Mock operational data
│   ├── workers.json            # Worker profiles
│   ├── tasks.json              # Task assignments
│   ├── messages.json           # Worker messages (text/audio/image)
│   └── calendar.json           # Scheduled task timings
│
├── frontend/                    # Web UI
│   ├── index.html              # Main dashboard
│   ├── script.js               # Frontend logic
│   ├── base.css                # Base styles
│   ├── layout.css              # Layout styles
│   ├── components.css          # Component styles
│   ├── chat.css                # Chat interface styles
│   └── assets/                 # Images and logos
│       ├── icons/
│       └── logos/
│
├── docs/                        # Documentation
│   └── images/                 # Architecture diagrams
│       ├── architecture.png
│       ├── agent-workflow.png
│       └── dashboard.png
│
├── .env.example                 # Environment variables template
├── .gitignore
├── requirements.txt             # Python dependencies
├── start.sh                     # Deployment startup script
├── README.md                    # This file
└── LICENSE
```

---

## 🌐 Deployment

### Live URLs

- **Frontend:** [https://ongroundai.vercel.app](https://ongroundai.vercel.app)
  ### ⚠️ Important Note About Loading Time<br>
    The backend runs on Render free tier, which sleeps after inactivity.<br>
    So when visiting the Vercel frontend<br>
    ⏳ Expect 50–70 seconds for backend to wake up<br>
    ⚠️ Buttons like “Run Analysis” or “Scan Worker Messages” may appear unresponsive initially<br>
    ✔️ Once warmed up, everything works normally<br>
- **Backend API:** [https://ongroundai-backend.onrender.com](https://ongroundai-backend.onrender.com)
- **API Health Check:** [https://ongroundai-backend.onrender.com/](https://ongroundai-backend.onrender.com/)

### Deploy Your Own Instance

#### Backend (Render)

1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `./start.sh`
   - **Environment Variables:** Add `GOOGLE_API_KEY`
5. Deploy

#### Frontend (Vercel)

1. Fork this repository
2. Import project on [Vercel](https://vercel.com)
3. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `frontend`
   - **Build Command:** (leave empty)
   - **Output Directory:** `.`
4. Update `API_BASE_URL` in `frontend/script.js` to your Render backend URL
5. Deploy

---

## 🔮 Future Enhancements

### Phase 2 Features

- [ ] **A2A Protocol:** Agent-to-agent communication for collaborative workflows
- [ ] **True MCP Servers:** Real Google Drive, Maps, Twilio integrations
- [ ] **Advanced Memory:** Long-term Memory Bank for worker behavior patterns
- [ ] **Real Audio Processing:** Google Speech-to-Text for 10+ languages
- [ ] **Real Image Analysis:** Google Vision API for actual metadata extraction
- [ ] **Analytics Dashboard:** Historical trends and predictive insights


---

## 🙏 Acknowledgments

- **Google AI Agents Intensive Course** (Nov 2025) - For the comprehensive training
- **Google ADK Team** - For the Agent Development Kit framework
- **Kaggle** - For hosting the course and competition
- **Course Instructors:** Kanchana Patlolla, Anant Nawalgaria, and the entire Google team
- **Mock Data Inspiration:** Real-world field operations challenges faced by logistics and utility companies across India

---

## 📞 Contact

**Parthiv Ghosh**
- LinkedIn: [linkedin.com/in/parthivghosh119](https://linkedin.com/in/parthivghosh119)
- Kaggle: [kaggle.com/parthivghosh](https://kaggle.com/parthivghosh)
- Email: g.parthiv119@gmail.com

---

## 🎥 Demo Video

[![OnGroundAI Demo](https://img.youtube.com/vi/1NvneSqpSeA/0.jpg)]([https://youtube.com/your-video](https://youtu.be/1NvneSqpSeA))

---

<div align="center">

**Built with ❤️ for the Google AI Agents Intensive Capstone Project**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/gparthiv/ongroundai/issues) • [Request Feature](https://github.com/gparthiv/ongroundai/issues)

</div>

---
