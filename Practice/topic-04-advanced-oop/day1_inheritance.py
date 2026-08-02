# Topic 4, Day 1 Homework -- Inheritance

# Exercise 1: Person -> Student, extending __init__ and a method with super()
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old."


class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def introduce(self):
        description = super().introduce()
        return f"{description}, studying at {self.school}."


student = Student("Priya", 20, "IIT Delhi")
print(student.introduce())


# Exercise 2: EBook extending Book from the Library Manager project
class Book:
    def __init__(self, title, author, is_borrowed=False):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrow_count = 0


class EBook(Book):
    def __init__(self, title, author, file_size_mb):
        super().__init__(title, author)
        self.file_size_mb = file_size_mb


ebook = EBook("Deep Work", "Cal Newport", 4)
print(ebook.title, ebook.author, ebook.file_size_mb)


# DSA micro-drill: most_frequent using a dict as a frequency counter
def most_frequent(lst):
    values = {}
    most_frequent_value = 0
    time_appeared = 0
    for val in lst:
        values[val] = values.get(val, 0) + 1
        if values[val] > time_appeared:
            time_appeared = values[val]
            most_frequent_value = val
    return most_frequent_value


print(most_frequent([1, 2, 1, 2, 3, 2, 1, 1]))  # 1
print(most_frequent([1]))                         # 1 -- edge case: single element
