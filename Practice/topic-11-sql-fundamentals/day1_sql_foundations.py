"""
Topic 11, Day 1: SQL Foundations

Covered: the shift from imperative (Python) to declarative (SQL) thinking;
setting up a real SQLite database via sqlite3 (connection, cursor, commit);
CREATE TABLE, PRIMARY KEY; parameterized queries (?) and why they prevent
SQL injection; SELECT/WHERE/ORDER BY/LIMIT and SQL's actual logical
execution order (FROM -> WHERE -> SELECT -> ORDER BY); LIKE pattern
matching; .fetchall() (returns [] on no match) vs .fetchone() (returns
None on no match) -- and the one-element-tuple trailing-comma trap.

Note: SQL uses a single "=" for equality, not Python's "==" -- SQLite
tolerates "==" as a non-standard convenience, but "=" is the correct,
portable habit across every real database engine.
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS store(
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        in_stock INTEGER
    )
""")

# --- Homework 1: create + insert (executemany) + three query types ---
# Goal: full round trip -- create, insert safely with parameters, and
# query using WHERE / ORDER BY / LIKE.

stocks_to_add = [
    ("Soya", 30, 400),
    ("Chips", 10, 150),
    ("Sugar", 60, 200),
    ("Wheat", 40, 550),
    ("Cheese", 120, 53),
]
cursor.executemany(
    "INSERT INTO store (name, price, in_stock) VALUES (?, ?, ?)",
    stocks_to_add
)
connection.commit()

# (a) all in-stock products, sorted by price ascending
cursor.execute("SELECT * FROM store WHERE in_stock > 0 ORDER BY price")
print(cursor.fetchall())

# (b) all products with price greater than a chosen value
cursor.execute("SELECT * FROM store WHERE price > 100")
print(cursor.fetchall())

# (c) all products whose name contains a specific substring
cursor.execute("SELECT * FROM store WHERE name LIKE '%c%'")
print(cursor.fetchall())


# --- Homework 2: find_product_by_id using .fetchone() ---
# Goal: the specific None-check .fetchone() requires -- unlike .fetchall(),
# which returns [] (falsy but safely iterable) on no match, .fetchone()
# returns None (falsy AND not indexable -- an unchecked result[i] on it
# would crash with a TypeError).

def find_product_by_id(product_id):
    cursor.execute("SELECT * FROM store WHERE id = ?", (product_id,))
    available = cursor.fetchone()
    if available:
        return available
    return "No product found with that id"


print(find_product_by_id(3))    # existing id -> real row tuple
print(find_product_by_id(99))    # missing id -> friendly message


# --- DSA Micro-drill: second_highest_price ---
# Goal: extend Topic 4's second_largest to track a (name, price) PAIR at
# each step, not just the raw number, so the name and price never get
# mismatched as the two trackers update.

def second_highest_price(products):
    highest = (0, float("-inf"))
    second_highest = (0, float("-inf"))
    for product in products:
        if product[1] > highest[1]:
            second_highest = highest
            highest = product
        elif highest[1] > product[1] > second_highest[1]:
            second_highest = product
    return (f'"{second_highest[0]}" -- {highest[1]} is highest, '
            f'{second_highest[1]} is second-highest')


print(second_highest_price([("Pen", 10), ("Notebook", 50), ("Bag", 800), ("Pencil", 5)]))
# "Notebook" -- 800 is highest, 50 is second-highest

connection.close()
