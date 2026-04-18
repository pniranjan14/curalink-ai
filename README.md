<div align="center">

# 🩺 CuraLink
### AI-Powered Medical Research Assistant

**Research-backed. Hallucination-free. Real-time.**

[![Live Demo](https://curalink-ai-nu.vercel.app/)](YOUR_DEPLOYED_URL)
[![Demo Video](https://www.loom.com/share/5e4204238d814b0fa52a4b3d4ebc81c4)](YOUR_LOOM_LINK)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react)

</div>

---

## 📌 What is CuraLink?

CuraLink is a full-stack AI medical research companion that helps patients, researchers, and clinicians find **real, research-backed insights** about any disease — sourced live from the world's top medical databases.

Unlike generic AI chatbots that rely on pre-trained knowledge (and hallucinate), CuraLink **fetches real data in real-time** from PubMed, OpenAlex, and ClinicalTrials.gov — then uses an LLM purely to synthesize and explain those results in plain language.

> **Input:** Disease + Location  
> **Output:** Top research publications + relevant clinical trials + a clear, cited explanation

---

## ✨ Key Features

- 🔍 **Zero Hallucination** — LLM only uses live-fetched research data, never its training memory
- ⚡ **Parallel API Retrieval** — PubMed, OpenAlex & ClinicalTrials.gov queried simultaneously
- 🧠 **Groq-Powered Context Extraction** — Ultra-fast disease & location detection from natural language
- 📊 **BM25 Ranking** — Fetches up to 60 results, ranks and filters to the most relevant ones
- 💬 **Multi-Turn Conversations** — Full context memory across the session via Supabase
- 🌍 **Location-Aware Trials** — Finds clinical trials geographically relevant to the user
- 📄 **Source Transparency** — Every response cites specific paper titles and NCT IDs

---

## 🏗️ Architecture

```
User Message
     │
     ▼
┌─────────────────────┐
│  Groq LLM           │  ← Extracts disease + location in milliseconds
└─────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Parallel Data Retrieval             │
│  PubMed API  │  OpenAlex API  │  ClinicalTrials.gov  │
└─────────────────────────────────────────────┘
     │  (up to 60 raw results)
     ▼
┌─────────────────────┐
│   BM25 Ranking      │  ← Scores & filters to top 8–10 results
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  LLM Synthesis      │  ← Generates cited, human-readable response
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Supabase           │  ← Saves conversation for context persistence
└─────────────────────┘
     │
     ▼
  Response to User (with publications + trials sidebar)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19 + Vite + Tailwind CSS |
| Backend | Django 4.2 + Django REST Framework |
| LLM (Extraction) | Groq (LLaMA 3 / Mistral — ultra-fast inference) |
| LLM (Synthesis) | Ollama / Open-Source LLM |
| Ranking | BM25 (`rank-bm25`) |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Database | Supabase (PostgreSQL) |
| Data Sources | PubMed (NCBI), OpenAlex, ClinicalTrials.gov |
| Deployment | Vercel (Frontend) + Render/Railway (Backend) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.ai) installed locally
- Supabase account (free tier works)
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/curalink.git
cd curalink
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key

# Groq
GROQ_API_KEY=your-groq-api-key

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Supabase
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key

# API URLs
PUBMED_BASE_URL=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
OPENALEX_BASE_URL=https://api.openalex.org
CLINICALTRIALS_BASE_URL=https://clinicaltrials.gov/api/v2

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver 8000
```

### 3. LLM Setup (Ollama)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull mistral

# Start the server
ollama serve
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` folder:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Start the dev server:

```bash
npm run dev
```

### 5. Open the App

Visit `http://localhost:5173` and try a query like:

> *"I have lung cancer and I'm in Mumbai"*

---

## 📁 Project Structure

```
curalink/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── curalink/          # Django config
│   └── api/
│       ├── views.py       # Chat endpoint
│       ├── models.py      # Conversation & Message models
│       ├── serializers.py
│       └── services/
│           ├── pubmed_service.py
│           ├── openalex_service.py
│           ├── clinicaltrials_service.py
│           ├── ranking_service.py
│           └── llm_service.py
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── ChatWindow.jsx
        │   ├── ChatMessage.jsx
        │   ├── InputBar.jsx
        │   ├── ResearchCard.jsx
        │   ├── ClinicalTrialCard.jsx
        │   └── Sidebar.jsx
        ├── hooks/useChat.js
        ├── store/chatStore.js
        └── services/api.js
```

---

## 🔌 Data Sources

| Source | What it provides | API Docs |
|---|---|---|
| [PubMed (NCBI)](https://pubmed.ncbi.nlm.nih.gov/) | Peer-reviewed medical research papers | [E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/) |
| [OpenAlex](https://openalex.org/) | Open-access academic works | [OpenAlex API](https://docs.openalex.org/) |
| [ClinicalTrials.gov](https://clinicaltrials.gov/) | Ongoing & completed clinical studies | [ClinicalTrials API v2](https://clinicaltrials.gov/data-api/api) |

All three are **free and open** — no paid API keys required for data retrieval.

---

## 💡 Example Queries

```
"I have melanoma and I'm in Berlin"
"Diagnosed with Type 2 Diabetes, located in London"
"Parkinson's disease treatment options, New York"
"Latest research on glioblastoma in India"
```

**Follow-up questions (context-aware):**
```
"Are there any recruiting trials near me?"
"What are the latest treatment options?"
"Can you explain the first paper in simpler terms?"
```

---

## 🌐 Deployment

### Backend (Render / Railway)

```bash
# Procfile
web: gunicorn curalink.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

Set all `.env` variables in your hosting provider's environment settings.

### Frontend (Vercel)

```bash
npm run build
# Deploy the dist/ folder to Vercel
# Set VITE_API_BASE_URL to your deployed backend URL
```

---

## 🤝 Built For

> **CuraLink Hackathon v2.0** — organized by Humanity Founder  
> Built as part of a hiring challenge to demonstrate AI engineering and full-stack development skills.

---

## ⚠️ Disclaimer

CuraLink is a research tool and prototype. It is **not a substitute for professional medical advice**. Always consult a qualified healthcare professional for medical decisions.

---

<div align="center">

Made with ❤️ by **P Niranajn**

</div>
