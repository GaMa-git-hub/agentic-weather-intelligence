![Python](https://img.shields.io/badge/Python-3.x-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-purple)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Status](https://img.shields.io/badge/Status-Active-success)


# 🌦️ Agentic Weather Intelligence System

An **Agentic AI system** that retrieves real-time weather data, reasons over user queries, and produces intelligent responses using a **LangGraph-orchestrated autonomous agent** powered by a **local LLM (Ollama + Gemma 2B)**.

This project demonstrates modern **agent architecture design**, combining deterministic software engineering with LLM reasoning — a core pattern used in production AI systems.

---

## 🚀 Project Overview

Traditional chatbots rely entirely on LLM reasoning, which can lead to hallucinations and unreliable outputs.

This system implements a **Hybrid Agent Architecture** where:

- Python handles structured decision-making
- External tools provide real-world data
- A local LLM performs reasoning and natural language generation
- LangGraph orchestrates the workflow as a state machine

The result is a **reliable, context-aware AI agent** capable of autonomous tool usage.

---

## 🧠 Agent Architecture

The agent operates as a LangGraph state pipeline:
User Input
↓
Intent Detection Node
↓
City Extraction Node
↓
Weather Tool Node
↓
LLM Response Node
↓
Final Answer


### Hybrid Control Principle

| Component | Responsibility |
|-----------|---------------|
| Python Logic | Deterministic decisions |
| Weather Tool | Real-world data retrieval |
| LLM (Gemma 2B) | Reasoning & response generation |
| LangGraph | Workflow orchestration |

This design prevents hallucinations and ensures grounded responses.

---

## ✨ Current Features

- 🌍 Real-time weather retrieval (OpenWeather API)
- 🤖 Local LLM reasoning using Ollama (Gemma 2B)
- 🧩 LangGraph-based agent orchestration
- 🔄 Context-aware follow-up queries
- 🧠 Stateful conversation flow
- ⚙️ Deterministic tool calling
- 🔐 Secure API key handling using `.env`
- 🧱 Modular node-based architecture

---

## 🧩 Example Interaction
Ask: what is weather in chennai?
→ Real-time weather response

Ask: in kochi?
→ Context-aware follow-up

Ask: should I carry umbrella?
→ Recommendation based on latest weather data



---

## 🛠️ Tech Stack

### Core
- Python 3.x

### AI & Agents
- Ollama (Local LLM runtime)
- Gemma:2B Model
- LangGraph (Agent orchestration)

### External Tools
- OpenWeather API

### Development
- Git & GitHub
- Virtual Environments
- Modular Project Structure

---
```
## 📂 Project Structure
agentic-weather-intelligence/
│
├── agents/ # Earlier manual agent implementation
├── graph/ # LangGraph workflow
│ └── weather_graph.py
│
├── llm/ # Ollama client wrapper
├── tools/ # Weather API integration
├── config/ # Environment settings
│
├── main.py # Application entry point
├── requirements.txt
└── .gitignore


---

## ⚙️ How It Works

1. User submits a query.
2. Intent node determines whether weather data is required.
3. City extraction node identifies the location.
4. Weather tool fetches live API data.
5. LLM generates a grounded response using tool output.
6. Graph state persists for follow-up queries.

---

## ▶️ Running the Project Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/agentic-weather-intelligence.git
cd agentic-weather-intelligence

2️⃣ Create Virtual Environment
3️⃣ Install Dependencies
4️⃣ Add Environment Variables
5️⃣ Start Ollama
6️⃣ Run the Agent

🎯 Engineering Concepts Demonstrated

Agentic AI system design

LangGraph orchestration

Tool-calling architecture

Hybrid deterministic + LLM reasoning

Stateful conversational agents

Local LLM deployment

Modular software design

🔮 Future Enhancements

Multi-agent collaboration

Forecast analysis agent

Historical weather RAG system

Alert & notification engine

Web dashboard interface

👨‍💻 Author
Built as part of hands-on exploration into Agentic AI systems and autonomous workflows.


---

## ✅ After Adding It

Run:

```bash
git add README.md
git commit -m "Add professional project README"
git push
