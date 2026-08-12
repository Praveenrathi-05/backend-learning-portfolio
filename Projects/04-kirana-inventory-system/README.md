# Kirana Store Inventory & Low-Stock Alert System (CLI)

A command-line inventory manager for small shops — tracking stock levels,
flagging low-stock items automatically, and distinguishing perishable from
regular goods.

## The Problem

Small shopkeepers across India — kirana stores, medical stores, stationery
shops — often track inventory from memory or a paper register. This leads
to real, recurring losses: stockouts on fast-moving items, overstocking of
slow-moving items, and perishables quietly expiring unnoticed. Most digital
inventory tools assume constant connectivity and tech comfort a lot of
small shop owners don't have — a simple, local, offline-first tool solves
a genuine version of this problem.

## What It Does

- Add regular or perishable products, each with its own reorder threshold
- Restock and sell products by name (case-insensitive), with quantity
  validation — stock can never go negative
- Automatically flag low-stock items via a **generator**, without building
  a full list upfront
- Track total inventory value across the whole shop
- Persist all data to a file — loads automatically on startup, with a
  graceful first-run experience if no data exists yet
- Fully validated menu input — no crashes on bad numeric input, no silent
  failures on a product that doesn't exist

## What I Practiced

- **Inheritance & polymorphism** — `PerishableProduct` extends `Product`
  via `super().__init__()` and `super().__str__()`; both classes implement
  their own `to_line()` for file persistence, so `Shop.save_to_file()`
  never needs to check which type of product it's holding
- **Composition** — `Shop` holds a list of `Product` objects
- **Magic methods** — `__str__` for clean display, `__lt__` for sorting by
  stock level
- **A decorator** (`@log_action`) — logs every restock/sell action without
  that logging logic living inside the methods themselves
- **A generator** (`low_stock_items`) — yields low-stock products lazily,
  one at a time
- **Defensive programming** — every method is correct on its own regardless
  of caller (case-insensitive matching lives inside `Shop`, not the menu
  layer), file loading handles a missing file gracefully via
  `try/except FileNotFoundError`
- **Git branching** — the restock feature was built on its own branch
  (`feature/restock`) and merged back into `main` once working

## How to Run

```bash
python shop.py
```

## Possible Future Improvements

- Real date comparisons for expiry (currently stored as plain text)
- A `total_sold` counter per product for lifetime sales tracking
- Move from a flat file to a proper database to handle concurrent access
  safely (see the open question below)

## Open Question — What Breaks at Scale

Right now, all data lives in one local text file. If two shop assistants
updated stock from two different devices around the same time, both
reading and writing the same file — what could go wrong? This is a direct
preview of database transactions and concurrency, not yet solved here on
purpose.
