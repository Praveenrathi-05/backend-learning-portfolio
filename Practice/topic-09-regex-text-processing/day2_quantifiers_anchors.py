"""
Topic 9, Day 2: Bridge & Reinforcement

Covered: \w, \s, . (wildcard), quantifiers * ? {n} {n,m}, and anchors ^ $
(taught mid-session after flagging they hadn't been covered yet).

Standing framework adopted mid-Day-2: every concept and every problem gets
the full "restate -> tools -> sub-steps -> what could go wrong" treatment
from here forward.
"""

import re


# --- Homework 1: \w+_\d+ on log lines ---
# Goal: identify which lines match a username_id shape, and understand WHY
# \w+ (which includes underscore) still stops correctly at the literal "_"
# in the pattern, via backtracking.

log_lines = [
    "user_42 logged in",
    "admin_1 updated settings",
    "guest logged in",       # no underscore+digit shape -- should NOT match
    "system_007 rebooted",
]

pattern = r"\w+_\d+"
for line in log_lines:
    match = re.search(pattern, line)
    if match:
        print(f"MATCH: {match.group()}")
    else:
        print(f"NO MATCH: {line}")


# --- Homework 2: is_valid_username(s) ---
# First attempt used re.search(r"\w{3,}") with no anchors -- bug: only checks
# that a valid substring exists SOMEWHERE, not that the WHOLE string is valid.
# "ab!cdefgh" would have incorrectly passed. Fixed by adding ^ and $ anchors,
# forcing the entire string to match, not just a piece of it.

def is_valid_username(s):
    return re.search(r"^\w{3,}$", s) is not None


print(is_valid_username("praveen"))     # True
print(is_valid_username("ab!cdefgh"))    # False -- correctly rejected now
print(is_valid_username("ab"))            # False -- too short


# --- Homework 3: count_words(s) -- WITHOUT regex ---
# Goal: solve the same "how many words" question using plain string tools,
# as a contrast to the regex-based version done later in Day 3.

def count_words(s):
    return len(s.split())   # .split() with no args auto-collapses whitespace


print(count_words("Hello   world  from Praveen"))   # 4
