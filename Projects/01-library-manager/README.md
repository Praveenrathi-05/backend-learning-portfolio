# Library Manager (CLI)

A command-line application for managing a small book library — 
tracking availability, borrowing, returns, and usage stats.

## The Problem

Small libraries, school reading rooms, and personal book collections are 
often still tracked on paper or scattered notes, with no easy way to see 
what's currently available or how often a book has been borrowed.

## What It Does

- Add new books to the library
- Borrow and return books by title (case-insensitive matching)
- View all available books, or the full catalog with status
- Tracks how many times each book has been borrowed
- Fully validated user input — no crashes on invalid menu choices or 
  malformed input

## What I Practiced

- Class design (`Book`, `Library`) — bundling data with the operations 
  that safely act on it
- Defensive programming — guarding against "book not found," double 
  borrowing, and non-numeric menu input
- Menu-driven control flow using `while True` + `break`

## How to Run

```bash
python library.py
```

## Possible Future Improvements

- Persist books to a file so data survives between runs
- Add due dates and overdue tracking