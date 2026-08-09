# Topic 7, Day 2 -- DSA Micro-Drill

# reverse_string: reverses a string without using slicing (s[::-1])
# or the built-in reversed().
#
# Approach: walk through the ORIGINAL string starting from its last
# character and moving backward, building up a new string one character
# at a time. Single loop, single direction -- no need to track two
# positions at once.


def reverse_string(s):
    new_s = ""
    i = len(s) - 1
    while i >= 0:
        new_s += s[i]
        i -= 1
    return new_s


print(reverse_string("hello"))  # "olleh"
