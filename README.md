# 📦 Hyper-Personalized Retail Support Agent  
### **(RAG + Tools + LLM Orchestration + PII Safety + Groq Integration)**

This repository contains a complete backend system for a **hyper-personalized conversational retail assistant**.  
It combines **RAG**, **real-time user context**, **tool integrations**, and **privacy-safe LLM reasoning** powered by **Groq Llama-3.3**.

---

# 🌟 What This System Does

This backend is designed for modern retail use-cases where customers expect:

- **Instant answers**
- **Personalized support**
- **Grounded responses**
- **Real-time recommendations**
- **Location-aware suggestions**

Example:

**User:** *“I'm cold.”*  
**Bot:** *“There’s a Starbucks 50m away. You also have a 10% coupon for Hot Cocoa. Want directions?”*

---

# 🧠 Key Features

## ✔️ Retrieval-Augmented Generation (RAG)
- Ingests multiple internal documents (policies, return rules, loyalty terms, coupons)
- Splits into chunks for optimized retrieval
- Embeds using `bge-small-en-v1.5`
- Stores in a **FAISS vector database**
- Retrieves relevant text for grounding every answer

## ✔️ Real-Time Retail Tools
The backend simulates real production tools:

- **Nearby Store Finder** (uses user GPS)
- **Personalized Coupon Engine**
- **Order Status Checker**
- **Inventory Availability Lookup**

These are included in each LLM prompt to create **actionable**, not generic, responses.

## ✔️ Privacy & PII Masking (Mandatory)
Before any data reaches the LLM, sensitive fields are masked:

- Phone numbers  
- Emails  
- Names  
- Addresses  
- Payment identifiers  

This ensures compliance and safe external LLM usage.

## ✔️ Orchestration Layer (Brain of the System)
A custom orchestrator handles:

1. Input validation  
2. Privacy filtering  
3. Tool execution  
4. RAG retrieval  
5. Prompt construction  
6. Groq LLM generation  
7. Final response formatting  

This ensures the agent is grounded, safe, and context-aware.

## ✔️ LLM Backend: Groq (FREE + FAST)
This project uses:

**`llama-3.3-70b-versatile` via GroqCloud**

Advantages:

- Free development tier  
- Extremely low latency  
- High-quality model outputs  
- No GPU/CPU dependency on your machine  

The LLM can be changed in:  
`src/config.py`

---

# 🏗️ Architecture Overview

```
                ┌─────────────────────────┐
                │        User Query       │
                └──────────────┬──────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │ FastAPI Backend   │
                    └───────┬───────────┘
                            │
                 ┌──────────┴───────────┐
                 ▼                      ▼
    ┌─────────────────────┐   ┌──────────────────────┐
    │ PII Masking Layer   │   │ Tool Executor        │
    │ (privacy filter)    │   │ (stores, coupons…)   │
    └─────────────────────┘   └──────────────────────┘
                 │                      │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ RAG Retriever        │
                 │ (FAISS + embeddings) │
                 └──────────────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Prompt Orchestrator  │
                 │ (system + tools +    │
                 │   rag + user prompt) │
                 └──────────────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Groq LLM API         │
                 │ llama-3.3-70b        │
                 └──────────────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Final Response     │
                 └──────────────────────┘
```

---

# 📁 Project Structure

```
hyper-personalized-support-bot/
│
├── data/
│   ├── raw_docs/        # RAG source documents (.txt)
│   └── vector_store/    # FAISS index + metadata
│
├── src/
│   ├── rag/             # Ingestion + retrieval pipeline
│   ├── models/          # Groq LLM wrapper + embeddings
│   ├── app/             # FastAPI server + orchestration
│   ├── utils/           # PII masking, helpers
│   └── config.py        # Global configuration
│
├── main.py              # FastAPI entrypoint
└── README.md            # You're reading this
```

---

# 🚀 Getting Started

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 2️⃣ Add Your Groq API Key

Create `.env` in the project root:

```bash
GROQ_API_KEY=your_groq_key_here
```

## 3️⃣ Build the Vector Database

Place policy documents in `data/raw_docs/`

Then run:

```bash
python -m src.rag.ingest
```

## 4️⃣ Start the Server

```bash
python main.py
```

Server runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

---

# 🧪 Example API Call

```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -d '{
    "user_id": "u123",
    "message": "What is the return policy?",
    "lat": 19.07,
    "lon": 72.87
  }'
```

Example response (real Llama-3.3-70B output via Groq):

```json
{
  "answer": "You can return unopened items within 30 days..."
}
```

---

# 🔧 Configuration

Edit model or settings in:  
`src/config.py`

Example:

```python
LLM_MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
TOP_K = 5
```

---

# ⚙️ RAG Pipeline Details

1. Load .txt documents  
2. Split into overlapping chunks  
3. Embed each using BGE embeddings  
4. Index via FAISS  
5. At query time:
   - embed user question  
   - perform semantic search  
   - inject top-K chunks into the prompt  

This ensures the model **does not hallucinate** and stays aligned to policy.

---

# 🔐 Privacy Enforcement

The system applies regex-based masking to:

- Names  
- Emails  
- Phone numbers  
- Addresses  
- Payment identifiers  

Masked before sending to Groq.  
This meets standard enterprise PII rules.

---

# 📡 Tool Integrations

The orchestrator uses helper functions to simulate real retail systems:

- Distance to nearby stores  
- Available coupons  
- Latest order status  
- Possible inventory availability  

These are added under:

```text
### Real-Time Tools
```

in the final LLM prompt.

---

# 🧩 LLM Prompt Structure

The prompt is constructed as:

```text
System Instructions
User Profile
Real-Time Tools
RAG Context
User Message
```

This layering ensures:

- Accuracy  
- Personalization  
- Actionability  
- Grounded responses  

---

# 🎯 Summary

This project demonstrates a **production-grade architecture** for Conversational Retail AI:

- 🧠 RAG-grounded responses  
- 🔧 Real-time tools  
- 🔐 PII-safe interactions  
- 🚀 Groq-powered LLM  
- ⚡ FastAPI backend  
- 💬 Ready for chatbot UI integration  

It is designed to be easily extended with:

- React chat UI  
- Docker deployment  
- Production LLM endpoints  
- Additional tools (CRM, inventory, loyalty)  

---

# 🗣️ Next Step

You can now connect this backend to:

- A **React Chatbot UI**  
- A mobile app  
- A web widget  
- A kiosk interface  

