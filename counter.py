import json
import os

COUNTER_FILE = 'counters.json'


def load_counters():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_counters(counters):
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counters, f)


def increment_counter(user_id: int) -> int:
    counters = load_counters()
    if str(user_id) not in counters:
        counters[str(user_id)] = 0
    counters[str(user_id)] += 1
    save_counters(counters)
    return counters[str(user_id)]
