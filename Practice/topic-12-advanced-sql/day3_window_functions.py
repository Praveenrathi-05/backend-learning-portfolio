"""
Topic 12, Day 3: Window Functions

Covered: window functions compute a value across a set of related rows
WITHOUT collapsing them -- every original row survives, unlike GROUP BY.
PARTITION BY splits rows into groups (like GROUP BY) but the window
function computes separately WITHIN each group, with no collapsing.

RANK() vs DENSE_RANK() vs ROW_NUMBER(): RANK() leaves a gap exactly the
size of a tie (1, 1, 3); DENSE_RANK() has no gap (1, 1, 2); ROW_NUMBER()
never ties at all, always strictly sequential. LAG()/LEAD() look at the
previous/next row (within a partition, if PARTITION BY is present).

A window function's result cannot be filtered with WHERE in the same
query level it's computed in (WHERE runs before it exists) -- must wrap
in a CTE or subquery and filter the OUTER layer instead. This is the
real mechanism behind the classic "top N per group" interview pattern.

Real bug caught and fixed in Homework 2: GROUP BY collapses rows into
one per group BEFORE ranking ever runs, which answers "which ONE product
wins overall" -- not "each product's own best order." The fix: keep
every individual row intact (no GROUP BY/SUM), and let PARTITION BY do
the per-group scoping instead, inside the window function itself.
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

# --- Homework 1: global rank vs PARTITION BY rank, side by side ---
# Goal: directly experience the before/after effect of adding PARTITION BY,
# most visible on "milk" (2 orders) -- globally its orders compete against
# every other product's orders; partitioned, they only compete with each
# other.

cursor.execute("""
    SELECT store.name, orders.quantity,
           store.price * orders.quantity AS order_value,
           RANK() OVER(ORDER BY store.price * orders.quantity DESC) as value_rank
    FROM store
    INNER JOIN orders ON store.id = orders.product_id
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT store.name, orders.quantity,
           store.price * orders.quantity AS order_value,
           RANK() OVER(PARTITION BY store.name ORDER BY store.price * orders.quantity DESC) as value_rank
    FROM store
    INNER JOIN orders ON store.id = orders.product_id
""")
print(cursor.fetchall())


# --- Homework 2: single highest-value order PER PRODUCT (top-N-per-group) ---
# Goal: the canonical "top N per group" interview pattern. Keep every
# individual order as its own row (no GROUP BY/SUM collapsing them first),
# rank each product's orders against only that same product's other
# orders via PARTITION BY, then wrap in a CTE to filter on the resulting
# rank (WHERE can't see a window function's result directly).

cursor.execute("""
    WITH order_products AS (
        SELECT store.name as name, orders.quantity * store.price as total_price, store.price as price
        FROM store INNER JOIN orders on store.id = orders.product_id
    ), order_stats AS (
        SELECT name, total_price, RANK() OVER (
            PARTITION BY name ORDER BY total_price DESC
        ) as rank FROM order_products
    )
    SELECT * FROM order_stats where rank <= 1
""")
result = cursor.fetchall()
print(result)
# [('cheese', 2400, 1), ('ghee', 5500, 1), ('milk', 1400, 1)]
# -- one row per product, each showing THAT product's own best order


# --- DSA Micro-drill: rank_within_groups ---
# Goal: RANK() OVER (PARTITION BY group ORDER BY value DESC), reimplemented
# in plain Python -- group (like PARTITION BY), sort each group descending,
# then walk through assigning ranks with RANK()'s exact tie behavior: a
# tied value repeats the previous rank, but the underlying position
# counter still advances underneath it, so the next distinct value jumps
# forward by however many rows tied before it (the "gap").

def rank_within_groups(records):
    # Grouping (mirrors PARTITION BY)
    values = {}
    for record in records:
        values[record[0]] = values.get(record[0], []) + [record[1]]

    # Sorting each group descending (mirrors ORDER BY ... DESC)
    for key in values:
        values[key].sort(reverse=True)

    # Ranking, replicating RANK()'s gap-after-tie behavior
    new_values = {}
    for key, value_list in values.items():
        rank = 0
        current_value = float("-inf")
        new_values[key] = []
        for val in value_list:
            if current_value != val:
                rank += 1
                new_values[key].append((val, rank))
            else:
                new_values[key].append((val, rank))
                rank += 1
            current_value = val
    return new_values


print(rank_within_groups([("food", 200), ("food", 200), ("food", 50), ("transport", 80), ("transport", 40)]))
# {'food': [(200, 1), (200, 1), (50, 3)], 'transport': [(80, 1), (40, 2)]}

connection.close()
