# Topic 5, Day 2 Homework -- Bridge & Reinforcement (File Handling)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Exercise 1: read movies.txt with .readlines(), print each with a position number
with open("movies.txt", "r") as file:
    lines = file.readlines()
    for i in range(len(lines)):
        print(f"{i+1}. {lines[i].strip()}")


# Exercise 2: structured data round-trip -- write (name, score) pairs,
# read them back, reconstruct, convert, and compute the average
with open("scores.txt", "w") as file:
    file.write("Praveen,85\n")
    file.write("Ritika,92\n")
    file.write("Vinit,78\n")

with open("scores.txt", "r") as file:
    scores = []
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        _, score = line.split(",")
        scores.append(int(score))
    print(sum(scores) / len(scores))


# DSA micro-drill: find_duplicates -- each repeated value appears exactly
# once in the output, no matter how many times it repeats in the input
def find_duplicates(lst):
    values = {}
    duplicates = []
    for num in lst:
        if num in values:
            if values[num] == 1:
                duplicates.append(num)   # append only the moment count crosses 1 -> 2
            values[num] += 1
        else:
            values[num] = 1
    return duplicates


print(find_duplicates([1, 2, 2, 3, 3, 3, 4, 4, 7, 9, 9, 8, 8, 3]))
# [2, 3, 4, 9, 8]
