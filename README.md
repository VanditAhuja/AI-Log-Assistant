# AI-Powered Log Intelligence & Debugging Assistant

> An enterprise-grade AI log analysis system built during HCLtech Internship

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)
![AI](https://img.shields.io/badge/AI-Groq%20LLaMA3-purple)

---

# Project Overview

A full-stack AI-based log analysis system that allows developers to upload application log files and interact with them using natural language queries. The system uses AI to identify errors, summarize logs, suggest probable root causes and fixes — helping in faster debugging by converting raw logs into structured insights.

This project simulates an enterprise-level observability tool used in modern IT operations.

---

# Features

-  **Log File Upload** — Upload any `.log` or `.txt` file
-  **Automatic Error Detection** — Extracts ERROR and CRITICAL events
-  **Visual Dashboard** — Charts and stats for log distribution
-  **AI Root Cause Analysis** — Powered by Groq LLaMA3 AI
-  **Natural Language Chat** — Ask questions about your logs
-  **Upload History** — Track previously analyzed log files
-  **PDF Export** — Download professional analysis reports

---

# Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI | Groq API (LLaMA3-70B) |
| Frontend | HTML, CSS, JavaScript |
| PDF | ReportLab |
| Version Control | Git, GitHub |

---

# Project Structure
AI-Log-Assistant/

│

├── backend/

│   ├── app.py          # FastAPI server & API endpoints

│   ├── database.py     # Log history management

│   └── pdf_generator.py # PDF report generation

│

├── ai/

│   └── ai_engine.py    # Groq AI integration

│

├── parser/

│   └── parser.py       # Log file parser

│

├── frontend/

│   └── index.html      # Web dashboard

│

├── logs/

│   └── sample.log      # Sample log file

│

├── requirements.txt

└── README.md
---

# Getting Started

# 1. Clone the repository
```bash
git clone https://github.com/VanditAhuja/AI-Log-Assistant.git
cd AI-Log-Assistant
```

# 2. Install dependencies
```bash
pip install -r requirements.txt
```

# 3. Set up environment variables
Create a `.env` file in the root directory:
GROQ_API_KEY=your-groq-api-key-here
Get your free Groq API key at: https://console.groq.com

# 4. Run the server
```bash
uvicorn backend.app:app --reload
```

# 5. Open the app
http://127.0.0.1:8000/app
---

# Screenshots

# Dashboard
- Upload log files and get instant AI analysis
- Visual charts showing log distribution
- Error detection with timestamps

# AI Analysis
- Root cause analysis
- Impact assessment
- Suggested fixes
- Prevention strategies

# Chat Interface
- Ask natural language questions about your logs
- Get instant AI-powered answers

# PDF Report
- Download professional analysis reports
- Clean white professional format

---

# API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/app` | Web dashboard |
| POST | `/upload` | Upload and analyze log file |
| POST | `/chat` | Chat about logs |
| GET | `/history` | Get upload history |
| GET | `/export/{filename}` | Download PDF report |

---

# Developer

**Vandit Ahuja**
---
