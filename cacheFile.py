import json
import os

CACHE_FILE = "message_cache.json"

def save_message_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def load_message_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None
