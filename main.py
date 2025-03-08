from fastapi import FastAPI, Query
import csv
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import time
from search_algorithms import exact_search, lev_search, jaro_search, traditional_jw_search, soundex_search, enhanced_jw_search, jaccard_search

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def load_books_from_csv(filename: str) -> List[dict]:
    books = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books

books = load_books_from_csv("./assets/BooksDatasetClean.csv")

@app.get('/')
def index():
    return {"name": "karlbenedict"}

# searches

@app.get('/exact/{query}')
def exactSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = exact_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/lev/{query}')
def levSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = lev_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/jaro/{query}')
def jaroSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = jaro_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/traditionaljw/{query}')
def traditionalJWSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = traditional_jw_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/enhancedjw/{query}')
def enhancedJWSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = enhanced_jw_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/soundex/{query}')
def soundexSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = soundex_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/jaccard/{query}')
def jaccardSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = jaccard_search(query, books)
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results
    }

@app.get('/book/{id}')
def getBookById(id: str) -> Dict[str, Any]:
    book = next((book for book in books if book["id"] == id), None)

    if book:
        return book
    else:
        return {"message": "no book found, dumbass"}