# Topic 2, Day 1 Homework
# Exercise 1: Lists -- append and remove by value
foods = ["pizza", "pavbhaji", "panipuri", "vadapav", "frankie"]
foods.append("Rasmalai")
foods.remove("pavbhaji")
print(foods)
print(len(foods))

# Exercise 2: Tuples -- demonstrating immutability
birthplace = ("bikaner", "Rajasthan")
# Uncommenting the next line will crash with:
# TypeError: 'tuple' object does not support item assignment
# birthplace[0] = "nokha"
# This is useful because a birthplace is a fixed fact that should never be
# accidentally overwritten elsewhere in a larger program.
