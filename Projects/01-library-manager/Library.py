class Book:
    def __init__(self, title, author, is_borrowed = False):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrow_count = 0

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author} [{status}]"
class Library:
    def __init__(self):
        self.books = [] # Library HAS-A collection of Book objects

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
    def add_ebook(self, title, author, file_size):
        ebook = EBook(title, author, file_size)
        self.books.append(ebook)

    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                if not book.is_borrowed:
                    book.is_borrowed = True
                    book.borrow_count += 1
                else:
                    print("Book is already borrowed")
                return
        print("Book is Not Available")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.is_borrowed:
                book.is_borrowed = False
                return
        print("Book is Not Available")

    def show_available_books(self):
        for book in self.books:
            if not book.is_borrowed:
                print(book.title)

    def show_all_books(self):
        for book in self.books:
            print(book)

class EBook(Book):
    def __init__(self, title, author, file_size_mb):
        super().__init__(title, author)
        self.file_size_mb = file_size_mb

    def __str__(self):
        return f"{self.title} by {self.author} [{self.file_size_mb}]MB"
    
library = Library()

while True:
    print("Menu:\n1.Add Book\n2.Borrow Book\n3.Return Book\n4.View Available Books\n5.View All Books\n0.Exit")
    task = (input("Enter Task Number: "))
    if task.isdigit():
        task = int(task)
        if task == 0:
            break
        elif task == 1:
            title = input("Enter Book Title: ").strip()
            author = input("Enter Book Author: ").strip()
            library.add_book(title, author)
        elif task == 2:
            title = input("Enter Book Title: ").strip()
            library.borrow_book(title)
        elif task == 3:
            title = input("Enter Book Title: ").strip()
            library.return_book(title)
        elif task == 4:
            library.show_available_books()
        elif task == 5:
            library.show_all_books()
        else:
            continue
    else:
        print("Enter a Number")