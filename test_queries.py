import json
import time
import csv
from typing import List, Dict
import Levenshtein
from soundex import Soundex

def load_books_from_csv(filename: str) -> List[dict]:
    books = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books

books = load_books_from_csv("./assets/BooksDatasetClean.csv")

# Extract titles
titles = [book["title"] for book in books]

# Example queries
queries = ["algorithm", "code", "design", "programming"]

def run_search(query, algo, thresholds=[0.7, 0.8, 0.9]):
    index_and_scores = {thr: dict() for thr in thresholds}
    query_in_middle_of_string = []
    exact_matches = {thr: dict() for thr in thresholds}
    start_time = time.time()

    for index, title in enumerate(titles):
        score = algo(query.lower(), title.lower())
        for thr in thresholds:
            if score >= thr:
                index_and_scores[thr][index] = score
                if query.lower() in title.lower().split():
                    exact_matches[thr][index] = score
        if query.lower() in title.lower().split():
            query_in_middle_of_string.append(title)

    end_time = time.time()
    execution_time = end_time - start_time

    results = {
        'search_results': {thr: len(index_and_scores[thr]) for thr in thresholds},
        'returned_exact_matches': {thr: len(exact_matches[thr]) for thr in thresholds},
        'actual_exact_match': len(query_in_middle_of_string),
        'time_of_execution': execution_time
    }

    return results

def run_jaro(query, thresholds=[0.7, 0.8, 0.9]):
    return run_search(query, Levenshtein.jaro, thresholds)

def run_lev(query):
    index_and_scores = dict()
    query_in_middle_of_string = []
    exact_matches = dict()
    start_time = time.time()

    for index, title in enumerate(titles):
        score = Levenshtein.distance(query.lower(), title.lower())
        if score <= 3:
            index_and_scores[index] = score
            if query.lower() in title.lower().split():
                exact_matches[index] = score
        if query.lower() in title.lower().split():
            query_in_middle_of_string.append(title)

    end_time = time.time()
    execution_time = end_time - start_time

    results = {
        'search_result': len(index_and_scores),
        'returned_exact_match': len(exact_matches),
        'actual_exact_match': len(query_in_middle_of_string),
        'time_of_execution': execution_time
    }

    return results

def run_soundex(query):
    sn = Soundex()
    index_and_scores = dict()
    query_in_middle_of_string = []
    exact_matches = dict()
    start_time = time.time()

    for index, title in enumerate(titles):
        if sn.soundex_generator(query) == sn.soundex_generator(title):
            index_and_scores[index] = sn.soundex_generator(query)
            if query.lower() in title.lower().split():
                exact_matches[index] = sn.soundex_generator(query)
        if query.lower() in title.lower().split():
            query_in_middle_of_string.append(title)

    end_time = time.time()
    execution_time = end_time - start_time

    results = {
        'search_result': len(index_and_scores),
        'returned_exact_match': len(exact_matches),
        'actual_exact_match': len(query_in_middle_of_string),
        'time_of_execution': execution_time
    }

    return results

# Initialize a dictionary to store results
all_results = {}

# Run the search for each query with different algorithms
for query in queries:
    all_results[query] = {
        'jaro': run_jaro(query),
        'levenshtein': run_lev(query),
        'soundex': run_soundex(query)
    }

# Save results to a JSON file
with open('results.json', 'w') as json_file:
    json.dump(all_results, json_file, indent=4)

print("Results have been saved to results.json")
