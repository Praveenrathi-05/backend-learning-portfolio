# Topic 1, Day 1 Homework
# Exercise 2: Mutability vs Rebinding
# Goal: demonstrate the difference between immutable rebinding and mutable in-place change

# Example 1: immutable (int) - reassignment does NOT affect the other variable
x = 5
y = x
x += 5
print(y)  # 5 -- y is untouched, x was rebound to a new object

# Example 2: mutable (list) - mutation DOES affect the other variable
arr = [1, 2, 3, 4]
new_arr = arr
arr.append(5)
print(new_arr)  # [1, 2, 3, 4, 5] -- both names point to the same object
