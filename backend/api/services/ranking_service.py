from rank_bm25 import BM25Okapi
import re

def tokenize(text):
    """Simple tokenizer for BM25."""
    return re.findall(r'\w+', text.lower())

def rank_publications(query: str, publications: list, top_k: int = 8) -> list:
    """
    Rank publications using BM25 keyword matching.
    Much lighter and faster than semantic models on limited CPUs.
    """
    if not publications:
        return []

    # Prepare corpus for BM25
    corpus = []
    for pub in publications:
        text = f"{pub.get('title', '')} {pub.get('abstract', '')} {pub.get('journal', '')}"
        corpus.append(tokenize(text))

    if not corpus:
        return publications[:top_k]

    bm25 = BM25Okapi(corpus)
    tokenized_query = tokenize(query)
    
    # Get scores
    scores = bm25.get_scores(tokenized_query)
    
    # Attach scores and sort
    scored = list(zip(publications, scores))
    scored.sort(key=lambda x: x[1], reverse=True)

    results = []
    for pub, score in scored[:top_k]:
        pub_copy = dict(pub)
        pub_copy['relevance_score'] = round(float(score), 4)
        results.append(pub_copy)

    return results

def rank_trials(query: str, trials: list, top_k: int = 5) -> list:
    """Rank clinical trials using BM25 keyword matching."""
    if not trials:
        return []

    corpus = []
    for trial in trials:
        text = f"{trial.get('title', '')} {trial.get('summary', '')} {trial.get('phase', '')}"
        corpus.append(tokenize(text))

    if not corpus:
        return trials[:top_k]

    bm25 = BM25Okapi(corpus)
    tokenized_query = tokenize(query)
    
    scores = bm25.get_scores(tokenized_query)
    
    scored = list(zip(trials, scores))
    scored.sort(key=lambda x: x[1], reverse=True)

    results = []
    for trial, score in scored[:top_k]:
        trial_copy = dict(trial)
        trial_copy['relevance_score'] = round(float(score), 4)
        results.append(trial_copy)

    return results
