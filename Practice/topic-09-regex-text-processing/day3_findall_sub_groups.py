"""
Topic 9, Day 3: Depth & Application

Covered: re.findall(), re.sub(), capture groups, greedy vs lazy quantifiers,
and applying regex to real, messy text.

Standing habit locked in today: ALWAYS use raw strings (r"...") for regex
patterns -- not optional. \b is a real Python escape sequence (backspace)
in a normal string, silently breaking any pattern that relies on it as a
word boundary if the r-prefix is forgotten.
"""

import re


# --- Homework 1: extract_prices(text) ---
# Goal: combine findall() with explicit string -> int conversion, since
# regex ALWAYS returns captured text as strings, never real numbers.

def extract_prices(text):
    matches = re.findall(r"\d+", text)
    return [int(match) for match in matches]


print(extract_prices("Rent: ₹8500, Food: ₹3200, Transport: ₹600"))
# [8500, 3200, 600]


# --- Homework 2: clean_phone_number(raw) ---
# Goal: strip a messy phone number down to just its 10 digits using re.sub(),
# and (self-added) handle a leading "91" country code if it results in more
# than 10 digits after stripping.

def clean_phone_number(raw):
    digits_only = re.sub(r"\D", "", raw)
    if len(digits_only) > 10 and digits_only.startswith("91"):
        digits_only = digits_only[2:]
    return digits_only


print(clean_phone_number("+91 98765-43210"))   # 9876543210
print(clean_phone_number("(987) 654-3210"))     # 9876543210
print(clean_phone_number("9876543210"))          # 9876543210


# --- DSA Micro-drill: count_words(text) using regex ---
# Goal: use \b (word boundary) + \w+ to count words even with irregular
# punctuation/spacing, e.g. "This--is" correctly counted as TWO words,
# since "-" is not a word character and creates a boundary on both sides.

def count_words(text):
    return len(re.findall(r"\b\w+\b", text))


print(count_words("Hello,   world! This--is a test."))
# 6 -- Hello, world, This, is, a, test
