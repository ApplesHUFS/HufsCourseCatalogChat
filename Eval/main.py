import json
from gpt_integration import get_gpt_answer
from typing import List, Dict, Any

def load_processed_data(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def chatting(query):
    processed_data = load_processed_data("server/processed_data.json")
    answer = get_gpt_answer(query, processed_data)
    return answer