# Topic 1, Day 1 Homework
# Exercise 1: FizzBuzz
# Goal: practice control flow branching order (check "both" before individual checks)

number = int(input("Enter a number: "))
if number % 3 == 0 and number % 5 == 0:
    print("FizzBuzz")
elif number % 3 == 0:
    print("Fizz")
elif number % 5 == 0:
    print("Buzz")
else:
    print(number)
