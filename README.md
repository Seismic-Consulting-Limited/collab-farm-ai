# CollabFarm AI Assistant

## Overview

The CollabFarm AI Assistant is a Retrieval-Augmented Generation (RAG) based chatbot that provides users with accurate information about the CollabFarm platform.

The assistant uses approved CollabFarm knowledge sources and an AI language model to answer public platform questions related to:

* Cooperative registration and management
* Investor activities
* Farmer onboarding
* Farm information
* Farming cycles
* Funding opportunities
* Investment tracking
* Settlement processes

The system is designed to provide responses based on CollabFarm-specific knowledge rather than relying only on general AI knowledge.

---

# Architecture Overview

The CollabFarm AI Assistant follows a Retrieval-Augmented Generation (RAG) architecture.

The system:

1. Receives a user's question.
2. Searches the CollabFarm knowledge base for relevant information.
3. Combines the retrieved information with the user's question.
4. Sends the context to the AI model.
5. Returns a grounded response to the user.

---

# Technology Stack

## Backend

### Python

Python is used for:

* AI workflow management
* API development
* Knowledge processing
* Retrieval operations

---

## API Framework

### FastAPI

FastAPI provides the backend API layer between the frontend application and the AI assistant.

It handles:

* Receiving user messages
* Managing chat requests
* Returning AI responses
* Providing API documentation

---

## Large Language Model

### Ollama Cloud

Ollama Cloud provides the language model used for response generation.

Current model:

`gpt-oss:120b`

The model handles:

* Natural language understanding
* Response generation
* Conversational interaction

---

## Retrieval-Augmented Generation Components

### ChromaDB

ChromaDB is used as the vector database.

It stores embedded CollabFarm knowledge and allows the system to search information based on meaning rather than exact keywords.

---

### Sentence Transformers

Sentence Transformers converts knowledge documents into embeddings for semantic search.

Embedding model:

`all-MiniLM-L6-v2`

---

### LangChain Components

LangChain components are used for:

* Text splitting
* Document processing
* RAG workflow support

---

# Project Structure

```text
collab-farm-ai/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── memory.py
│   │   └── ollama_client.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   └── embedder.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── retriever.py
│   │
│   └── vectorstore/
│       ├── __init__.py
│       └── chroma.py
│
├── knowledge/
│   ├── raw/
│   └── chroma_db/
│
├── .env
├── .env.example
├── api_main.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Folder Description

## app/api

Contains the FastAPI communication layer.

Responsible for:

* Receiving frontend requests
* Passing requests to the chatbot
* Returning responses

Main file:

`routes.py`

---

## app/chatbot

Contains chatbot logic.

### chatbot.py

Handles:

* User questions
* Session memory
* Retrieval calls
* Prompt creation
* AI response generation
* Duplicate-question handling

### memory.py

Handles temporary session-based conversation memory.

The chatbot keeps the most recent 10 messages for each session when building conversation history.

### ollama_client.py

Handles communication with Ollama Cloud.

---

## app/ingestion

Contains the knowledge preparation pipeline.

### loader.py

Loads CollabFarm knowledge documents.

### splitter.py

Splits documents into smaller chunks.

### embedder.py

Creates embeddings from text chunks.

---

## app/retrieval

Handles knowledge searching.

### retriever.py

Responsible for:

* Converting questions into embeddings
* Searching ChromaDB
* Returning relevant CollabFarm information

---

## app/vectorstore

Handles ChromaDB operations.

### chroma.py

Responsible for:

* Connecting to ChromaDB
* Creating collections
* Storing embeddings

---

# Installation Guide

## Requirements

Install the following:

* Python 3.12
* Git
* pip

Python 3.12 is the recommended version for the current project environment.

---

## Clone Repository

Clone the repository:

```bash
git clone <repository-url>
cd collab-farm-ai
```

---

## Create Virtual Environment

Create a Python virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Confirm the Python version:

```powershell
python --version
```

Expected:

```text
Python 3.12.x
```

---

## Install Dependencies

Install the project dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root.

Use `.env.example` as the template.

The Ollama Cloud API key must be configured in the environment before starting the chatbot.

The `.env.example` file lists both required variables. Copy it to `.env` and set your own values:

```text
OLLAMA_API_KEY=your-ollama-cloud-api-key
CHAT_API_KEY=your-long-random-chat-api-secret
```

- `OLLAMA_API_KEY` authenticates requests from this service to Ollama Cloud.
- `CHAT_API_KEY` authenticates callers of the CollabFarm `/chat` API. These are separate keys.

Do not commit the `.env` file or expose either key. Never use the example placeholder as a production secret.

---

# Knowledge Base

The chatbot uses the CollabFarm knowledge stored under:

```text
knowledge/raw/
```

The generated ChromaDB vector database is stored under:

```text
knowledge/chroma_db/
```

The vector database is generated data and should not be treated as the source knowledge itself.

---

# Running the API

Start the FastAPI application with Uvicorn:

```powershell
python -m uvicorn api_main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# Health Check

Open:

```text
http://127.0.0.1:8000/
```

A successful response should look like:

```json
{
  "message": "Status OK"
}
```

---

# API Documentation

FastAPI provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The documentation can be used to inspect and test the available API endpoints.

---

# Chat Endpoint

The chatbot accepts requests through:

```text
POST /chat
```

The request requires a `session_id` and a user `message`.

Example request:

```json
{
  "session_id": "test-session-001",
  "message": "What is CollabFarm?"
}
```

Example PowerShell request:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/chat" `
  -Method Post `
  -Headers @{ "X-API-Key" = "your-chat-api-secret" } `
  -ContentType "application/json" `
  -Body '{"session_id":"test-session-001","message":"What is CollabFarm?"}'
```

The response contains the chatbot's answer.

Example:

```json
{
  "answer": "CollabFarm is an agricultural financing platform..."
}
```

---

# Session Memory

The chatbot uses `session_id` to maintain temporary conversation history. Each session has its own conversation history.

- The chatbot stores at most the **10 most recent messages** per session.
- A session expires after **30 minutes of inactivity**. Expired history is removed when the memory store is next accessed.
- Session memory is held in process memory, so it is cleared when the API process restarts and is not shared between multiple Uvicorn workers. Use a shared store such as Redis or a database if persistent or multi-worker sessions are required.
- If the same question is repeated while its prior question-and-answer pair remains in the recent history, the chatbot returns the previous answer instead of making another AI request.

The backend team should agree on who creates `session_id`, how it is associated with a user, and whether the frontend/backend should call session cleanup when a conversation ends.

---

# Testing

The project includes individual test files for components such as:

* Chatbot
* ChromaDB
* Embeddings
* Knowledge loader
* Retriever
* Text splitter

The project also contains an evaluation suite under:

```text
eval/
```

The 30-question baseline test can be run with:

```powershell
python eval\run_baseline.py
```

Results are saved to:

```text
eval\baseline_results.json
```

The keyword checker can be run with:

```powershell
python eval\check_results.py
```

---

# Current Baseline Test

The chatbot has been tested against 30 questions covering:

* Platform overview
* Cooperatives
* Farmers
* Farms
* Farming cycles
* Funding
* Investors
* Investments
* Disbursement
* Settlement
* Transparency
* Greetings
* Thanks
* Unsupported questions

The latest test completed:

**30/30 questions successfully**

The automated keyword checker recorded:

**27/30 (90%)**

Three keyword reviews were identified as valid responses rather than actual chatbot failures:

* The funding-model question correctly returned that the information was unavailable.
* The greeting response was valid even without the exact keyword `hi`.
* The response to the thank-you message was valid even without the exact keyword `thank`.

Therefore, the keyword score should not be treated as the chatbot's actual accuracy score.

---

# Development Notes

The chatbot is designed to answer using CollabFarm-specific knowledge.

When information is not available in the current knowledge, the assistant should not invent an answer.

The configured fallback response is:

```text
The information is not available in the current CollabFarm knowledge.
```

The system should prioritize accurate, grounded responses over speculative answers.
