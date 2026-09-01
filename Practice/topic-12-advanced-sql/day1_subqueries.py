"""
Topic 12, Day 1: Subqueries

Covered: a subquery is a complete SELECT nested inside another query --
always read from the INSIDE OUT, innermost query first. Scalar subqueries
(exactly one value, usable with =/>/<), IN/NOT IN (subquery returns
multiple values), EXISTS (checks only whether ANY row comes back, ignores
its content -- SELECT 1 is idiomatic since the value itself is unused).

Correlated vs uncorrelated: the precise, syntactic TEST for correlation is
whether the inner query references a column belonging to the OUTER
query's table/alias. An uncorrelated subquery computes its answer once,
independent of the outer query. A correlated subquery's answer depends on
which outer row is currently being considered, so the database must
re-execute it once per outer row -- a real, honest performance cost worth
being aware of on large tables.

Also learned directly, by comparison: a technically-correct but
over-engineered query (nested EXISTS, two levels of correlation) is often
a sign a simpler formulation exists -- here, COUNT(*) > N inside a single
correlated subquery expressed "more than one order" far more simply than
nested EXISTS did, with identical results.
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()


# --- Homework 1: products priced below the average of ORDERED products ---
# Goal: nesting a subquery inside a subquery -- the innermost query
# collects which products were ever ordered (directly from orders.product_id,
# no join needed -- that column already lives there), the middle query
# averages price only among those, the outer query filters ALL products
# against that threshold.

cursor.execute("""
    SELECT name FROM store
    WHERE price < (
        SELECT AVG(price) FROM store
        WHERE id IN (SELECT product_id FROM orders)
    )
""")
print(cursor.fetchall())
# average of ordered products (cheese 120, ghee 550, milk 35) = 235
# -> cheese, milk, chaas all qualify (chaas itself was never ordered, but
#    the OUTER where still checks it against every row in store)


# --- Homework 2: products ordered more than once, via a correlated subquery ---
# Goal: solve a GROUP BY/HAVING-shaped problem (Topic 11) using a
# correlated subquery instead -- COUNT(*) > N is the simple, idiomatic
# pattern here, preferred over nested EXISTS for expressing a QUANTITY
# rather than pure existence.

cursor.execute("""
    SELECT name FROM store s WHERE
    (SELECT count(*) FROM orders o WHERE o.product_id = s.id) > 1
""")
print(cursor.fetchall())
# [('milk',)] -- milk has 2 orders, the only product exceeding 1


# --- DSA Micro-drill: values_above_average ---
# Goal: mirror the SQL "price > (SELECT AVG(price)...)" pattern in plain
# Python -- a genuine two-pass problem: compute the average first (pass 1,
# requires seeing every value), THEN filter using that stored result
# (pass 2) -- can't be done in a single pass, since you don't know the
# average until you've seen everything.

def values_above_average(numbers):
    average = sum(numbers) / len(numbers)
    return [num for num in numbers if num > average]


print(values_above_average([10, 20, 30, 40]))
# [30, 40]  -- average is 25

connection.close()
