import os
import datetime
import json

def save_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def log(message):
    print(f"[{datetime.datetime.now()}] {message}")
