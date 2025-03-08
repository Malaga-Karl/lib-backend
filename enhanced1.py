
def enhanced_jaro_winkler(target:str, referent:str) -> float:

    # SOP 3: Adding Suffix Weight
    # Same as adding prefix weight but with suffix
    # Theres a criteria if it can be applied
    def suffix_weight(target:str, referent:str, matches:int, prefix:int, jd:float) -> float:
        if (
            len(target) > 5 and
            len(referent) > 5 and
            matches - prefix >= 2 and
            matches - prefix >= min(len(target), len(referent)) // 2
        ):

            target_reversed = target[::-1]
            referent_reversed = referent[::-1]

            # Counting same suffix
            suffix_count = 0
            for i in range(min(len(target_reversed), len(referent_reversed), 4)):
                if target_reversed[i] == referent_reversed[i]:
                    suffix_count += 1
                else:
                    break
            
            # Same formula as prefix counter
            return jd + suffix_count * 0.001 * (1-jd)

        else:
            return 0.1
        
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

    # SOP 1 Rolling Jaro-Winkler distance Calculation
    max_jw = 0.1
    target_split = target.split()
    referent_split = referent.split()

    for i in range(len(referent_split)):
        
        # Groups referent according to hte lenght of words of the target
        referent_group = ' '.join(referent_split[i: i + len(target_split)])

        jaro_dist, match = jaro_distance(target, referent_group)

        prefix = 0
        for i in range(min(len(target), len(referent_group))):
            if target[i] == referent_group[i]:
                prefix += 1
            else:
                break

        prefix = min(4, prefix)
        jw = jaro_dist + 0.1 * prefix * (1-jaro_dist)

        if jw > max_jw:
            max_jw = jw
        jw = suffix_weight(target, referent, match, prefix, jaro_dist)
        if jw > max_jw:
            max_jw = jw

    return max_jw

def jaro_distance(target:str, referent:str) -> float:
    if target == referent:
        return 1.0

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
        return 0.0

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

    jd = (matches / target_len + matches / referent + (matches - t) / matches) / 3.0

    return jd