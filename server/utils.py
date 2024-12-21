import numpy as np
from sentence_transformers import SentenceTransformer
import functools
from typing import List

MAX_CONTEXT_LENGTH = 5000

HEADER_WEIGHT = 0.4
CONTENT_WEIGHT = 0.6

HEADER_KEYWORD_WEIGHT = 0.4
HEADER_SEMANTIC_WEIGHT = 0.6
CONTENT_KEYWORD_WEIGHT = 0.3
CONTENT_SEMANTIC_WEIGHT = 0.7

RELEVANCE_THRESHOLD = 0.35 

model = SentenceTransformer('jhgan/ko-sbert-nli')

def get_embedding(text: str) -> List[float]:
    return model.encode(text).tolist()

@functools.lru_cache(maxsize=100)
def get_chunk_embedding(chunk: str) -> List[float]:
    return get_embedding(chunk)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))