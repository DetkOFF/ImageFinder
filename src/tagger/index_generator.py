import json
from collections import defaultdict
import spacy
import pickle
from pathlib import Path
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

# # # # Create an inverted index from the captions. # # # #
def create_index():
    inv_index = defaultdict(set)
    records = {}

    res_path = resource_path("/../captions.jsonl")
    with open(res_path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            fn = rec["filename"]
            cap = rec["caption"]
            records[fn] = rec

            for lemma in tokenize(cap):
                inv_index[lemma].add(fn)
    
    pkl_path = resource_path("/../inv_index.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(inv_index, f)

create_index()