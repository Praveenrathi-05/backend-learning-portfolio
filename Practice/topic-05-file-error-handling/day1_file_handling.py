# Topic 5, Day 1 Homework -- File Handling Foundations

# Exercise 1: write 3 movies to a file, then read it back to confirm
with open("movies.txt", "w") as file:
    for i in range(3):
        movie = input("Enter your favourite movie: ")
        file.write(movie + "\n")

with open("movies.txt", "r") as file:
    content = file.read()
    print(content)


# Exercise 2: append ONE more movie without erasing the existing ones,
# then read back to confirm all 4 are present
with open("movies.txt", "a") as file:
    movie = input("Enter your favourite movie: ")
    file.write(movie + "\n")

with open("movies.txt", "r") as file:
    content = file.read()
    print(content)


# DSA micro-drill: count_lines -- iterate over the file object directly
# (line by line) instead of loading the whole file into one string first
def count_lines(filename):
    count = 0
    with open(filename, "r") as file:
        for _ in file:
            count += 1
    return count


print(count_lines("movies.txt"))  # 4
