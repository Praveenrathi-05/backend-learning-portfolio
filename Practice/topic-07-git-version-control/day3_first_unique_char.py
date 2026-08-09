# Topic 7, Day 3 -- DSA Micro-Drill

# first_unique_char: returns the index of the first character in a
# string that doesn't repeat anywhere else. Returns -1 if every
# character repeats.
#
# Requires TWO passes over the string:
#   1. build a frequency count of every character (dict-as-counter,
#      same pattern as most_frequent)
#   2. walk through the string AGAIN, in its original order, and return
#      the index of the first character whose count is exactly 1
#
# Why two passes: the frequency dict alone has no concept of "order" --
# it can tell you a character is unique, but not which unique character
# appeared FIRST in the original string. Only re-scanning in order
# preserves that.


def first_unique_char(s):
    frequency = {}
    for char in s:
        frequency[char] = frequency.get(char, 0) + 1

    for i in range(len(s)):
        if frequency[s[i]] == 1:
            return i
    return -1


print(first_unique_char("swiss"))  # 1  -- 'w' is the first non-repeating char
print(first_unique_char("aabb"))    # -1 -- every character repeats
