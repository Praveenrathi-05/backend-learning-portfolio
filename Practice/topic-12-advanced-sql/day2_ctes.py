"""
Topic 12, Day 2: Common Table Expressions (CTEs)

Covered: WITH name AS (...) -- naming a subquery so it can be referenced
like a real table for the rest of one query. CTEs are primarily a
readability/reuse tool, NOT a reliable performance improvement -- most
engines optimize a CTE into essentially the same execution plan as an
equivalent nested subquery. Multiple CTEs can be chained, with later ones
referencing earlier ones by name, avoiding rewriting the same logic twice.
A CTE's lifetime is scoped strictly to the single query it's attached to
(exactly like a local variable inside a function) -- it cannot be queried
again in a separate, later cursor.execute() call.

Recurring lesson worth internalizing (hit twice this topic): before
joining two tables inside a subquery/CTE, check whether the column you
actually need already lives on just ONE of them -- a join is only needed
when you genuinely require columns from BOTH sides at once.
"""

import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

# --- Homework 1: yesterday's nested-subquery problem, rewritten as 2 CTEs ---
# Goal: direct, hands-on proof that CTEs solve yesterday's exact pain point --
# products priced below the average price of ONLY the ordered products.
# (Simplified from an earlier draft that redundantly joined store+orders
# just to pull product_id, which already lives directly on orders alone.)

cursor.execute("""
    WITH ordered_products AS (
        SELECT product_id FROM orders
    ), ordered_products_prices AS (
        SELECT name, price FROM store WHERE id IN (SELECT product_id FROM ordered_products)
    )
    SELECT name, price FROM ordered_products_prices
    WHERE price < (SELECT AVG(price) FROM ordered_products_prices)
""")
result = cursor.fetchall()
print(result)
# [('cheese', 120), ('milk', 35)]


# --- Homework 2: best-seller by total quantity, using one CTE ---
# Goal: a realistic "what's our top product" report -- CTE computes
# per-product totals once, final SELECT just sorts and takes the top row.

cursor.execute("""
    WITH products AS (
        SELECT name, SUM(quantity) as total_quantity FROM store
        INNER JOIN orders ON store.id = orders.product_id GROUP BY name
    )
    SELECT name, total_quantity FROM products ORDER BY total_quantity DESC LIMIT 1
""")
result = cursor.fetchall()
print(result)
# [('milk', 72)]


# --- DSA Micro-drill: two_stage_filter ---
# Goal: mirror the shape of chained CTEs in plain Python -- stage two's
# INPUT is stage one's OUTPUT, not the original records, exactly like
# ordered_products_prices building on top of ordered_products above.

def is_even(n):
    return n % 2 == 0


def above_ten(n):
    return n > 10


def two_stage_filter(records, first_stage, second_stage):
    stage_one_results = [record for record in records if first_stage(record)]
    stage_two_results = [r for r in stage_one_results if second_stage(r)]
    return stage_two_results


records = [10, 25, 3, 47, 16, 8, 33]
print(two_stage_filter(records, is_even, above_ten))
# Stage 1 (is_even): keeps [10, 16, 8]
# Stage 2 (above_ten) applied to THAT result: keeps [16]
# [16]

connection.close()
