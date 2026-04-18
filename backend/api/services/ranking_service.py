from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load once at module level (cached in memory)
_model = None

def get_model():
    global _model
    if _model is None:
        # Load a lightweight, fast model
        _model = SentenceTransformer('all-MiniLM-L6-v2')
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
