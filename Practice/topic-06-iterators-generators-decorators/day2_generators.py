# Topic 6, Day 2 Homework -- Generators

# Exercise 1: countdown_by -- yields values, lazily, one at a time
def countdown_by(start, step):
    while start > 0:
        yield start
        start -= step


for value in countdown_by(10, 3):
    print(value)  # 10, 7, 4, 1


# Exercise 2: flatten rewritten as a generator (yield instead of .append())
def flatten(nested_list):
    i = 0
    while i < len(nested_list):
        j = 0
        while j < len(nested_list[i]):
            yield nested_list[i][j]
            j += 1
        i += 1


print(list(flatten([[1, 2, 3], [1, 2], [5], [9, 7, 3, 2, 7]])))
# [1, 2, 3, 1, 2, 5, 9, 7, 3, 2, 7]


# DSA micro-drill: fibonacci generator, stopping before exceeding a limit
def fibonacci(limit):
    first_number = 0
    second_number = 1
    while first_number < limit:
        yield first_number
        # multiple assignment -- both new values computed from OLD values
        # before either variable is overwritten
        first_number, second_number = second_number, first_number + second_number


print(list(fibonacci(10)))  # [0, 1, 1, 2, 3, 5, 8]
