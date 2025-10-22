import hashlib
from datetime import datetime, timezone

def analyze_string(value: str):
    value = value.strip()
    return {
        "length": len(value),
        "is_palindrome": value.lower() == value[::-1].lower(),
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": hashlib.sha256(value.encode()).hexdigest(),
        "character_frequency_map": {c: value.count(c) for c in set(value)},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
