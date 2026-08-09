# Topic 7, Day 1 -- DSA Micro-Drill

# is_balanced: checks whether a string of parentheses is correctly
# matched and nested.
#
# Two distinct failure conditions to handle:
#   1. running counter goes negative mid-scan -> a ')' with nothing to match
#   2. counter isn't back to 0 at the very end -> some '(' never got closed
# The negative check must happen INSIDE the loop (not just at the end),
# otherwise a case like ")(" would wrongly look balanced (net = 0 at the end).


def is_balanced(s):
    value = 0
    for char in s:
        if char == "(":
            value += 1
        elif char == ")":
            value -= 1
        if value < 0:
            return False
    return value == 0


print(is_balanced("(())"))   # True
print(is_balanced("(()"))     # False -- unclosed open paren
print(is_balanced(")("))      # False -- close paren with nothing to match
