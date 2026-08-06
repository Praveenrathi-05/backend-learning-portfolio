# Topic 6, Day 3 Homework -- Decorators

# Exercise 1: decorator that uppercases a wrapped function's string return value
def uppercase_output(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


@uppercase_output
def introduce(name):
    return f"Hi, I'm {name}"


print(introduce("Praveen"))  # "HI, I'M PRAVEEN"


# Exercise 2: decorator that tracks call count PER decorated function,
# using nonlocal so each decorated function gets its own independent counter
# (a global counter would incorrectly be shared across every decorated function)
def call_counter(func):
    counter = 0

    def wrapper(*args, **kwargs):
        nonlocal counter
        counter += 1
        print(counter)
        return func(*args, **kwargs)

    return wrapper


@call_counter
def hello():
    print("Hello")


hello()
hello()
hello()  # 1, Hello / 2, Hello / 3, Hello


# DSA micro-drill: unique_values -- lazily deduplicate a list using yield
def unique_values(lst):
    seen = {}
    i = 0
    while i < len(lst):
        if lst[i] not in seen:
            seen[lst[i]] = True
            yield lst[i]
        i += 1


print(list(unique_values([1, 2, 2, 3, 1, 4, 7, 7, 9, 8, 3, 2, 1])))
# [1, 2, 3, 4, 7, 9, 8]
