import re

def parse_query(query: str):
    q = query.lower().strip()
    filters = {}

    # Detect palindromes
    if "palindromic" in q or "palindrome" in q:
        filters["is_palindrome"] = True

    # Detect single-word or one-word requests
    if "single word" in q or "one word" in q:
        filters["word_count"] = 1

    # Detect "longer than X" patterns
    match = re.search(r"longer than (\d+)", q)
    if match:
        num = int(match.group(1))
        filters["min_length"] = num + 1

    # Detect "shorter than X" patterns 
    match = re.search(r"shorter than (\d+)", q)
    if match:
        num = int(match.group(1))
        filters["max_length"] = num - 1

    # Detect "containing the letter X"
    match = re.search(r"containing the letter (\w)", q)
    if match:
        filters["contains_character"] = match.group(1)

    # Handle "strings containing the letter z"
    match = re.search(r"containing the letter (\w)", q)
    if match:
        filters["contains_character"] = match.group(1)

    if not filters:
        raise ValueError("Unable to parse natural language query")

    return filters
