# Topic 3, Day 2 Homework

# Exercise 1: default parameters + keyword arguments
def describe_student(name, grade="Not Assigned"):
    print(f"{name}'s grade: {grade}")


describe_student("Praveen")
describe_student(grade="B", name="Sudha")


# Exercise 2: get_min_max without using min()/max(), returning multiple values
def get_min_max(numbers):
    minimum = numbers[0]
    maximum = numbers[0]
    for i in range(1, len(numbers)):
        if minimum > numbers[i]:
            minimum = numbers[i]
        if maximum < numbers[i]:
            maximum = numbers[i]
    return minimum, maximum


minimum, maximum = get_min_max([1, 2, 5, 8, -4])
print(minimum, maximum)


# DSA micro-drill: count_vowels, character-by-character
def count_vowels(word):
    vowels = "aeiou"
    count = 0
    for char in word.lower():
        if char in vowels:
            count += 1
    return count


print(count_vowels("Praveen"))
