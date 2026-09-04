import sqlite3, time
from pathlib import Path

file_name = Path(__file__).resolve().parent / "store.db"

connection = sqlite3.connect(file_name)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    category_id INTEGER,
    amount INTEGER,
    note TEXT,
    date TEXT
);
""")

cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Food",))
food_id = cursor.lastrowid

cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Transport",))
transport_id = cursor.lastrowid

cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Shopping",))
shopping_id = cursor.lastrowid

cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Entertainment",))
entertainment_id = cursor.lastrowid

cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Bills",))
bills_id = cursor.lastrowid

cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 250, "Groceries", "2025-01-03")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (transport_id, 120, "Bus pass", "2025-01-05")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (shopping_id, 1500, "Shoes", "2025-01-08")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (entertainment_id, 300, "Movie", "2025-01-10")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (bills_id, 2200, "Electricity", "2025-01-12")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 180, "Lunch", "2025-01-15")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (transport_id, 200, "Auto", "2025-01-18")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (shopping_id, 800, "Clothes", "2025-01-20")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 350, "Dinner", "2025-01-24")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (entertainment_id, 500, "Concert", "2025-01-27")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (bills_id, 1800, "Internet", "2025-02-02")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 600, "Groceries", "2025-02-05")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (transport_id, 150, "Cab", "2025-02-08")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (shopping_id, 2200, "Headphones", "2025-02-11")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (entertainment_id, 250, "Streaming", "2025-02-14")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 450, "Restaurant", "2025-02-18")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (transport_id, 100, "Bus", "2025-02-20")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (shopping_id, 700, "Backpack", "2025-02-23")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (bills_id, 2500, "Electricity", "2025-02-26")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 300, "Fruits", "2025-03-01")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (transport_id, 180, "Auto", "2025-03-04")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (shopping_id, 1200, "Jacket", "2025-03-07")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (entertainment_id, 400, "Movie", "2025-03-10")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (bills_id, 2100, "Water bill", "2025-03-13")
)
cursor.execute(
    "INSERT INTO expenses (category_id, amount, note, date) VALUES (?, ?, ?, ?)",
    (food_id, 550, "Dinner", "2025-03-16")
)


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function call took {end - start:.2f} seconds")
        return result
    return wrapper


def category_totals():
    cursor.execute("""
        SELECT c.name, SUM(amount) as total FROM categories c
        INNER JOIN expenses e ON e.category_id = c.id GROUP BY c.name
    """)
    return cursor.fetchall()


def above_average_categories():
    # Uses a derived table (subquery inside FROM) to compute the average
    # OF the per-category totals -- a two-level aggregation, not a flat
    # average across all individual expenses.
    cursor.execute("""
        SELECT c.name, SUM(e.amount) as total FROM categories c
        INNER JOIN expenses e ON e.category_id = c.id GROUP BY c.name HAVING total >
        (SELECT AVG(total) FROM (
            SELECT SUM(e.amount) AS total
            FROM categories c
            INNER JOIN expenses e ON e.category_id = c.id
            GROUP BY c.name
        ) AS avg_total)
    """)
    return cursor.fetchall()


def spending_with_category_average(category_name):
    # CTE computes one row (this category's own average), then that
    # single-row CTE is joined against every individual expense in the
    # category, broadcasting the average onto each expense row.
    cursor.execute("""
        WITH category_expenses as (
            SELECT c.name as name, AVG(e.amount) as avg, e.category_id as id
            FROM categories c INNER JOIN expenses e ON e.category_id = c.id
            WHERE c.name = (?) GROUP BY name
        )
        SELECT c.name, e.note, e.amount, c.avg FROM category_expenses c
        INNER JOIN expenses e ON e.category_id = c.id
    """, (category_name,))
    return cursor.fetchall()


def ranked_expenses_per_category():
    cursor.execute("""
        SELECT c.name, e.note, e.amount,
               RANK() OVER(PARTITION BY e.category_id ORDER BY amount DESC) as amount_rank
        FROM expenses e INNER JOIN categories c ON c.id = e.category_id
    """)
    return cursor.fetchall()


@timer
def top_expense_per_category():
    # Top-N-per-group pattern: CTE computes the rank per category,
    # outer query filters to rank <= 1 -- can't filter a window
    # function's result directly in the same query level it's computed.
    cursor.execute("""
        WITH ranked AS (
            SELECT c.name, e.note, e.amount,
                   RANK() OVER(PARTITION BY e.category_id ORDER BY amount DESC) as amount_rank
            FROM expenses e INNER JOIN categories c ON c.id = e.category_id
        )
        SELECT * FROM ranked WHERE amount_rank <= 1
    """)
    return cursor.fetchall()


def get_categories():
    cursor.execute("SELECT name FROM categories")
    return [category[0] for category in cursor.fetchall()]


def menu():
    while True:
        print("1. Category totals\n2. Above-average categories\n3. Spending with category average\n"
              "4. Ranked expenses\n5. Top expense per category\n6. Exit")
        try:
            task = int(input("Enter Task Number: "))
        except ValueError:
            print("Type a Number")
        else:
            if task == 1:
                print(category_totals())
            elif task == 2:
                print(above_average_categories())
            elif task == 3:
                while True:
                    name = input("Enter Category Name: ").title()
                    if name != "":
                        if name in get_categories():
                            break
                        else:
                            print("Invalid category. Please choose from the available categories.")
                print(spending_with_category_average(name))
            elif task == 4:
                print(ranked_expenses_per_category())
            elif task == 5:
                print(top_expense_per_category())
            elif task == 6:
                break
            else:
                print("Not a valid task")


connection.commit()

# NOTE: menu() must run WHILE the connection is still open, since every
# report function calls cursor.execute(). connection.close() has to come
# AFTER menu() fully returns -- not before it's ever called. The original
# ordering had close() run immediately, before menu() was even invoked,
# which would raise "Cannot operate on a closed database" the instant
# any menu option tried to query.
if __name__ == "__main__":
    menu()

connection.close()
