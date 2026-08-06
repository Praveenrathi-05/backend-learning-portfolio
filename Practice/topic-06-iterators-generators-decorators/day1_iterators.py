# Topic 6, Day 1 Homework -- Iterators

# Exercise 1: custom iterator class producing even numbers up to a limit
class EvenNumbers:
    def __init__(self, end):
        self.start = 2
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.start > self.end:
            raise StopIteration
        value = self.start
        self.start += 2
        return value


for count in EvenNumbers(9):
    print(count)  # 2, 4, 6, 8


# Exercise 2: manual iter()/next() combined with error handling
items = ["phone", "laptop", "watch"]
iterator = iter(items)

try:
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))  # no 4th item -> raises StopIteration
except StopIteration:
    print("End of list")


# DSA micro-drill: flatten a list of lists into one flat list
def flatten(nested_list):
    values = []
    for lst in nested_list:
        for value in lst:
            values.append(value)
    return values


print(flatten([[1, 2], [3, 4], [5]]))  # [1, 2, 3, 4, 5]
