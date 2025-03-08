'''
Enhanced Jaro Winkler File.
This file contains 5 main functions:

    plain jaro distance
        literal plain lang

    weighted jaro winkler (SOP 3)
        jw = jaro_dist + max(prefix, suffix) * 0.1 * (1-jaro_dist) -> main change

    rolling jw (SOP 1)
        groups the referent into chunks according to the number of words in target
    
    jaccard jw (SOP 2)
        if the target and referent are 80% + similar in length, perform this instead of rolling
        jaccard but instead of intersection of same words, intersection is jaro-winklered words

    enhanced jaro winkler (combined)
        did as drew on flowchart
'''

import nltk
from nltk.corpus import stopwords
import re
stops = set(stopwords.words('english'))

# Initial Jaro Distance
def jaro_distance(target:str, referent:str) -> tuple[float, int]:
    if target == referent:
        return 1.0, len(target)

    target_len, referent_len = len(target), len(referent)
    max_dist = max(target_len, referent_len) // 2 - 1 # for symmetric peeking

    matches = 0

    # Hash map for trasposition
    target_hash = [0] * target_len
    referent_hash = [0] * referent_len

    # For getting character matches
    for i in range(target_len):
        for j in range(max(0, i - max_dist), min(referent_len, i + max_dist + 1)):
            if target[i] == referent[j] and referent_hash[j] == 0:
                target_hash[i] = 1
                referent_hash[j] = 1
                matches += 1
                break
    
    if matches == 0:
        return 0.0, matches

    # Transpositions
    t = 0
    point = 0

    for i in range(target_len):
        if target_hash[i]:
            while referent_hash[point] == 0:
                point += 1
            if target[i] != referent[point]:
                t += 1
            point += 1
    t /= 2

    jd = (matches / target_len + matches / referent_len + (matches - t) / matches) / 3.0

    return jd, matches

def weighted_jw(target:str, referent:str) -> float:
    target = target.lower()
    referent = referent.lower()
    jaro_dist, match = jaro_distance(target, referent)

    # counts prefix
    prefix = 0
    for i in range(min(len(target), len(referent))):
        if target[i] == referent[i]:
            prefix += 1
        else:
            break

    prefix = min(4, prefix)

    # count suffix
    # SOP 3 suffix weight
    suffix_count = 0
    if (
        len(target) > 5 and
        len(referent) > 5 and
        match - prefix >= 2 and
        match - prefix >= min(len(target), len(referent)) // 2
    ):
        target_reversed = target[::-1]
        referent_reversed = referent[::-1]

        # Counting same suffix
        for i in range(min(len(target_reversed), len(referent_reversed), 4)):
            if target_reversed[i] == referent_reversed[i]:
                suffix_count += 1
            else:
                break
    
    suffix = min(4, suffix_count)

    jw = jaro_dist + max(prefix, suffix) * 0.1 * (1-jaro_dist)
    return jw


# SOP 1 Rolling Jaro-Winkler distance Calculation
def rolling_jw(target:str, referent:str):
    max_jw = 0.1
    target_split = target.split()
    target_length = len(target_split)
    referent_split = referent.split()

    for i in range(len(referent_split)):
        # Groups referent according to hte lenght of words of the target
        referent_group = ' '.join(referent_split[i: i + len(target_split)])
        if len(referent_group.split()) < target_length:
            break
        jw = weighted_jw(target, referent_group)

        if jw > max_jw:
            max_jw = jw

    return max_jw


def jaccard_jw(target:str, referent:str):
    def remove_stopwords(sentence):
        words = re.findall(r'\b\w+\b', sentence)  # Extract words (ignoring punctuation)
        return [word for word in words if word.lower() not in stops]  # Return list instead of string

    target = remove_stopwords(target)
    referent = remove_stopwords(referent)

    fuzzy_matches = 0
    matched_targets = set()  # Track matched target words
    unmatched_targets = []   # Track words without a match

    for target_word in target:
        found_match = False  # Flag to check if a word gets a match

        for referent_word in referent:
            score = weighted_jw(target_word, referent_word)
            # print(f"{target_word} vs {referent_word}: {score}")
            
            if score >= 0.8:
                fuzzy_matches += score
                matched_targets.add(target_word)
                found_match = True  # Mark as matched
        
        if not found_match:
            unmatched_targets.append(target_word)  # Store unmatched words

    score = fuzzy_matches / (len(matched_targets) + len(unmatched_targets))
    return score

def enhanced_jaro_winkler(target:str, referent:str):
    ejw_score = 0.0

    if len(target.split()) > 1 and len(target.split()) > 1 and (len(target.split()) / len(referent.split())) >= 0.6:
        ejw_score = weighted_jw(target, referent)
        if ejw_score >= 0.8:
            # print("used weighted")
            return ejw_score
        else:
            ejw_score = jaccard_jw(target, referent)
            # print("used jaccard")
            return ejw_score

    else:
        ejw_score = rolling_jw(target, referent)
        # print("used rolling")
    return ejw_score