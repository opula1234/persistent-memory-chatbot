# 🤖 AI Chatbot with Persistent Database Memory

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![SQLite](https://img.shields.io/badge/SQLite-Persistent-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-red)

A production-ready FastAPI chatbot powered by Google's Gemini 2.5 Flash model with persistent conversational memory. Chat history is stored in SQLite and automatically reconstructed for every request, allowing the AI to maintain context across multiple interactions within the same session.

---

## 🚀 Key Features

### 🤖 AI-Powered Conversations

* Google Gemini 2.5 Flash integration via LangChain
* Context-aware responses
* Multi-turn conversation support

### 🧠 Persistent Memory

* Session-based chat history
* SQLite-backed storage
* Automatic context reconstruction
* Memory survives application restarts

### ⚡ FastAPI Backend

* Async API endpoints
* Automatic OpenAPI documentation
* Swagger UI & ReDoc support
* Pydantic request validation

### 🐳 Docker Support

* Containerized deployment
* Environment variable configuration
* Persistent volume mounting
* Portable across environments

### 🗄️ Database Management

* SQLModel ORM
* Automatic table creation using FastAPI Lifespan
* Lightweight SQLite storage
* Easy migration path to PostgreSQL

---

# 🏛️ System Architecture

```text
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Request
       ▼
┌────────────────────┐
│      FastAPI       │
│   REST Endpoint    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Retrieve History  │
│    from SQLite     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Convert to Human & │
│   AI Messages      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Gemini 2.5 Flash   │
│     via LangChain  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Save Conversation  │
│ Back to Database   │
└─────────┬──────────┘
          │
          ▼
      Response
```

---

# 🛠️ Tech Stack

| Technology       | Purpose               |
| ---------------- | --------------------- |
| Python           | Programming Language  |
| FastAPI          | REST API Framework    |
| SQLModel         | ORM                   |
| SQLite           | Persistent Database   |
| LangChain        | LLM Framework         |
| Gemini 2.5 Flash | Large Language Model  |
| Uvicorn          | ASGI Server           |
| Docker           | Containerization      |
| uv               | Dependency Management |

---

# 📂 Project Structure

```text
persistent-memory-chatbot/
│
├── main.py
├── Dockerfile
├── .dockerignore
├── chat_history.db
├── pyproject.toml
├── uv.lock
├── README.md
│
└── __pycache__/
```

---

# 🔧 Prerequisites

* Python 3.10+
* Docker (Optional)
* Google Gemini API Key
* uv Package Manager

Install uv:

```bash
pip install uv
```

---

# 📥 Installation

## Clone Repository

```bash
git clone https://github.com/opula1234/persistent-memory-chatbot.git

cd persistent-memory-chatbot
```

## Install Dependencies

```bash
uv sync
```

## Configure Environment Variables

### Windows

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### Linux/macOS

```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

# ▶️ Running Locally

Start the application:

```bash
uv run python main.py
```

Or run using Uvicorn:

```bash
uv run uvicorn main:app --reload
```

Application URL:

```text
http://localhost:8000
```

---

# 🐳 Docker Deployment

## Build Docker Image

```bash
docker build -t persistent-chatbot .
```

Verify image:

```bash
docker images
```

---

## Run Docker Container

```bash
docker run -d \
-p 8000:8000 \
-v chatbot_data:/app \
-e GEMINI_API_KEY="your_api_key_here" \
--name persistent-chatbot \
persistent-chatbot
```

---

## Verify Running Container

```bash
docker ps
```

Expected output:

```text
CONTAINER ID   IMAGE                STATUS
xxxxxxxxxxxx   persistent-chatbot   Up
```

---

## View Logs

```bash
docker logs -f persistent-chatbot
```

---

## Stop Container

```bash
docker stop persistent-chatbot
```

---

## Remove Container

```bash
docker rm persistent-chatbot
```

---

# 💾 Data Persistence

The SQLite database is stored inside the container.

To prevent data loss when containers are recreated, a Docker volume is mounted:

```bash
-v chatbot_data:/app
```

Benefits:

* Database survives container restarts
* Chat history remains intact
* Easy backup and migration

Inspect volume:

```bash
docker volume ls
```

---

# 🗄️ Database Schema

## ChatMessageRecord

| Field       | Type    | Description             |
| ----------- | ------- | ----------------------- |
| id          | Integer | Primary Key             |
| session_id  | String  | Conversation Identifier |
| sender_type | String  | human / ai              |
| content     | String  | Message Content         |

Example:

```json
{
  "id": 1,
  "session_id": "user_123",
  "sender_type": "human",
  "content": "Hello"
}
```

---

# 📡 API Endpoint

## Chat with Persistent Memory

### Request

```http
POST /api/v1/chat-with-history
```

### Request Body

```json
{
  "session_id": "user_123",
  "prompt": "My name is Alex"
}
```

### Response

```json
{
  "session_id": "user_123",
  "reply": "Hello Alex! Nice to meet you."
}
```

---

# 🧪 Example Usage

## First Request

```bash
curl -X POST http://localhost:8000/api/v1/chat-with-history \
-H "Content-Type: application/json" \
-d '{
      "session_id":"user_123",
      "prompt":"My name is Alex"
    }'
```

## Follow-up Request

```bash
curl -X POST http://localhost:8000/api/v1/chat-with-history \
-H "Content-Type: application/json" \
-d '{
      "session_id":"user_123",
      "prompt":"What is my name?"
    }'
```

### Response

```json
{
  "session_id": "user_123",
  "reply": "Your name is Alex."
}
```

This demonstrates persistent conversational memory.

---

# 📖 API Documentation

| Tool       | URL                         |
| ---------- | --------------------------- |
| Swagger UI | http://localhost:8000/docs  |
| ReDoc      | http://localhost:8000/redoc |

---

# 🔒 Production Recommendations

For real-world deployments:

* Use PostgreSQL instead of SQLite
* Store secrets in environment variables
* Enable JWT Authentication
* Add Role-Based Access Control (RBAC)
* Use HTTPS
* Implement Rate Limiting
* Add Structured Logging
* Add Monitoring (Prometheus/Grafana)
* Configure CI/CD Pipelines
* Deploy via Docker Compose or Kubernetes

---

# 🔮 Future Enhancements

* PostgreSQL Support
* Redis Caching
* JWT Authentication
* Docker Compose
* Kubernetes Deployment
* CI/CD using GitHub Actions
* LangGraph Integration
* Vector Database Memory (ChromaDB/Pinecone)
* Streaming Responses
* OpenTelemetry Observability

---

# 👨‍💻 Author

Built with ❤️ using:

* FastAPI
* SQLModel
* LangChain
* Google Gemini 2.5 Flash
* Docker

This project demonstrates how to build a session-aware AI chatbot with persistent memory, containerized deployment, and production-ready architecture.
