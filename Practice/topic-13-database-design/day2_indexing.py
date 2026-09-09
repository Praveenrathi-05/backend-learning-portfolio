"""
Topic 13, Day 2: Indexing

Covered: an index is a real, physically-stored structure (typically a
B-Tree) the database builds and maintains alongside a table, enabling
O(log n) lookups instead of an O(n) full table scan. CREATE INDEX does
real, immediate work -- it scans and builds the structure from EXISTING
rows the moment it runs, and every future INSERT/UPDATE/DELETE must also
update the index to keep it in sync (the real, honest cost of indexing).

EXPLAIN QUERY PLAN is how you VERIFY (never assume) whether a query
actually uses an index: "SCAN table" means a full scan; "SEARCH table
USING INDEX ..." means the index is being used.

Genuine limitations worth remembering: a leading wildcard (LIKE '%x%')
defeats an index entirely, since the sorted structure can't help when a
match could be anywhere in the value. A composite index (multiple
columns together) is sorted by the FIRST column, then by later columns
WITHIN each first-column group -- it can efficiently answer queries on
the first column alone, or the first+second together, but generally
cannot efficiently answer a query on just the second column alone.

Indexing is a genuine trade-off (read speed vs. write speed vs. storage),
not a blanket "index everything" rule -- add indexes deliberately, on
columns that are actually frequently searched, filtered, or joined on.
"""

import sqlite3
import random
import time

# --- Homework 1: measure AND verify the effect of an index ---
# Goal: not just observe a timing difference (which can be noisy on a
# small/fast run), but confirm via EXPLAIN QUERY PLAN that the query
# plan itself actually changes from SCAN to SEARCH ... USING INDEX.

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE big_table (id INTEGER PRIMARY KEY, name TEXT)")

names = [f"user_{i}" for i in range(100000)]
random.shuffle(names)
cursor.executemany("INSERT INTO big_table (name) values (?)", [(n,) for n in names])
connection.commit()

start = time.time()
cursor.execute("SELECT * FROM big_table where name = 'user_5478'")
cursor.fetchone()
print(f"Without index: {time.time() - start:.6f}s")
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM big_table WHERE name = 'user_5478'")
print(cursor.fetchone())
# Expect to see "SCAN big_table" here

cursor.execute("CREATE INDEX idx_name ON big_table(name)")
start = time.time()
cursor.execute("SELECT * FROM big_table where name = 'user_5478'")
cursor.fetchone()
print(f"With index: {time.time() - start:.6f}s")
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM big_table WHERE name = 'user_5478'")
print(cursor.fetchone())
# Expect to see "SEARCH big_table USING INDEX idx_name (name=?)" here

connection.close()


# --- Homework 2: applying indexing to a real, existing project schema ---
# Goal: identify a genuinely busy column from a past project (Weekly
# Project #6's categories.name, filtered by spending_with_category_average)
# and confirm via EXPLAIN QUERY PLAN that the index is actually used --
# the honest way to verify this, independent of whether the dataset is
# large enough to show a visible timing difference.
#
# cursor.execute("CREATE INDEX idx_category_name ON categories(name)")
# -- confirmed via EXPLAIN QUERY PLAN: query plan correctly switches to
#    using the index


# --- DSA Micro-drill: binary_search ---
# Goal: the actual algorithm a B-Tree index is conceptually built around
# -- eliminate HALF the remaining search space with every comparison,
# rather than checking every element one by one (O(log n) vs O(n)).

def binary_search(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] < target:
            low = mid + 1
        elif sorted_list[mid] > target:
            high = mid - 1
        else:
            return mid
    return -1


print(binary_search([2, 5, 8, 12, 16, 23, 38, 45, 56, 72], 23))   # 5
print(binary_search([2, 5, 8, 12, 16, 23, 38, 45, 56, 72], 5))     # 1
print(binary_search([2, 5, 8, 12, 16, 23, 38, 45, 56, 72], 100))   # -1 (not found)
