# CollabFarm AI Assistant

## Overview

The CollabFarm AI Assistant is a Retrieval-Augmented Generation (RAG) based chatbot that provides users with accurate information about the CollabFarm platform.

The assistant uses approved CollabFarm knowledge sources and an AI language model to answer public platform questions related to:

- Cooperative registration and management
- Investor activities
- Farmer onboarding
- Farm information
- Farming cycles
- Funding opportunities
- Investment tracking
- Settlement processes

The system is designed to provide responses based on CollabFarm-specific knowledge rather than relying only on general AI knowledge.

---

# Architecture Overview

The CollabFarm AI Assistant follows a Retrieval-Augmented Generation (RAG) architecture.

The system retrieves relevant information from the CollabFarm knowledge base, combines it with the user's question, and sends it to the AI model to generate a grounded response.


---

# Technology Stack

## Backend

### Python

Python is used for:

- AI workflow management
- API development
- Knowledge processing
- Retrieval operations

---

## API Framework

### FastAPI

FastAPI provides the backend API layer between the frontend application and the AI assistant.

It handles:

- Receiving user messages
- Managing chat requests
- Returning AI responses
- Providing Swagger API documentation

---

## Large Language Model

### Ollama Cloud

Ollama Cloud provides the language model used for response generation.

Current model: gpt-oss:120b


The model handles:

- Natural language understanding
- Response generation
- Conversational interaction

---

## Retrieval-Augmented Generation Components

### ChromaDB

ChromaDB is used as the vector database.

It stores embedded CollabFarm knowledge and allows the system to search information based on meaning rather than exact keywords.

---

### Sentence Transformers

Sentence Transformers converts knowledge documents into embeddings for semantic search.

Embedding model:all-MiniLM-L6-v2


---

### LangChain Components

LangChain components are used for:

- Text splitting
- Document processing
- RAG workflow support

---

# Project Structure
API-for-LLM/

├── app/
│
│ ├── api/
│ │ ├── init.py
│ │ └── routes.py
│ │
│ ├── chatbot/
│ │ ├── init.py
│ │ ├── chatbot.py
│ │ ├── memory.py
│ │ └── ollama_client.py
│ │
│ ├── ingestion/
│ │ ├── init.py
│ │ ├── loader.py
│ │ ├── splitter.py
│ │ └── embedder.py
│ │
│ ├── retrieval/
│ │ ├── init.py
│ │ └── retriever.py
│ │
│ └── vectorstore/
│ ├── init.py
│ └── chroma.py
│
├── knowledge/
│ ├── raw/
│ └── chroma_db/
│
├── .env
├── .env.example
├── api_main.py
├── main.py
├── requirements.txt
└── README.md

---

# Folder Description

## app/api

Contains the FastAPI communication layer.

Responsible for:

- Receiving frontend requests
- Passing requests to the chatbot
- Returning responses

Main file: routes.py


---

## app/chatbot

Contains chatbot logic.

### chatbot.py

Handles:

- User questions
- Session memory
- Retrieval calls
- Prompt creation
- AI response generation

### memory.py

Handles temporary session-based conversation memory.

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

- Converting questions into embeddings
- Searching ChromaDB
- Returning relevant CollabFarm information

---

## app/vectorstore

Handles ChromaDB operations.

### chroma.py

Responsible for:

- Connecting to ChromaDB
- Creating collections
- Storing embeddings

---

# Installation Guide

## Requirements

Install:

- Python 3.10+
- Git
- pip

---

## Clone Repository  git clone <repository-url>





