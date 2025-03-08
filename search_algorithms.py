from typing import List, Dict
from Levenshtein import distance, jaro, jaro_winkler
from soundex import Soundex
from enhanced1 import enhanced_jaro_winkler
from searches import run_jaccard

def exact_search(query: str, books: List[Dict[str, str]]) -> List[Dict[str, str]]:
    results = [
        book for book in books
        if query.lower() in book["title"].lower()
    ]
    return results

def lev_search(query: str, books: List[Dict[str, str]]) -> List[Dict[str, str]]:
    results = [
        book for book in books
        if distance(query.lower(), book["title"].lower()) <= 3
    ]
    return results

def jaro_search(query: str, books: List[Dict[str, float]]) -> List[Dict[str, float]]:
    scored_books = [
        {"id": book["id"], "score": jaro(query.lower(), book["title"].lower())} for book in books
    ]
    results = [book for book in scored_books if book["score"] >= 0.8]
    return results

def traditional_jw_search(query: str, books: List[Dict[str, float]]) -> List[Dict[str, float]]:
    scored_books = [
        {"id": book["id"], "score": jaro_winkler(query.lower(), book["title"].lower())} for book in books
    ]
    results = [book for book in scored_books if book["score"] >= 0.8]
    return results

def soundex_search(query: str, books: List[Dict[str, str]]) -> List[Dict[str, str]]:
    sn = Soundex()
    results = [
        book for book in books
        if sn.soundex_generator(query) == sn.soundex_generator(book["title"])
    ]
    return results

def enhanced_jw_search(query: str, books: List[Dict[str, float]]) -> List[Dict[str, float]]:
    scored_books = [
        {"id": book["id"], "score": enhanced_jaro_winkler(query.lower(), book["title"].lower())} for book in books
    ]
    results = [book for book in scored_books if book["score"] >= 0.8]
    return results

def jaccard_search(query: str, books: List[Dict[str, float]]) -> List[Dict[str, float]]:
    scored_books = [
        {"id": book["id"], "score": run_jaccard(query.lower(), book["title"].lower())} for book in books
    ]
    results = [book for book in scored_books if book["score"] >= 0.7]
    return results