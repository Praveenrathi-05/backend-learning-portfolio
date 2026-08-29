"""
Topic 11, Day 3: Aggregation -- GROUP BY, COUNT, AVG, HAVING

Covered: GROUP BY collapses many rows into one row per distinct group,
with any aggregate function (SUM, COUNT, AVG, MIN, MAX) computed once per
group, not once overall. COUNT(*) counts rows in a group regardless of
column contents; COUNT(column) counts only non-NULL values in that column
-- these differ the moment a column can genuinely be NULL.

HAVING filters GROUPS after aggregation; WHERE filters individual ROWS
before grouping/aggregation even happens -- which is precisely why WHERE
cannot reference an aggregate result at all (it runs too early in the
pipeline to see one). Full logical execution order:
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT.

Also confirmed: GROUP BY only ever operates on rows that already survived
an earlier INNER JOIN -- a product with zero matching orders is excluded
by the JOIN before grouping ever runs, so it stays absent even with
GROUP BY added on top.
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

# --- Homework 1: per-product order count + total quantity, all at once ---
# Goal: the real, general-purpose version of Day 2's one-product-at-a-time
# total_spent_by_product -- GROUP BY + COUNT(*) + SUM together, in a single
# query, rather than looping over products calling a function per product.

cursor.execute("""
    SELECT store.name, COUNT(*) as num_orders, SUM(orders.quantity) as total_units
    FROM store
    INNER JOIN orders ON store.id = orders.product_id
    GROUP BY store.name
""")
result = cursor.fetchall()
print(result)
# [('cheese', 1, 20), ('ghee', 1, 10), ('milk', 2, 72)]
# "chaas" (zero orders) is still absent -- INNER JOIN excludes it BEFORE
# GROUP BY ever runs, so grouping can't resurrect a row that was never
# in its input to begin with.


# --- Homework 2: HAVING to filter on an aggregated total ---
# Goal: filter on the RESULT of SUM(), which WHERE structurally cannot do
# (WHERE runs before grouping/aggregation exists at all).

cursor.execute("""
    SELECT store.name FROM store
    INNER JOIN orders ON store.id = orders.product_id
    GROUP BY store.name HAVING SUM(orders.quantity) > 30
""")
result = cursor.fetchall()
print(result)
# [('milk',)] -- only milk's total (72) actually exceeds the threshold


# --- DSA Micro-drill: group_and_aggregate ---
# Goal: reuse Day 2's group_by_key() rather than reimplementing its logic
# -- compose two small functions instead of duplicating grouping logic in
# a second place. Then apply an arbitrary passed-in function (sum, max,
# len, anything) to each category's collected list.

def group_by_key(records):
    new_records = {}
    for record in records:
        new_records[record[0]] = new_records.get(record[0], []) + [record[1]]
    return new_records


def group_and_aggregate(records, agg_func):
    new_records = group_by_key(records)
    for record in new_records:
        new_records[record] = agg_func(new_records[record])
    return new_records


print(group_and_aggregate([("food", 200), ("transport", 50), ("food", 150)], sum))
# {'food': 350, 'transport': 50}
print(group_and_aggregate([("food", 200), ("transport", 50), ("food", 150)], max))
# {'food': 200, 'transport': 50}
print(group_and_aggregate([("food", 200), ("transport", 50), ("food", 150)], len))
# {'food': 2, 'transport': 1}

connection.close()
