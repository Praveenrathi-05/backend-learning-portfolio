import os, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Expense:
    def __init__(self, amount, category, note):
        self.amount = amount
        self.category = category
        self.note = note

    def __str__(self):
        return f"₹{self.amount} - {self.category} ({self.note})"


class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def log_action(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"Running {func.__name__} and it took {end - start:.4f} seconds")
            return result
        return wrapper

    @log_action
    def add_expense(self, amount, category, note):
        self.expenses.append(Expense(amount, category, note))

    @log_action
    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for expense in self.expenses:
                file.write(f"{expense.amount},{expense.category},{expense.note}\n")

    def load_from_file(self, filename):
        self.expenses = []
        try:
            with open(filename) as file:
                for line in file:
                    line = line.strip()
                    amount, category, note = line.split(",")
                    self.expenses.append(Expense(float(amount), category, note))
        except FileNotFoundError:
            print("No saved expenses found. Starting with an empty expense list.")

    def category_totals(self):
        # Full scan required before any total can be trusted: a category's
        # running total isn't final until every expense has been seen, since
        # expenses for the same category can appear anywhere in the list.
        # (If expenses were pre-sorted/grouped by category, a category's total
        # could be yielded incrementally as soon as the category changes --
        # see practice notes for that alternate version.)
        categories = {}
        i = 0
        while i < len(self.expenses):
            if self.expenses[i].category in categories:
                categories[self.expenses[i].category] += self.expenses[i].amount
            else:
                categories[self.expenses[i].category] = self.expenses[i].amount
            i += 1
        for key, value in categories.items():
            yield (key, value)

    def total_spent(self):
        return sum(expense.amount for expense in self.expenses)


expenseTracker = ExpenseTracker()
filename = "expenses.txt"
expenseTracker.load_from_file(filename)

while True:
    print("1.Add Expense\n2.View All Expenses\n3.View Category Totals\n4.View Total Spent\n5.Save to File\n0.Exit (auto-saves before exiting)")
    try:
        task = int(input("Enter Task Number: "))
    except ValueError:
        print("Type a Number")
    else:
        if task == 1:
            try:
                amount = float(input("Enter amount: ").strip())
            except ValueError:
                print("Amount should be a number")
            else:
                category = input("Enter category: ").strip()
                note = input("Enter note: ").strip()
                expenseTracker.add_expense(amount, category, note)
        elif task == 2:
            for expense in expenseTracker.expenses:
                print(expense)
        elif task == 3:
            for expense in expenseTracker.category_totals():
                print(expense)
        elif task == 4:
            print(expenseTracker.total_spent())
        elif task == 5:
            expenseTracker.save_to_file(filename)
        elif task == 0:
            expenseTracker.save_to_file("expenses.txt")
            break
        else:
            print("Not a valid task")
