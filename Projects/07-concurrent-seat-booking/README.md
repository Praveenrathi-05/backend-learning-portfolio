# Concurrent Seat Booking System

A command-line seat-booking system built specifically to expose, prove,
and then fix a real race condition — the exact "booking system with
concurrency" project my original roadmap reserved for once I had
transactions, isolation levels, and locking (Topic 14) properly under
my belt.

## The Problem

The hardest part of any real booking system (tickets, seats, slots)
isn't the UI — it's guaranteeing two customers can never be sold the
same seat, even if they click "book" within the same millisecond. This
project deliberately builds the naive, broken version first, proves the
bug is real using genuine OS-level thread concurrency (not just a
simulated interleaving), and then builds and verifies the fix.

## What It Does

- `book_seat_unsafe()` — deliberately naive: reads `is_booked`, sleeps
  2 seconds (widening the race window on purpose so the bug reproduces
  reliably), then writes. **No transaction, no protection.**
- `simulate_concurrent_booking()` — uses real `threading.Thread`s, each
  with its own database connection, to force two customers to hit the
  same seat at nearly the same instant.
- **Verified directly, not just claimed**: run repeatedly, both threads
  print `"Seat Booked!"` and the database ends up with 2 rows for the
  same seat — a real, reproducible double-booking.
- `book_seat_safe()` — the fix: check-and-book fused into one atomic
  transaction, with bounded retries (3 attempts, brief pause) on lock
  conflicts.
- **Verified directly**: across 5 real concurrent trials, exactly one
  customer books successfully, the other correctly sees "Seat already
  booked!", and exactly 1 row lands in the database — every time.
- `book_seat_with_lock_ordering()` — multi-seat booking, always
  processing requested seats in ascending id order regardless of the
  order the customer specified them, directly preventing deadlocks
  between two customers booking overlapping seat groups.
- **Verified directly**: two customers requesting overlapping,
  deliberately oppositely-ordered seat sets (`[1,2,3]` vs `[4,3,2]`,
  sharing seat 2) — across 5 trials, zero double bookings, zero
  deadlocks or hangs, every seat's booking count exactly 1.
- Full menu loop with input validation for booking, viewing
  availability, running the concurrency demo, and viewing history.

## What I Practiced

- Real OS-level concurrency via `threading`, not just simulated
  interleaving — a direct, hands-on preview of Topics 67/68
- The lost-update race condition, reproduced and proven on my own code
  before fixing it, not just read about
- Transactions, `BEGIN`/`COMMIT`/`ROLLBACK`, and bounded retry logic
  under real lock contention (Topic 14, Days 1 & 3)
- Consistent lock ordering to structurally prevent deadlocks in
  multi-resource transactions (Topic 14, Day 3)
- A real, self-found bug: an earlier version of the multi-seat function
  checked every seat's availability in one pass, then updated all of
  them in a second, separate pass — reopening a smaller version of the
  original race condition for multi-seat bookings specifically. Fixed
  by fusing the check and the update into a single step per seat,
  inside one continuous transaction.
- The discipline of proving a fix works under the exact real conditions
  it's meant to survive, rather than trusting that it "looks correct"

## How to Run

```bash
python booking_system.py
```

## Possible Future Improvements

- A proper waiting-list/queue for a seat that's released after being
  held but not confirmed
- Configurable lock timeout and exponential backoff on retries
- A stress test simulating many more than 2 concurrent customers

## Open Scalability Question

If this system needed to handle 10,000 people trying to book the same
popular seat within one second (a concert on-sale moment), would
retry-loop-based locking, as built here, actually hold up — or would
9,999 failed retries create a new problem of its own (thundering herd)?
Not yet answered — a direct preview of message queues and rate limiting
(Topics 78, 80).
