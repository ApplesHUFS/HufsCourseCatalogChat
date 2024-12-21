from typing import List, Dict, Any
import numpy as np
from rank_bm25 import BM25Okapi
from utils import cosine_similarity, get_embedding, HEADER_WEIGHT, CONTENT_WEIGHT, HEADER_SEMANTIC_WEIGHT, HEADER_KEYWORD_WEIGHT, CONTENT_SEMANTIC_WEIGHT, CONTENT_KEYWORD_WEIGHT, RELEVANCE_THRESHOLD

def semantic_search(query: str, chunks: List[Dict[str, Any]], k: int = 5) -> List[Dict[str, Any]]:
    query_embedding = get_embedding(query)
    similarities = []
    for chunk in chunks:
        header_similarity = cosine_similarity(query_embedding, chunk['header_embedding'])
        content_similarity = cosine_similarity(query_embedding, chunk['chunk_embedding'])
        combined_similarity = HEADER_WEIGHT * header_similarity + CONTENT_WEIGHT * content_similarity
        similarities.append(combined_similarity)

    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return [chunks[i] for i in top_k_indices]

def keyword_search(query: str, chunks: List[Dict[str, Any]], k: int = 5) -> List[Dict[str, Any]]:
    corpus = [f"{chunk['header']} {chunk['chunk']}" for chunk in chunks]
    bm25 = BM25Okapi(corpus)
    doc_scores = bm25.get_scores(query.split())
    top_k_indices = np.argsort(doc_scores)[-k:][::-1]
    return [chunks[i] for i in top_k_indices]

def hybrid_search(query: str, chunks: List[Dict[str, Any]], k: int = 5) -> List[Dict[str, Any]]:
    query_embedding = get_embedding(query)
    bm25 = BM25Okapi([chunk['header'] + " " + chunk['chunk'] for chunk in chunks])

    scored_results = []
    for chunk in chunks:
        header_semantic_score = cosine_similarity(query_embedding, chunk['header_embedding'])
        header_keyword_score = bm25.get_scores([query])[chunks.index(chunk)]
        header_score = (HEADER_SEMANTIC_WEIGHT * header_semantic_score +
                        HEADER_KEYWORD_WEIGHT * header_keyword_score)

        content_semantic_score = cosine_similarity(query_embedding, chunk['chunk_embedding'])
        content_keyword_score = bm25.get_scores([query])[chunks.index(chunk)]
        content_score = (CONTENT_SEMANTIC_WEIGHT * content_semantic_score +
                         CONTENT_KEYWORD_WEIGHT * content_keyword_score)

        final_score = HEADER_WEIGHT * header_score + CONTENT_WEIGHT * content_score

        if final_score >= RELEVANCE_THRESHOLD:
            scored_results.append({
                **chunk,
                'relevance_score': final_score
            })

    scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return scored_results[:k]