def normalize_braille_sequence(sequence):
    """
    Enhanced normalization with fuzzy matching:
    1. Converts to lowercase
    2. Sorts characters
    3. Removes duplicates
    4. Finds closest valid sequence if exact match not found
    """
    if not sequence:
        return ""
    
    # Remove any non-Braille keys (only keep d, w, q, k, o, p)
    valid_chars = {'d', 'w', 'q', 'k', 'o', 'p'}
    filtered = [c for c in sequence.lower() if c in valid_chars]
    
    # Sort and remove duplicates
    unique_sorted = sorted(set(filtered))
    normalized = ''.join(unique_sorted)
    
    return normalized

def find_closest_braille_sequence(sequence, key_map):
    """
    Find the closest valid Braille sequence to the input
    using subsequence matching and edit distance
    """
    if not sequence:
        return ""
    
    normalized = normalize_braille_sequence(sequence)
    
    # Exact match exists
    if normalized in key_map:
        return normalized
    
    # Try to find closest match
    min_distance = float('inf')
    closest_seq = ""
    
    # Check all possible valid sequences
    for valid_seq in key_map.keys():
        # Check if input is a subsequence of a valid sequence
        if is_subsequence(normalized, valid_seq):
            distance = levenshtein_distance(normalized, valid_seq)
            if distance < min_distance:
                min_distance = distance
                closest_seq = valid_seq
    
    # If we found a close match with small distance
    if closest_seq and min_distance <= 2:  # Allow up to 2 differences
        return closest_seq
    
    # Try to find sequence with smallest edit distance
    for valid_seq in key_map.keys():
        distance = levenshtein_distance(normalized, valid_seq)
        if distance < min_distance:
            min_distance = distance
            closest_seq = valid_seq
    
    # Only return if distance is small enough
    return closest_seq if min_distance <= 2 else ""

def is_subsequence(s1, s2):
    """Check if s1 is a subsequence of s2"""
    it = iter(s2)
    return all(c in it for c in s1)

def get_common_error_patterns():
    """
    Returns common error patterns in Braille input
    Maps incorrect sequences to likely intended sequences
    """
    return {
        "dkp": "dk",    # Common extra key
        "dwk": "dw",     # Common extra key
        "doq": "dq",     # Common missing key
        "kq": "kqw",     # Common missing key
        "ko": "kow",     # Common missing key
        "dp": "dq",      # Common key confusion
        "wk": "dw"       # Common key confusion
    }

def levenshtein_distance(s1, s2):
    """
    Calculate Levenshtein distance between two strings
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]