"""
Topic 13, Day 3: Beyond B-Trees -- Index Types, UNIQUE Constraints & Real Design Judgment

Covered: UNIQUE does two things together -- a constraint (rejects
duplicate inserts with sqlite3.IntegrityError) AND an automatic index
(enforcing uniqueness efficiently needs the same fast-lookup structure
as a normal index). Foreign keys are NOT automatically indexed in
SQLite -- a deliberate design choice, since the database can't know
your actual access patterns just from a column being a foreign key;
indexing every FK automatically would impose a real write-cost even on
tables where that column is rarely searched/joined on. The
responsibility to index FKs is left to the schema designer, using real
judgment, not a blanket automatic rule.

Hash indexes: O(1) exact-match lookups, but no concept of ORDER, so
they can't help range queries (WHERE price > 100) at all -- a B-Tree's
sorted structure is what makes ranges efficient, which is exactly why
B-Trees remain the general-purpose default. Full-text indexes are a
genuinely different tool again, for searching INSIDE text content --
neither a B-Tree nor hash index can efficiently answer a LIKE '%x%'
style query.

Real indexing decision checklist (used in this homework's DSA drill):
1. Is the column used in WHERE/JOIN/ORDER BY frequently?
2. Is it a foreign key? (almost always index it)
3. Does it need uniqueness enforced? (use UNIQUE)
4. Is the table small? (index may not even be used regardless)
5. Is the table write-heavy and read-rarely? (index may hurt more than help)
6. When in doubt, check EXPLAIN QUERY PLAN -- never assume.
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

# --- Homework 1: audit + fix every foreign key across all prior projects ---
# Goal: comprehensive fix -- every FK column across Topics 11-13 has been
# silently un-indexed until now. CREATE INDEX IF NOT EXISTS is safe to
# re-run without erroring if the index already exists.

foreign_keys_to_index = [
    ("orders", "product_id"),        # Topics 11-12 store/orders schema
    ("expenses", "category_id"),      # Weekly Project #6
    ("member", "trainer_id"),          # Topic 13 Day 1 gym schema
    ("member", "plan_id"),
]

for table, column in foreign_keys_to_index:
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_{column} ON {table}({column})")

connection.commit()

# Verify via EXPLAIN QUERY PLAN that a representative join now uses the index
cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT store.name, orders.quantity FROM store
    INNER JOIN orders ON store.id = orders.product_id
""")
print(cursor.fetchall())
# Expect to see "... USING INDEX idx_orders_product_id ..." referencing orders


# --- Homework 2: UNIQUE constraint + proof it rejects a duplicate ---
# Goal: a real data-integrity guardrail (not just a speed optimization) --
# applied to Weekly Project #6's categories.name, since two categories
# sharing a name would create real ambiguity in every WHERE c.name = ?
# lookup the reporting functions rely on. See finance_dashboard.py
# (Weekly Project #6) for the actual applied version:
#
#   CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE)
#
#   try:
#       cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Food",))
#       connection.commit()
#   except sqlite3.IntegrityError as e:
#       print(f"Insert failed: {e}")   # correctly fires on the duplicate


# --- DSA Micro-drill: would_benefit_from_index ---
# Goal: translate the 6-point decision checklist into explicit, checkable
# conditions -- gated on "is this column ever filtered/joined on at all"
# first (used_in_filter), then an OR between "genuinely high read volume"
# and "table large enough that even an occasional scan is expensive" --
# either is sufficient on its own -- and finally, writes must not exceed
# reads (don't index a write-heavy, read-light column).

def would_benefit_from_index(access_pattern):
    reads = access_pattern['reads_per_day']
    writes = access_pattern['writes_per_day']
    used_in_filter = access_pattern['used_in_where_or_join']
    rows = access_pattern['row_count']

    return (
        used_in_filter
        and (reads > 10000 or rows > 100000)
        and writes <= reads
    )


print(would_benefit_from_index({
    "reads_per_day": 50000, "writes_per_day": 10,
    "used_in_where_or_join": True, "row_count": 2000000
}))
# True -- read-heavy, filtered/joined on frequently, large table

print(would_benefit_from_index({
    "reads_per_day": 5, "writes_per_day": 50000,
    "used_in_where_or_join": False, "row_count": 500
}))
# False -- write-heavy, rarely queried, tiny table, never filtered on

connection.close()
