"""
Topic 10, Day 1: JSON Foundations

Covered: json.dumps()/json.loads() (object <-> string), json.dump()/json.load()
(direct file read/write), the Python <-> JSON type mapping (True->true,
None->null), and why tuples silently become JSON arrays (lossy round-trip).
"""

import json

file_name = "expenses.json"


# --- Homework 1: save_expenses_json / load_expenses_json ---
# Goal: the real, correct replacement for Weekly Project #3's comma-based
# storage -- structural JSON instead of a fragile delimiter, plus graceful
# handling of a missing file on first run (Topic 5's error handling).

def save_expenses_json(expenses, filename):
    with open(filename, "w") as file:
        json.dump(expenses, file, indent=4)


def load_expenses_json(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


expenses = [
    {"amount": 250, "category": "food", "note": "lunch"},
    {"amount": 1200, "category": "rent", "note": "monthly"},
    {"amount": 80, "category": "transport", "note": "auto"},
]

save_expenses_json(expenses, file_name)
loaded = load_expenses_json(file_name)
print(loaded)


# --- Homework 2: pretty_print_json ---
# Goal: see what indent=2 actually changes -- purely readability, no effect
# on the underlying data itself (a round trip produces an identical dict
# either way).

def pretty_print_json(data):
    print(json.dumps(data, indent=2))


library = {
    "name": "City Library",
    "books": [
        {"title": "Deep Work", "author": "Cal Newport"},
        {"title": "Atomic Habits", "author": "James Clear"},
    ],
}
pretty_print_json(library)


# --- DSA Micro-drill: merge_json_dicts ---
# Goal: parse two JSON strings back into real dicts, then merge them so the
# second dict's keys win on any overlap.

def merge_json_dicts(json_str1, json_str2):
    dict1 = json.loads(json_str1)
    dict2 = json.loads(json_str2)
    for key, value in dict2.items():
        dict1[key] = value
    return dict1


print(merge_json_dicts('{"a": 1, "b": 2}', '{"b": 99, "c": 3}'))
# {'a': 1, 'b': 99, 'c': 3}

# Alternative, idiomatic version using dict unpacking (doesn't mutate dict1):
# return {**dict1, **dict2}
