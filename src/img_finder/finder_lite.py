import pickle
from typing import List, Dict, Set
import os, sys

def resource_path(rel_path: str) -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, rel_path)

pkl_path = resource_path("inv_index.pkl")
with open(pkl_path, "rb") as f:
        inv_index = pickle.load(f)


def search_by_word(word: str, inv_index: dict, operator: str = "AND") -> List[str]:
    key = word.lower()
    return list(inv_index.get(key, []))