import json
from collections import defaultdict
import spacy
import pickle
from typing import List, Dict, Set
import os, sys

nlp_ru = spacy.load("ru_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

def resource_path(rel_path: str) -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, rel_path)

def tokenize(text: str) -> set[str]:
    model = nlp_ru if any('а' <= ch <= 'я' or 'А' <= ch <= 'Я' for ch in text) else nlp_en
    doc = model(text.lower())
    return {tok.lemma_ for tok in doc if tok.is_alpha}


pkl_path = resource_path("inv_index.pkl")
with open(pkl_path, "rb") as f:
        inv_index = pickle.load(f)


def search_by_tags(tags: List[str],
                     inv_index: Dict[str, Set[str]],
                     operator: str = "AND") -> List[str]:
    if not tags:
        return []
     
    sets = [inv_index.get(l, set()) for l in tags]
    if operator.upper() == "AND":
        result = set.intersection(*sets)
    else:
        result = set.union(*sets)
    return list(result)        


def search(query: str, inv_index: dict, operator: str = "AND") -> list[str]:
     lemmas = list(tokenize(query))
     
     return search_by_tags(lemmas, inv_index, operator)


def search_by_word(word: str, inv_index: dict, operator: str = "AND") -> List[str]:
    key = word.lower()
    return list(inv_index.get(key, []))