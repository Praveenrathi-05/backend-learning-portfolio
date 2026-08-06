# Personal Expense Tracker (CLI)

A command-line expense tracker with persistent storage — data survives
between runs, unlike the earlier Library Manager and Hostel Bill Manager
projects, which lost everything the moment the program closed.

## The Problem

Most budgeting tools assume a bank-linked, always-online user — which
excludes a huge number of people in a cash-heavy economy who just want a
simple, local way to see where their money is actually going day to day.

## What It Does

- Add expenses (amount, category, note)
- View all expenses, or totals broken down by category
- View total spending across everything
- Automatically loads saved data on startup, and saves on exit
- Fully validated numeric input (accepts decimals, not just whole numbers)
- Logs how long key actions take, via a custom decorator

## What I Practiced

- **File handling** — expenses persist across runs using comma-separated
  storage, following the same read/write pattern from Topic 5
- **Error handling** — `try/except FileNotFoundError` makes the very first
  run (no file yet) fail gracefully instead of crashing
- **Generators** — `category_totals()` yields `(category, total)` pairs
  one at a time instead of returning a fully-built list or dict
- **Decorators** — a custom `@log_action` decorator times any method it's
  applied to, without changing that method's own code, using
  `*args, **kwargs` so it works on methods with any signature
- **Composition** — an `ExpenseTracker` *has* `Expense` objects

## A Design Note on `category_totals()`

This method still has to scan every expense once before it can yield any
result — because a category's total isn't final until every expense has
been seen (expenses for the same category can appear anywhere in the
list). If the data were already sorted/grouped by category, totals could
be yielded incrementally as each category's block of entries ends. This
is a simplified version of a real optimization databases use for
`GROUP BY` queries on sorted data.

## How to Run

```bash
python expense_tracker.py
```

## Possible Future Improvements

- Handle multiple users, or multiple named tracking files
- Add date tracking and month-over-month comparisons
- Sort expenses by category before storage, to make `category_totals()`
  genuinely streaming instead of full-scan-then-yield
