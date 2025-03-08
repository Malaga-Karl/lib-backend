from typing import List, Dict, Any

def exactSearch(query: str) -> Dict[str, Any]:
    start_time = time.time()
    results = [
        book for book in books
        if query.lower() in book["title"].lower()
    ]
    end_time = time.time()
    duration = end_time - start_time

    return {
        "count": len(results),
        "duration": duration,
        "results": results if results else {"message": "No books found"}
    }

def run_jaccard(target: str, referent: str) -> float:

    query_set = set(query.lower().split())
    title_set = set(title.lower().split())
    return len(query_set.intersection(title_set)) / len(query_set.union(title_set)) # according kay GPT .7 pero tayo bahala sa threshold. .7 considered as fuzzy match btw
            