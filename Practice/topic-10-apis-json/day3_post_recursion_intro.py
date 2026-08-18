"""
Topic 10, Day 3: POST Requests, Query Parameters, Headers & Production Reality

Covered: GET vs POST intent, params= for query strings, json= for request
bodies, headers= for credentials/metadata, timeout= as a non-negotiable
production habit, and a full three-way error-handling shape (bad status
code / ConnectionError / Timeout). Also a first, informal introduction to
recursion, months ahead of its formal topic (28).
"""

import requests
import json


# --- Homework 1: get_github_user with timeout + Timeout handling ---
# Goal: complete the "full, real" error-handling shape -- status code,
# ConnectionError, AND Timeout all handled distinctly.

def get_github_user(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"{username} has {data['public_repos']} public repos"
        else:
            return f"User not found (status {response.status_code})"
    except requests.exceptions.ConnectionError:
        return "Couldn't reach the server at all — check your connection or the URL."
    except requests.exceptions.Timeout:
        return "Request timed out."


print(get_github_user("Praveenrathi-05"))


# --- Homework 2: query params + unguided nested-JSON navigation ---
# Goal: explore an unfamiliar response shape by printing it first
# (json.dumps with indent), THEN write extraction code -- rather than
# guessing the structure in advance.

response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "backend python", "sort": "stars"}
)
data = response.json()
print(json.dumps(data, indent=2))

for i in range(3):
    print(data['items'][i]['name'])
    print(data['items'][i]['stargazers_count'])


# --- DSA Micro-drill: flatten_json_keys (first taste of recursion) ---
# Goal: flatten an arbitrarily-nested dict into a single-level dict, with
# dotted key paths showing how deep each value was buried.
#
# Base case: the value is NOT a dict -> record it under the current path.
# Recursive case: the value IS a dict -> call flatten_json_keys again on
#   it, with the prefix extended -- then merge (.update()) the smaller
#   result back into this level's result, since a dict merge is how a
#   sub-call's complete answer gets folded into the caller's answer.

def flatten_json_keys(data, prefix=""):
    paths = {}
    for key in data:
        current_prefix = prefix + "." + key if prefix != "" else key
        if not isinstance(data[key], dict):
            paths[current_prefix] = data[key]
        else:
            deeper = flatten_json_keys(data[key], current_prefix)
            paths.update(deeper)
    return paths


print(flatten_json_keys({
    "user": {
        "name": "Praveen",
        "address": {"city": "Ahmedabad"}
    }
}))
# {'user.name': 'Praveen', 'user.address.city': 'Ahmedabad'}
