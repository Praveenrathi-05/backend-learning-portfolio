"""
Topic 9, Day 1: Regular Expressions & Text Processing - Foundations

Covered: what regex is (matching shape vs exact text), raw strings (r"..."),
re.search(), Match objects, .group(), \d (digit), + (one or more),
checking `if match:` before calling .group() to avoid AttributeError on None.
"""

import re


# --- Homework 1: print first number found in each message, or "No number found" ---
# Goal: confirms re.search() stops at the FIRST match, even if a string has
# more than one number in it -- it does not find all of them.

messages = [
    "Your OTP is 4821, valid for 5 minutes.",
    "No numbers here at all.",
    "Order #1042 shipped, tracking id 9981",
]

for msg in messages:
    match = re.search(r"\d+", msg)
    if match:
        print(match.group())
    else:
        print("No number found")


# --- Homework 2: has_number(s) -- boolean check using re.search ---
# Goal: use re.search purely as a True/False check, not to extract anything.

def has_number(s):
    return re.search(r"\d", s) is not None


print(has_number("room 42"))     # True
print(has_number("no digits"))    # False


# --- DSA Micro-drill: count_digits(s) -- WITHOUT regex or .isdigit() ---
# Goal: build the reflex of character-by-character checking without shortcuts.
# Solved two independent, correct ways.

def count_digits_v1(s):
    """Approach 1: try/except trick -- attempt int(char), count on success."""
    count = 0
    for char in s:
        try:
            int(char)
            count += 1
        except ValueError:
            pass
    return count


def count_digits_v2(s):
    """Approach 2: direct character-set membership check."""
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    count = 0
    for char in s:
        if char in digits:
            count += 1
    return count


print(count_digits_v1("room42b7"))   # 3
print(count_digits_v2("room42b7"))   # 3
