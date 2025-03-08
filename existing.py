class ExistingAlgo:
    
    def jaro_winkler(target, referent):
        def jaro_distance(target, referent):
            if target == referent:
                return 1.0

            target_len, referent_len = len(target), len(referent)
            max_dist = max(target_len, referent_len) // 2 - 1 # for symmetric peeking

            matches = 0
            target_hash = [0] * target_len
            referent_hash = [0] * referent_len

            # For getting mathces
            for i in range(target_len):
                for j in range(max(0, i - max_dist), min(referent_len, i + max_dist + 1)):
                    if target[i] == referent[j] and referent_hash[j] == 0:
                        target_hash[i] = 1
                        referent_hash[j] = 1
                        matches += 1
                        break

            if matches == 0:
                return 0.0
            
            # Transposition
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

            return (matches / target_len + matches / referent_len + (matches - t) / matches) / 3.0

        # Jaro Winkler Calculation
        jaro_dist = jaro_distance(target, referent)
        prefix = 0
        for i in range(min(len(target), len(referent))):
            if target[i] == referent[i]:
                prefix += 1
            else:
                break
        
        prefix = min(4, prefix)
        return jaro_dist + 0.1 * prefix * (1 - jaro_dist)

    def jaro_distance(target, referent):
        if target == referent:
            return 1.0
        
        target_len, referent_len = len(target), len(referent)
        max_dist = max(target_len, referent_len) // 2 - 1 # for symmetric peeking

        matches = 0
        target_hash = [0] * target_len
        referent_hash = [0] * referent_len

        # For getting mathces
        for i in range(target_len):
            for j in range(max(0, i - max_dist), min(referent_len, i + max_dist + 1)):
                if target[i] == referent[j] and referent_hash[j] == 0:
                    target_hash[i] = 1
                    referent_hash[j] = 1
                    matches += 1
                    break

        if matches == 0:
            return 0.0
        
        # Transposition
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

        return (matches / target_len + matches / referent_len + (matches - t) / matches) / 3.0