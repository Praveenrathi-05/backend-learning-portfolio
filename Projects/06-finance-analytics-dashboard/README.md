# Personal Finance Analytics Dashboard (SQL Edition)

A command-line reporting tool built to prove that genuinely useful
financial analysis can be expressed entirely in SQL — no manual Python
loops for totals, averages, or rankings — directly applying subqueries,
CTEs, and window functions from Topic 12 to a real, two-table schema.

## The Problem

My original Expense Tracker (Weekly Project #3) could log expenses and
compute simple totals, but had no way to answer genuinely useful
questions: which category do I overspend in relative to my own average?
Which specific expense in a category stands out from the rest? These are
exactly the questions subqueries, CTEs, and window functions exist to
answer cleanly.

## What It Does

- Stores expenses across 5 categories with a proper foreign key
  (`expenses.category_id` → `categories.id`)
- `category_totals()` — total spend per category (`GROUP BY`)
- `above_average_categories()` — categories spending more than the
  average *of the per-category totals*, using a derived table (subquery
  inside `FROM`) for a genuine two-level aggregation
- `spending_with_category_average(name)` — every expense in one category
  shown alongside that category's own average, via a CTE broadcast-joined
  against the individual expense rows
- `ranked_expenses_per_category()` — every expense ranked against only
  its own category's other expenses, using `RANK() OVER (PARTITION BY ...)`
- `top_expense_per_category()` — the classic top-N-per-group pattern: a
  CTE computes the rank, the outer query filters to the single highest
  expense per category
- A `@timer` decorator applied to the heaviest report, reporting real
  execution time
- Fully validated menu loop, including a category-name lookup that
  re-prompts until a real category is entered

## What I Practiced

- Foreign key design and `INNER JOIN` across a genuine schema
- Scalar subqueries and derived tables (subqueries inside `FROM`) for
  multi-level aggregation
- CTEs, including a single-row CTE broadcast-joined against a full table
- Window functions (`PARTITION BY`, `RANK()`) for per-group ranking
  without collapsing rows
- The top-N-per-group pattern: filtering a window function's result by
  wrapping it in a CTE, since `WHERE` can't see it directly
- A real, self-found bug: `connection.close()` was originally placed
  *before* `menu()` was ever called, meaning every report function would
  crash on "Cannot operate on a closed database" — fixed by moving
  `close()` to run only after `menu()` fully returns, so the connection's
  lifetime correctly wraps around everything that needs it

## How to Run

```bash
python finance_dashboard.py
```

## Possible Future Improvements

- Real `DATE` handling instead of plain text dates, for genuine
  month-over-month comparisons
- Indexing on `category_id` once the dataset is large enough to matter
  (a direct preview of Topic 13)
- A `LAG()`/`LEAD()`-based report comparing consecutive expenses within
  a category over time

## Open Scalability Question

Every query here scans the entire table on every run — instant at 25
rows, but several of these (especially the correlated/derived-table
subqueries) would become genuinely slow at millions of rows. What tool
exists specifically to make searching/filtering large tables fast
without scanning every row? Not yet answered — the direct subject of
Topic 13: Database Design & Indexing.
