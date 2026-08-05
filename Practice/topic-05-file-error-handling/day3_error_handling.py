# Topic 5, Day 3 Homework -- Error Handling

# Exercise 1: count_lines, now handling a missing file gracefully
def count_lines(filename):
    count = 0
    try:
        with open(filename, "r") as file:
            for _ in file:
                count += 1
        return count
    except FileNotFoundError:
        print("File does not exist")
        return count


print(count_lines("Hello.txt"))  # File does not exist -> 0


# Exercise 2: safe_divide -- catch ZeroDivisionError instead of crashing
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


print(safe_divide(10, 2))   # 5.0
print(safe_divide(5, 0))     # None


# DSA micro-drill: safe_get -- use try/except IndexError instead of a
# manual length check; negative indices remain valid
def safe_get(lst, index):
    try:
        return lst[index]
    except IndexError:
        return "Not found"


print(safe_get([10, 20, 30], 1))    # 20
print(safe_get([10, 20, 30], 10))   # "Not found"
print(safe_get([10, 20, 30], -1))   # 30 -- negative indexing still valid
