# Topic 3, Day 1 Homework

# Exercise 1: BMI calculator
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


praveen = calculate_bmi(70, 1.8)
rishi = calculate_bmi(74, 1.81)
print(praveen)
print(rishi)


# Exercise 2: is_even using a return value inside a loop
def is_even(number):
    return number % 2 == 0


for num in range(1, 11):
    if is_even(num):
        print(num)


# DSA micro-drill: total (accumulator pattern, no built-in sum())
def total(numbers):
    result = 0
    for num in numbers:
        result += num
    return result


print(total([1, 2, 3, 4, 5, 6]))
