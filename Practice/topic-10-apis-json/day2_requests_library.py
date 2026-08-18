"""
Topic 10, Day 2: The `requests` Library -- Real HTTP Calls

Covered: requests.get(), the Response object, status_code (2xx/4xx/5xx),
.json() for parsing responses, and the key distinction between a "bad"
response (server replied, still a Response object, no exception) versus
a connection failure (no response at all -- raises an exception instead).
"""

import requests


# --- Homework 1: get_github_user ---
# Goal: full real pattern -- check status_code BEFORE trusting the response,
# then extract a specific nested field from the JSON.

def get_github_user(username):
    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 200:
        data = response.json()
        return f"{username} has {data['public_repos']} public repos"
    else:
        return f"User not found (status {response.status_code})"


print(get_github_user("Praveenrathi-05"))


# --- Homework 2: wrapped in try/except for connection failure ---
# Goal: prove status-code checking alone isn't enough -- a totally
# unreachable domain doesn't return a Response at all, it raises
# requests.exceptions.ConnectionError. Tested deliberately against a
# domain that cannot resolve, confirming the except block actually fires.

def get_github_user_safe(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            data = response.json()
            return f"{username} has {data['public_repos']} public repos"
        else:
            return f"User not found (status {response.status_code})"
    except requests.exceptions.ConnectionError:
        return "Couldn't reach the server at all — check your connection or the URL."


print(get_github_user_safe("Praveenrathi-05"))          # success path

# Deliberately broken domain -- proves the except block genuinely fires,
# rather than just trusting it looks correct on paper.
def get_broken_connection():
    try:
        response = requests.get("https://this-is-not-a-real-domain-xyz999.com")
        return response.status_code
    except requests.exceptions.ConnectionError:
        return "Couldn't reach the server at all — check your connection or the URL."


print(get_broken_connection())


# --- DSA Micro-drill: find_deepest_value ---
# Goal: walk an arbitrary-length list of keys/indices into a nested
# dict/list structure, without hardcoding how many levels deep it goes.

def find_deepest_value(data, path):
    value = data
    for loc in path:
        value = value[loc]
    return value


data = {
    "users": ["Alice", "Bob", "Charlie"]
}
print(find_deepest_value(data, ["users", 1]))   # 'Bob'
# mixes a dict key ("users") with a list index (1) in the same path,
# proving value[loc] works identically whether value is a dict or a list.
