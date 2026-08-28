"""
Topic 11, Day 2: Joins

Covered: why relational databases split related data across tables instead
of nesting it (a table cell can only ever hold one plain value); foreign
keys (a column holding another table's primary key, linking rows without
nesting); cursor.lastrowid to grab an auto-generated id right after an
insert; INNER JOIN + ON to combine rows from two tables based on a match
condition; the critical behavior that INNER JOIN silently drops any row
with no match at all, on either side; and SUM() to combine multiple
matching rows into one number at the database level.

Debugging trail worth keeping, since it's the real lesson of the day:
.fetchall() on a SUM() query still returns a LIST -> .fetchone() is
correct here, since SUM() always collapses to exactly one row. But even
.fetchone() still hands back a TUPLE, e.g. (2520,) -- needs result[0] to
get the plain number out. And SUM() over zero matching rows returns NULL
(None) INSIDE that one-row tuple -- i.e. (None,), which is a non-empty,
truthy tuple -- so `if result:` alone is NOT enough; the check has to be
on result[0] specifically (`if result[0] is not None:`), since a plain
`if result[0]:` would also incorrectly treat a legitimate total of 0 as
"not found".
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER
    )
""")

# --- Homework 1: foreign key relationship + INNER JOIN + vanishing-row test ---
# Goal: build a real foreign-key relationship from scratch (orders.product_id
# references store.id), and directly verify that a product with ZERO orders
# ("chaas") is genuinely absent from the joined result.

cursor.execute("INSERT INTO store (name, price, in_stock) VALUES (?, ?, ?)", ("cheese", 120, 67))
cheese_id = cursor.lastrowid
cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (cheese_id, 20))

cursor.execute("INSERT INTO store (name, price, in_stock) VALUES (?, ?, ?)", ("ghee", 550, 25))
ghee_id = cursor.lastrowid
cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (ghee_id, 10))

cursor.execute("INSERT INTO store (name, price, in_stock) VALUES (?, ?, ?)", ("milk", 35, 120))
milk_id = cursor.lastrowid
cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (milk_id, 32))
cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (milk_id, 40))

# Deliberately given ZERO orders -- proves INNER JOIN excludes unmatched rows
cursor.execute("INSERT INTO store (name, price, in_stock) VALUES (?, ?, ?)", ("chaas", 20, 40))

connection.commit()

cursor.execute("""
    SELECT store.name, store.price, orders.quantity
    FROM store
    INNER JOIN orders ON store.id = orders.product_id
""")
result = cursor.fetchall()
print(result)
# "chaas" never appears anywhere in this list -- confirmed.


# --- Homework 2: total_spent_by_product ---
# Goal: JOIN + WHERE + SUM() combined -- a real, single-number reporting
# query, with correct handling of the "no matching product" edge case.

def total_spent_by_product(product_name):
    cursor.execute("""
        SELECT SUM(store.price * orders.quantity)
        FROM store
        INNER JOIN orders ON store.id = orders.product_id
        WHERE store.name = ?
    """, (product_name,))
    result = cursor.fetchone()
    if result[0] is not None:
        return result[0]
    return "a product that does not exist"


print(total_spent_by_product("milk"))    # 2520
print(total_spent_by_product("ghee"))     # 5500
print(total_spent_by_product("a product that does not exist"))
# "a product that does not exist"


# --- DSA Micro-drill: group_by_key ---
# Goal: extend the dict-as-counter pattern (most_frequent) to COLLECT
# values into a list per key, instead of counting occurrences --
# .get(key, []) supplies an empty list the first time a key is seen,
# and the existing list every time after.

def group_by_key(records):
    new_records = {}
    for record in records:
        new_records[record[0]] = new_records.get(record[0], []) + [record[1]]
    return new_records


print(group_by_key([("food", 200), ("transport", 50), ("food", 150), ("rent", 8000)]))
# {'food': [200, 150], 'transport': [50], 'rent': [8000]}

connection.close()
