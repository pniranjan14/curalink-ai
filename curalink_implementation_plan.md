# CuraLink — AI Medical Research Assistant
## Complete Implementation Plan

> Stack: React (Frontend) + Django + Django REST Framework (Backend) + Open-Source LLM (Ollama/HuggingFace)

---

## 📁 PROJECT STRUCTURE

```
curalink/
├── backend/                        # Django Project
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── curalink/                   # Django project config
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── api/                        # Main Django app
│       ├── __init__.py
│       ├── urls.py
│       ├── views.py
│       ├── models.py
│       ├── serializers.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── pubmed_service.py
│       │   ├── openalex_service.py
│       │   ├── clinicaltrials_service.py
│       │   ├── llm_service.py
│       │   └── ranking_service.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
│
└── frontend/                       # React Project
    ├── package.json
    ├── .env
    ├── public/
    │   └── index.html
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── components/
        │   ├── ChatWindow.jsx
        │   ├── ChatMessage.jsx
        │   ├── InputBar.jsx
        │   ├── ResearchCard.jsx
        │   ├── ClinicalTrialCard.jsx
        │   ├── Sidebar.jsx
        │   └── LoadingIndicator.jsx
        ├── services/
        │   └── api.js
        ├── hooks/
        │   └── useChat.js
        └── store/
            └── chatStore.js
```

---

## PHASE 1 — BACKEND SETUP

### Step 1.1 — Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install packages
pip install django djangorestframework django-cors-headers python-dotenv \
            requests httpx langchain langchain-community \
            sentence-transformers chromadb ollama openai \
            celery redis django-redis gunicorn
```

### Step 1.2 — Create Django Project

```bash
django-admin startproject curalink backend/
cd backend
python manage.py startapp api
```

### Step 1.3 — backend/requirements.txt

```
django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
python-dotenv==1.0.0
requests==2.31.0
httpx==0.25.0
langchain==0.1.0
langchain-community==0.0.13
sentence-transformers==2.2.2
chromadb==0.4.18
ollama==0.1.7
openai==1.6.1
gunicorn==21.2.0
```

### Step 1.4 — backend/.env

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# LLM Config
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Optional HuggingFace fallback
HUGGINGFACE_API_KEY=your-hf-key-here

# API Base URLs (all free/open)
PUBMED_BASE_URL=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
OPENALEX_BASE_URL=https://api.openalex.org
CLINICALTRIALS_BASE_URL=https://clinicaltrials.gov/api/v2

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Step 1.5 — backend/curalink/settings.py

```python
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'curalink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'curalink.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# LLM Config
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
PUBMED_BASE_URL = os.getenv('PUBMED_BASE_URL')
OPENALEX_BASE_URL = os.getenv('OPENALEX_BASE_URL')
CLINICALTRIALS_BASE_URL = os.getenv('CLINICALTRIALS_BASE_URL')
```

### Step 1.6 — backend/curalink/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

---

## PHASE 2 — BACKEND API SERVICES

### Step 2.1 — backend/api/services/pubmed_service.py

```python
import requests
import os
from django.conf import settings

PUBMED_BASE = settings.PUBMED_BASE_URL

def search_pubmed(disease: str, location: str = "", max_results: int = 50) -> list:
    """
    Search PubMed for research publications related to disease + location.
    Returns list of article metadata dicts.
    """
    query = f"{disease}"
    if location:
        query += f" {location}"

    # Step 1: Get IDs
    search_url = f"{PUBMED_BASE}/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }

    try:
        search_resp = requests.get(search_url, params=search_params, timeout=15)
        search_resp.raise_for_status()
        ids = search_resp.json()["esearchresult"]["idlist"]
    except Exception as e:
        print(f"PubMed search error: {e}")
        return []

    if not ids:
        return []

    # Step 2: Fetch summaries
    summary_url = f"{PUBMED_BASE}/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "json",
    }

    try:
        summary_resp = requests.get(summary_url, params=summary_params, timeout=15)
        summary_resp.raise_for_status()
        result_data = summary_resp.json().get("result", {})
    except Exception as e:
        print(f"PubMed summary error: {e}")
        return []

    articles = []
    for uid in ids:
        item = result_data.get(uid, {})
        if not item:
            continue
        articles.append({
            "source": "PubMed",
            "id": uid,
            "title": item.get("title", "No title"),
            "authors": [a.get("name") for a in item.get("authors", [])],
            "journal": item.get("fulljournalname", ""),
            "pubdate": item.get("pubdate", ""),
            "abstract": "",   # fetched separately if needed
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        })

    return articles


def fetch_abstract(pubmed_id: str) -> str:
    """Fetch abstract text for a single PubMed article."""
    fetch_url = f"{PUBMED_BASE}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "rettype": "abstract",
        "retmode": "text",
    }
    try:
        resp = requests.get(fetch_url, params=params, timeout=10)
        return resp.text.strip()
    except:
        return ""
```

### Step 2.2 — backend/api/services/openalex_service.py

```python
import requests
from django.conf import settings

OPENALEX_BASE = settings.OPENALEX_BASE_URL

def search_openalex(disease: str, location: str = "", max_results: int = 50) -> list:
    """
    Search OpenAlex for open-access research works related to the disease.
    """
    query = f"{disease}"
    if location:
        query += f" {location}"

    url = f"{OPENALEX_BASE}/works"
    params = {
        "search": query,
        "per-page": max_results,
        "sort": "relevance_score:desc",
        "filter": "is_oa:true",   # only open access
        "select": "id,title,authorships,publication_year,primary_location,abstract_inverted_index,doi",
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        works = resp.json().get("results", [])
    except Exception as e:
        print(f"OpenAlex error: {e}")
        return []

    results = []
    for work in works:
        authors = [
            a.get("author", {}).get("display_name", "")
            for a in work.get("authorships", [])
        ]
        location_info = work.get("primary_location") or {}
        source = location_info.get("source") or {}
        results.append({
            "source": "OpenAlex",
            "id": work.get("id", ""),
            "title": work.get("title", "No title"),
            "authors": authors,
            "journal": source.get("display_name", ""),
            "pubdate": str(work.get("publication_year", "")),
            "abstract": _reconstruct_abstract(work.get("abstract_inverted_index", {})),
            "url": work.get("doi", work.get("id", "")),
        })

    return results


def _reconstruct_abstract(inverted_index: dict) -> str:
    """OpenAlex stores abstracts as inverted index — reconstruct to string."""
    if not inverted_index:
        return ""
    positions = {}
    for word, pos_list in inverted_index.items():
        for pos in pos_list:
            positions[pos] = word
    return " ".join(positions[k] for k in sorted(positions.keys()))
```

### Step 2.3 — backend/api/services/clinicaltrials_service.py

```python
import requests
from django.conf import settings

CLINICALTRIALS_BASE = settings.CLINICALTRIALS_BASE_URL

def search_clinical_trials(disease: str, location: str = "", max_results: int = 30) -> list:
    """
    Search ClinicalTrials.gov for studies related to disease + location.
    """
    url = f"{CLINICALTRIALS_BASE}/studies"
    params = {
        "query.cond": disease,
        "query.locn": location if location else None,
        "pageSize": max_results,
        "format": "json",
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,StartDate,CompletionDate,"
                  "BriefSummary,Condition,InterventionName,LocationCity,LocationCountry",
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        studies = resp.json().get("studies", [])
    except Exception as e:
        print(f"ClinicalTrials error: {e}")
        return []

    results = []
    for study in studies:
        proto = study.get("protocolSection", {})
        id_module = proto.get("identificationModule", {})
        status_module = proto.get("statusModule", {})
        desc_module = proto.get("descriptionModule", {})
        design_module = proto.get("designModule", {})

        results.append({
            "source": "ClinicalTrials",
            "nct_id": id_module.get("nctId", ""),
            "title": id_module.get("briefTitle", "No title"),
            "status": status_module.get("overallStatus", ""),
            "phase": ", ".join(design_module.get("phases", [])),
            "start_date": status_module.get("startDateStruct", {}).get("date", ""),
            "completion_date": status_module.get("completionDateStruct", {}).get("date", ""),
            "summary": desc_module.get("briefSummary", ""),
            "url": f"https://clinicaltrials.gov/study/{id_module.get('nctId', '')}",
        })

    return results
```

### Step 2.4 — backend/api/services/ranking_service.py

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load once at module level (cached in memory)
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight, fast
    return _model


def rank_publications(query: str, publications: list, top_k: int = 8) -> list:
    """
    Rank publications by semantic similarity to the user query.
    Returns top_k most relevant publications.
    """
    if not publications:
        return []

    model = get_model()

    # Build text representation for each publication
    pub_texts = []
    for pub in publications:
        text = f"{pub.get('title', '')} {pub.get('abstract', '')} {pub.get('journal', '')}"
        pub_texts.append(text.strip())

    # Encode query and documents
    query_embedding = model.encode([query])
    doc_embeddings = model.encode(pub_texts)

    # Compute cosine similarities
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    # Attach scores and sort
    scored = list(zip(publications, similarities))
    scored.sort(key=lambda x: x[1], reverse=True)

    # Return top_k with score attached
    results = []
    for pub, score in scored[:top_k]:
        pub_copy = dict(pub)
        pub_copy['relevance_score'] = round(float(score), 4)
        results.append(pub_copy)

    return results


def rank_trials(query: str, trials: list, top_k: int = 5) -> list:
    """Rank clinical trials by relevance to query."""
    if not trials:
        return []

    model = get_model()

    trial_texts = []
    for trial in trials:
        text = f"{trial.get('title', '')} {trial.get('summary', '')} {trial.get('phase', '')}"
        trial_texts.append(text.strip())

    query_embedding = model.encode([query])
    doc_embeddings = model.encode(trial_texts)
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    scored = list(zip(trials, similarities))
    scored.sort(key=lambda x: x[1], reverse=True)

    results = []
    for trial, score in scored[:top_k]:
        trial_copy = dict(trial)
        trial_copy['relevance_score'] = round(float(score), 4)
        results.append(trial_copy)

    return results
```

### Step 2.5 — backend/api/services/llm_service.py

```python
import ollama
import json
from django.conf import settings

OLLAMA_MODEL = settings.OLLAMA_MODEL


def build_system_prompt() -> str:
    return """You are CuraLink, an AI-powered medical research assistant.
Your role is to help users understand their medical condition by providing 
research-backed insights drawn from real publications and clinical trials.

Guidelines:
- Always base your answers on the provided research publications and clinical trials.
- Be clear, compassionate, and non-alarmist.
- Mention specific paper titles or trial names when relevant.
- If data is insufficient, say so honestly.
- Never replace professional medical advice — always recommend consulting a doctor.
- Maintain context from previous messages in the conversation.
"""


def build_research_context(publications: list, trials: list) -> str:
    """Format fetched research data into a context string for the LLM."""
    context_parts = []

    if publications:
        context_parts.append("=== RELEVANT RESEARCH PUBLICATIONS ===")
        for i, pub in enumerate(publications[:8], 1):
            context_parts.append(
                f"{i}. [{pub.get('source')}] {pub.get('title', 'Untitled')}\n"
                f"   Authors: {', '.join(pub.get('authors', [])[:3])}\n"
                f"   Journal: {pub.get('journal', 'N/A')} | Date: {pub.get('pubdate', 'N/A')}\n"
                f"   Abstract: {pub.get('abstract', 'Not available')[:300]}...\n"
                f"   URL: {pub.get('url', '')}\n"
            )

    if trials:
        context_parts.append("\n=== RELEVANT CLINICAL TRIALS ===")
        for i, trial in enumerate(trials[:5], 1):
            context_parts.append(
                f"{i}. {trial.get('title', 'Untitled')}\n"
                f"   Status: {trial.get('status', 'N/A')} | Phase: {trial.get('phase', 'N/A')}\n"
                f"   Summary: {trial.get('summary', 'Not available')[:300]}...\n"
                f"   URL: {trial.get('url', '')}\n"
            )

    return "\n".join(context_parts)


def generate_response(
    user_message: str,
    conversation_history: list,
    publications: list,
    trials: list,
    disease: str,
    location: str,
) -> str:
    """
    Generate LLM response using Ollama with research context injected.
    conversation_history: list of {"role": "user"/"assistant", "content": "..."}
    """
    research_context = build_research_context(publications, trials)

    # Build messages array for Ollama
    messages = [
        {
            "role": "system",
            "content": build_system_prompt()
        }
    ]

    # Add conversation history (last 10 turns for context window)
    for msg in conversation_history[-10:]:
        messages.append(msg)

    # Build the current user message with injected research
    augmented_user_message = f"""User Query: {user_message}

Disease Context: {disease}
Location Context: {location if location else "Not specified"}

{research_context}

Based on the above research publications and clinical trials, please provide a helpful, 
accurate, and research-backed response to the user's query.
"""

    messages.append({
        "role": "user",
        "content": augmented_user_message
    })

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            options={
                "temperature": 0.3,   # lower = more factual
                "num_predict": 800,
            }
        )
        return response['message']['content']

    except Exception as e:
        print(f"Ollama error: {e}")
        # Fallback: return a structured response without LLM
        return _fallback_response(disease, publications, trials)


def extract_disease_and_location(user_message: str) -> dict:
    """
    Use LLM to extract disease and location from user message.
    Returns {"disease": "...", "location": "..."}
    """
    prompt = f"""Extract the medical condition/disease and location from this message.
Return ONLY a JSON object with keys "disease" and "location".
If location is not mentioned, use empty string.

Message: "{user_message}"

JSON:"""

    try:
        response = ollama.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            options={"temperature": 0, "num_predict": 100}
        )
        text = response['response'].strip()
        # Clean up potential markdown fences
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        # Simple keyword fallback
        return {"disease": user_message, "location": ""}


def _fallback_response(disease: str, publications: list, trials: list) -> str:
    """Fallback when LLM is unavailable."""
    response = f"Here are the research results I found for **{disease}**:\n\n"
    if publications:
        response += f"Found {len(publications)} relevant publications. "
    if trials:
        response += f"Found {len(trials)} relevant clinical trials. "
    response += "\n\nPlease consult a medical professional for personalized advice."
    return response
```

---

## PHASE 3 — DJANGO MODELS, VIEWS & URLs

### Step 3.1 — backend/api/models.py

```python
from django.db import models
import uuid


class Conversation(models.Model):
    """Store conversation sessions."""
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    disease = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.session_id} - {self.disease}"


class Message(models.Model):
    """Individual messages within a conversation."""
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
```

### Step 3.2 — backend/api/serializers.py

```python
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['session_id', 'disease', 'location', 'created_at', 'messages']


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    session_id = serializers.UUIDField(required=False, allow_null=True)


class ChatResponseSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    response = serializers.CharField()
    publications = serializers.ListField()
    trials = serializers.ListField()
    disease = serializers.CharField()
    location = serializers.CharField()
```

### Step 3.3 — backend/api/views.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ChatRequestSerializer
from .services.pubmed_service import search_pubmed
from .services.openalex_service import search_openalex
from .services.clinicaltrials_service import search_clinical_trials
from .services.ranking_service import rank_publications, rank_trials
from .services.llm_service import generate_response, extract_disease_and_location
import uuid


class ChatView(APIView):
    """Main chat endpoint — processes user message and returns research-backed response."""

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id')

        # Get or create conversation session
        if session_id:
            conversation, _ = Conversation.objects.get_or_create(session_id=session_id)
        else:
            conversation = Conversation.objects.create()

        # Build conversation history for LLM
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages.all()
        ]

        # Extract or update disease/location
        if not conversation.disease:
            extracted = extract_disease_and_location(user_message)
            conversation.disease = extracted.get('disease', user_message)
            conversation.location = extracted.get('location', '')
            conversation.save()
        else:
            # Check if user is updating disease/location in follow-up
            if any(kw in user_message.lower() for kw in ['disease', 'condition', 'suffering', 'diagnosed', 'located', 'city', 'country']):
                extracted = extract_disease_and_location(user_message)
                if extracted.get('disease'):
                    conversation.disease = extracted['disease']
                if extracted.get('location'):
                    conversation.location = extracted['location']
                conversation.save()

        disease = conversation.disease
        location = conversation.location

        # Fetch research data from all 3 sources in parallel (or sequential)
        pubmed_results = search_pubmed(disease, location, max_results=50)
        openalex_results = search_openalex(disease, location, max_results=50)
        trial_results = search_clinical_trials(disease, location, max_results=30)

        # Combine publications from both sources
        all_publications = pubmed_results + openalex_results

        # Rank & filter
        ranked_publications = rank_publications(user_message, all_publications, top_k=8)
        ranked_trials = rank_trials(user_message, trial_results, top_k=5)

        # Generate LLM response
        llm_response = generate_response(
            user_message=user_message,
            conversation_history=history,
            publications=ranked_publications,
            trials=ranked_trials,
            disease=disease,
            location=location,
        )

        # Save messages to DB
        Message.objects.create(conversation=conversation, role='user', content=user_message)
        Message.objects.create(conversation=conversation, role='assistant', content=llm_response)

        return Response({
            'session_id': str(conversation.session_id),
            'response': llm_response,
            'publications': ranked_publications,
            'trials': ranked_trials,
            'disease': disease,
            'location': location,
        })


class ConversationHistoryView(APIView):
    """Retrieve full conversation history for a session."""

    def get(self, request, session_id):
        try:
            conversation = Conversation.objects.get(session_id=session_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Session not found'}, status=404)

        messages = [
            {'role': msg.role, 'content': msg.content, 'created_at': msg.created_at}
            for msg in conversation.messages.all()
        ]
        return Response({
            'session_id': str(conversation.session_id),
            'disease': conversation.disease,
            'location': conversation.location,
            'messages': messages,
        })


class HealthCheckView(APIView):
    """Simple health check endpoint."""

    def get(self, request):
        return Response({'status': 'ok', 'service': 'CuraLink API'})
```

### Step 3.4 — backend/api/urls.py

```python
from django.urls import path
from .views import ChatView, ConversationHistoryView, HealthCheckView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('conversation/<uuid:session_id>/', ConversationHistoryView.as_view(), name='conversation-history'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
```

---

## PHASE 4 — FRONTEND REACT SETUP

### Step 4.1 — Create React App

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install axios uuid react-markdown lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 4.2 — frontend/.env

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Step 4.3 — frontend/tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
        },
        medical: {
          blue: '#0ea5e9',
          dark: '#0f172a',
        }
      }
    },
  },
  plugins: [],
}
```

### Step 4.4 — frontend/src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #0f172a;
  color: #f1f5f9;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #1e293b;
}

::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 3px;
}

.chat-message {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Step 4.5 — frontend/src/services/api.js

```js
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,  // 60s — LLM can be slow
});

export const sendMessage = async (message, sessionId = null) => {
  const payload = { message };
  if (sessionId) payload.session_id = sessionId;

  const { data } = await apiClient.post('/chat/', payload);
  return data;
};

export const getConversationHistory = async (sessionId) => {
  const { data } = await apiClient.get(`/conversation/${sessionId}/`);
  return data;
};
```

### Step 4.6 — frontend/src/store/chatStore.js

```js
import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';

const getStoredSessionId = () => localStorage.getItem('curalink_session_id');
const storeSessionId = (id) => localStorage.setItem('curalink_session_id', id);

export const useChatStore = () => {
  const [sessionId, setSessionId] = useState(getStoredSessionId());
  const [messages, setMessages] = useState([]);
  const [publications, setPublications] = useState([]);
  const [trials, setTrials] = useState([]);
  const [disease, setDisease] = useState('');
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const addMessage = useCallback((role, content) => {
    setMessages(prev => [...prev, { id: uuidv4(), role, content, timestamp: new Date() }]);
  }, []);

  const updateSession = useCallback((data) => {
    if (data.session_id && data.session_id !== sessionId) {
      setSessionId(data.session_id);
      storeSessionId(data.session_id);
    }
    if (data.publications) setPublications(data.publications);
    if (data.trials) setTrials(data.trials);
    if (data.disease) setDisease(data.disease);
    if (data.location) setLocation(data.location);
  }, [sessionId]);

  const clearSession = useCallback(() => {
    localStorage.removeItem('curalink_session_id');
    setSessionId(null);
    setMessages([]);
    setPublications([]);
    setTrials([]);
    setDisease('');
    setLocation('');
  }, []);

  return {
    sessionId, messages, publications, trials, disease, location,
    loading, error, setLoading, setError,
    addMessage, updateSession, clearSession,
  };
};
```

### Step 4.7 — frontend/src/hooks/useChat.js

```js
import { useCallback } from 'react';
import { sendMessage } from '../services/api';

export const useChat = (store) => {
  const { sessionId, addMessage, updateSession, setLoading, setError } = store;

  const handleSend = useCallback(async (userMessage) => {
    if (!userMessage.trim()) return;

    addMessage('user', userMessage);
    setLoading(true);
    setError(null);

    try {
      const data = await sendMessage(userMessage, sessionId);
      addMessage('assistant', data.response);
      updateSession(data);
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Something went wrong. Please try again.';
      setError(errMsg);
      addMessage('assistant', `Error: ${errMsg}`);
    } finally {
      setLoading(false);
    }
  }, [sessionId, addMessage, updateSession, setLoading, setError]);

  return { handleSend };
};
```

### Step 4.8 — frontend/src/components/ResearchCard.jsx

```jsx
import React, { useState } from 'react';
import { ExternalLink, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

const ResearchCard = ({ pub }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-green-500/50 transition-all duration-200">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 mb-2">
          <BookOpen size={14} className="text-green-400 flex-shrink-0" />
          <span className="text-xs font-medium text-green-400 bg-green-400/10 px-2 py-0.5 rounded-full">
            {pub.source}
          </span>
          {pub.relevance_score && (
            <span className="text-xs text-slate-400">
              {Math.round(pub.relevance_score * 100)}% match
            </span>
          )}
        </div>
        <a
          href={pub.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-slate-400 hover:text-green-400 flex-shrink-0"
        >
          <ExternalLink size={14} />
        </a>
      </div>

      <h4 className="text-sm font-semibold text-white leading-snug mb-2 line-clamp-2">
        {pub.title}
      </h4>

      {pub.authors?.length > 0 && (
        <p className="text-xs text-slate-400 mb-1">
          {pub.authors.slice(0, 2).join(', ')}
          {pub.authors.length > 2 ? ` +${pub.authors.length - 2} more` : ''}
        </p>
      )}

      {pub.journal && (
        <p className="text-xs text-slate-500 italic mb-2">
          {pub.journal} · {pub.pubdate}
        </p>
      )}

      {pub.abstract && (
        <>
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-sky-400 flex items-center gap-1 hover:text-sky-300"
          >
            {expanded ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
            {expanded ? 'Hide abstract' : 'Show abstract'}
          </button>
          {expanded && (
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              {pub.abstract.slice(0, 400)}...
            </p>
          )}
        </>
      )}
    </div>
  );
};

export default ResearchCard;
```

### Step 4.9 — frontend/src/components/ClinicalTrialCard.jsx

```jsx
import React from 'react';
import { ExternalLink, Activity } from 'lucide-react';

const statusColor = {
  'RECRUITING': 'text-green-400 bg-green-400/10',
  'COMPLETED': 'text-blue-400 bg-blue-400/10',
  'ACTIVE, NOT RECRUITING': 'text-yellow-400 bg-yellow-400/10',
  'TERMINATED': 'text-red-400 bg-red-400/10',
};

const ClinicalTrialCard = ({ trial }) => {
  const colorClass = statusColor[trial.status] || 'text-slate-400 bg-slate-400/10';

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-sky-500/50 transition-all duration-200">
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <Activity size={14} className="text-sky-400 flex-shrink-0" />
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${colorClass}`}>
            {trial.status}
          </span>
        </div>
        <a
          href={trial.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-slate-400 hover:text-sky-400 flex-shrink-0"
        >
          <ExternalLink size={14} />
        </a>
      </div>

      <h4 className="text-sm font-semibold text-white leading-snug mb-2">
        {trial.title}
      </h4>

      <div className="flex gap-3 text-xs text-slate-400 mb-2">
        {trial.phase && <span>Phase: {trial.phase}</span>}
        {trial.start_date && <span>Start: {trial.start_date}</span>}
      </div>

      {trial.summary && (
        <p className="text-xs text-slate-400 leading-relaxed line-clamp-3">
          {trial.summary}
        </p>
      )}

      <p className="text-xs text-slate-600 mt-2 font-mono">{trial.nct_id}</p>
    </div>
  );
};

export default ClinicalTrialCard;
```

### Step 4.10 — frontend/src/components/ChatMessage.jsx

```jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`chat-message flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} mb-6`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
        ${isUser ? 'bg-green-500' : 'bg-sky-600'}`}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Bubble */}
      <div className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed
        ${isUser
          ? 'bg-green-600 text-white rounded-tr-none'
          : 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700'
        }`}>
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
              ul: ({ children }) => <ul className="list-disc ml-4 mb-2 space-y-1">{children}</ul>,
              li: ({ children }) => <li>{children}</li>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
        <span className="text-xs opacity-50 mt-1 block text-right">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
};

export default ChatMessage;
```

### Step 4.11 — frontend/src/components/InputBar.jsx

```jsx
import React, { useState, useRef } from 'react';
import { Send, Loader2 } from 'lucide-react';

const InputBar = ({ onSend, loading }) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    if (!value.trim() || loading) return;
    onSend(value.trim());
    setValue('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-slate-800 bg-slate-900 p-4">
      <div className="flex gap-3 items-end max-w-4xl mx-auto">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe your disease and location (e.g., 'I have lung cancer and I'm in Mumbai')..."
          rows={2}
          className="flex-1 resize-none bg-slate-800 border border-slate-700 rounded-xl px-4 py-3
                     text-sm text-white placeholder-slate-500 focus:outline-none focus:border-green-500
                     transition-colors duration-200"
          disabled={loading}
        />
        <button
          onClick={handleSubmit}
          disabled={loading || !value.trim()}
          className="flex-shrink-0 w-10 h-10 rounded-xl bg-green-500 hover:bg-green-600
                     disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center
                     transition-colors duration-200"
        >
          {loading ? (
            <Loader2 size={18} className="animate-spin" />
          ) : (
            <Send size={18} />
          )}
        </button>
      </div>
      <p className="text-xs text-slate-600 text-center mt-2">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  );
};

export default InputBar;
```

### Step 4.12 — frontend/src/components/Sidebar.jsx

```jsx
import React from 'react';
import ResearchCard from './ResearchCard';
import ClinicalTrialCard from './ClinicalTrialCard';
import { BookOpen, FlaskConical, MapPin, Stethoscope } from 'lucide-react';

const Sidebar = ({ publications, trials, disease, location }) => {
  return (
    <div className="w-96 flex-shrink-0 border-l border-slate-800 bg-slate-900 overflow-y-auto flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-slate-800">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <BookOpen size={16} className="text-green-400" />
          Research Panel
        </h2>
        {disease && (
          <div className="flex gap-2 mt-2 flex-wrap">
            <span className="text-xs flex items-center gap-1 text-slate-400">
              <Stethoscope size={11} /> {disease}
            </span>
            {location && (
              <span className="text-xs flex items-center gap-1 text-slate-400">
                <MapPin size={11} /> {location}
              </span>
            )}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Publications */}
        {publications.length > 0 && (
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              <BookOpen size={12} />
              Publications ({publications.length})
            </h3>
            <div className="space-y-3">
              {publications.map((pub, i) => (
                <ResearchCard key={pub.id || i} pub={pub} />
              ))}
            </div>
          </div>
        )}

        {/* Clinical Trials */}
        {trials.length > 0 && (
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              <FlaskConical size={12} />
              Clinical Trials ({trials.length})
            </h3>
            <div className="space-y-3">
              {trials.map((trial, i) => (
                <ClinicalTrialCard key={trial.nct_id || i} trial={trial} />
              ))}
            </div>
          </div>
        )}

        {/* Empty state */}
        {publications.length === 0 && trials.length === 0 && (
          <div className="text-center py-12">
            <BookOpen size={32} className="text-slate-700 mx-auto mb-3" />
            <p className="text-sm text-slate-600">
              Research results will appear here after your first message.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
```

### Step 4.13 — frontend/src/components/ChatWindow.jsx

```jsx
import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import { Bot } from 'lucide-react';

const ChatWindow = ({ messages, loading }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="flex-1 overflow-y-auto p-6">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center">
          <div className="w-16 h-16 rounded-2xl bg-green-500/10 flex items-center justify-center mb-4">
            <Bot size={32} className="text-green-400" />
          </div>
          <h2 className="text-xl font-semibold text-white mb-2">CuraLink</h2>
          <p className="text-slate-400 text-sm max-w-sm">
            Your AI-powered medical research companion. Tell me your disease and location to get
            research-backed insights from real publications and clinical trials.
          </p>
          <div className="mt-6 grid grid-cols-1 gap-2 w-full max-w-sm">
            {[
              "I have lung cancer and I'm in Mumbai",
              "I'm diagnosed with type 2 diabetes in London",
              "Parkinson's disease, located in New York",
            ].map((example) => (
              <button
                key={example}
                className="text-left text-xs text-slate-400 border border-slate-700 rounded-lg px-3 py-2
                           hover:border-green-500/50 hover:text-white transition-all duration-200"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg} />
      ))}

      {loading && (
        <div className="flex gap-3 mb-6">
          <div className="w-8 h-8 rounded-full bg-sky-600 flex items-center justify-center flex-shrink-0">
            <Bot size={16} />
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-tl-none px-4 py-3">
            <div className="flex gap-1 items-center">
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0ms]" />
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:150ms]" />
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:300ms]" />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};

export default ChatWindow;
```

### Step 4.14 — frontend/src/App.jsx

```jsx
import React from 'react';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import Sidebar from './components/Sidebar';
import { useChatStore } from './store/chatStore';
import { useChat } from './hooks/useChat';
import { RefreshCw, Heart } from 'lucide-react';

function App() {
  const store = useChatStore();
  const { handleSend } = useChat(store);
  const { messages, publications, trials, disease, location, loading, clearSession } = store;

  return (
    <div className="flex flex-col h-screen bg-slate-950">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-3 border-b border-slate-800 bg-slate-900">
        <div className="flex items-center gap-2">
          <Heart size={20} className="text-green-400" />
          <span className="text-white font-semibold tracking-tight">CuraLink</span>
          <span className="text-xs text-slate-500 ml-1">Medical Research Assistant</span>
        </div>
        <button
          onClick={clearSession}
          className="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
        >
          <RefreshCw size={12} />
          New Session
        </button>
      </header>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Chat area */}
        <div className="flex flex-col flex-1 overflow-hidden">
          <ChatWindow messages={messages} loading={loading} />
          <InputBar onSend={handleSend} loading={loading} />
        </div>

        {/* Research sidebar */}
        <Sidebar
          publications={publications}
          trials={trials}
          disease={disease}
          location={location}
        />
      </div>
    </div>
  );
}

export default App;
```

---

## PHASE 5 — LLM SETUP (OLLAMA)

### Step 5.1 — Install Ollama & Pull a Model

```bash
# Install Ollama (Linux/Mac)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a free open-source medical-capable model
ollama pull mistral          # 7B, good quality, fast
# OR
ollama pull llama3           # better quality, heavier
# OR
ollama pull meditron         # specifically medical-focused (if available)

# Start Ollama server
ollama serve
```

### Step 5.2 — Test Ollama Connection

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "mistral",
  "messages": [{"role": "user", "content": "What is lung cancer?"}]
}'
```

---

## PHASE 6 — DATABASE & MIGRATIONS

```bash
cd backend
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser   # optional, for admin panel
```

---

## PHASE 7 — RUN THE PROJECT

### Terminal 1 — Start Ollama LLM server
```bash
ollama serve
```

### Terminal 2 — Start Django backend
```bash
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

### Terminal 3 — Start React frontend
```bash
cd frontend
npm run dev
```

Visit: `http://localhost:5173`

---

## PHASE 8 — DEPLOYMENT

### 8.1 — Backend Deployment (Render / Railway / VPS)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn curalink.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Procfile** (for Render/Railway):
```
web: gunicorn curalink.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

**backend/curalink/settings.py** — update for production:
```python
# Add these for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
ALLOWED_HOSTS = ['*']   # restrict to your domain in production
```

### 8.2 — Frontend Deployment (Vercel / Netlify)

```bash
cd frontend
npm run build   # creates dist/ folder

# Deploy dist/ to Vercel or Netlify
# Update VITE_API_BASE_URL to your deployed backend URL
```

### 8.3 — Ollama on Server

Option A — Use a free HuggingFace Inference API as fallback:
```python
# In llm_service.py, fallback to HuggingFace if Ollama fails
import openai

hf_client = openai.OpenAI(
    base_url="https://api-inference.huggingface.co/v1",
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
)

response = hf_client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=messages,
    max_tokens=800,
)
```

Option B — Deploy Ollama on a GPU server (Vast.ai, RunPod, etc.) and update `OLLAMA_BASE_URL`.

---

## PHASE 9 — TESTING CHECKLIST

```
✅ User types disease + location → backend extracts them correctly
✅ PubMed API returns results for that disease
✅ OpenAlex API returns results for that disease
✅ ClinicalTrials API returns trial results
✅ Ranking service orders results by relevance
✅ LLM generates a coherent, research-backed response
✅ Response appears in chat UI
✅ Publications and trials appear in sidebar
✅ Follow-up questions maintain context
✅ New session button resets everything
✅ Deployed link is publicly accessible
```

---

## QUICK SUMMARY — ORDER OF EXECUTION

```
1. Setup Django project + install packages
2. Create .env files for both frontend and backend
3. Copy all service files (pubmed, openalex, clinicaltrials, ranking, llm)
4. Create Django models + run migrations
5. Setup urls.py and views.py
6. Install Ollama + pull mistral model
7. Setup React project + install packages
8. Copy all component files
9. Run all 3 terminals (ollama + django + react)
10. Test with sample queries
11. Deploy backend → get URL → update frontend .env → deploy frontend
```

---

*Built for CuraLink Hackathon v2.0 — Good luck! 🚀*
