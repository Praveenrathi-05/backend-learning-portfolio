# Topic 4, Day 2 Homework -- Polymorphism

# Exercise 1: PaymentMethod hierarchy, called polymorphically (no if/elif type-checking)
class PaymentMethod:
    def pay(self, amount):
        return f"Paid ₹{amount} via Generic Method"


class CreditCard(PaymentMethod):
    def pay(self, amount):
        return f"Paid ₹{amount} via Credit Card"


class UPI(PaymentMethod):
    def pay(self, amount):
        return f"Paid ₹{amount} via UPI"


payments = [PaymentMethod(), CreditCard(), UPI()]
for payment in payments:
    print(payment.pay(500))


# Exercise 2: Library Manager -- polymorphic display_info() across Book and EBook
class Book:
    def __init__(self, title, author, is_borrowed=False):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrow_count = 0

    def display_info(self):
        status = "Not Available" if self.is_borrowed else "Available"
        return f"{self.title}, ({status}), {self.borrow_count} times borrowed"


class EBook(Book):
    def __init__(self, title, author, file_size_mb):
        super().__init__(title, author)
        self.file_size_mb = file_size_mb

    def display_info(self):
        return f"{self.title} by {self.author} [{self.file_size_mb}MB]"


library_items = [Book("Deep Work", "Cal Newport"), EBook("Atomic Habits", "James Clear", 10)]
for item in library_items:
    print(item.display_info())


# DSA micro-drill: second_largest, distinct values, single pass, no sorting
def second_largest(lst):
    largest = float("-inf")
    second = float("-inf")
    for num in lst:
        if num > largest:
            second = largest
            largest = num
        elif num > second and num != largest:
            second = num
    return second


print(second_largest([2, 1, 3, 4, 2]))  # 3
print(second_largest([5, 5, 3]))          # 3 -- edge case: duplicate largest value
