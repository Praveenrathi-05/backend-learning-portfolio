"""
Topic 14, Day 2: Isolation Levels

Covered: the three classic concurrency problems, precisely distinguished:
- Dirty read: seeing another transaction's UNCOMMITTED data (most
  dangerous -- can escape the database's boundary into the real world
  in a way rollback can never undo, e.g. a printed bank statement based
  on data that was later rolled back).
- Non-repeatable read: the SAME transaction reads the SAME row twice,
  gets two different (but both genuinely committed) values, because
  another transaction committed a change in between.
- Phantom read: a NEW row appears matching an earlier query's filter,
  mid-transaction (the set of matching rows changes, not a single row's
  value).

Four standard isolation levels, each strictly stricter than the last,
each preventing everything the previous level prevented plus one more:
READ UNCOMMITTED (prevents nothing) -> READ COMMITTED (prevents dirty
reads only) -> REPEATABLE READ (+ non-repeatable reads) -> SERIALIZABLE
(+ phantom reads too). Stricter = more correctness guarantees, but more
waiting/failures under concurrent load -- the real engineering judgment
is choosing the WEAKEST level that still prevents the anomalies that
would actually cause real harm to a specific application.

SQLite's real default behaves close to SERIALIZABLE via its own file
locking (not the configurable 4-level menu PostgreSQL offers) -- a
write from one connection can be flatly rejected ("database is locked")
if another connection has an open transaction, rather than allowing an
inconsistency to occur. This was directly observed in Homework 1 below.

Also introduced: the "lost update" / race condition problem (distinct
from the three classic reads) -- two transactions both read the same
stale value, both compute an update from it, and the second write
silently overwrites the effect of the first (e.g. two customers both
seeing "1 in stock" and both completing a purchase). SERIALIZABLE or a
dedicated locking mechanism (SELECT ... FOR UPDATE, optimistic
concurrency via version numbers) is the real fix -- a preview of
deeper concurrency-control topics ahead.
"""

import sqlite3

# --- Homework 1: attempt to demonstrate a non-repeatable read ---
# Goal: use two SEPARATE connections to the same database file to
# observe real concurrent behavior directly, rather than just reading
# about it.
#
# ACTUAL RESULT (worth keeping as the real lesson, not a "failed" test):
#   con_a begins a transaction and reads Maanvi's balance.
#   con_b begins a transaction, attempts to UPDATE the same row, then
#   tries to COMMIT while con_a's transaction is still open.
#   con_b's commit raised: sqlite3.OperationalError: database is locked
#
# This demonstrates SQLite's strong, near-SERIALIZABLE default locking
# in action: rather than allowing the non-repeatable read to occur,
# SQLite refused B's write outright while A's transaction was open --
# a live, concrete example of the "stricter isolation = more failures
# under contention" trade-off from this lesson, rather than the "clean"
# non-repeatable-read demo originally intended.

con_a = sqlite3.connect("bank.db")
con_b = sqlite3.connect("bank.db")

cursor_a = con_a.cursor()
cursor_b = con_b.cursor()

cursor_a.execute("BEGIN")
cursor_a.execute("SELECT * FROM accounts WHERE name = ?", ("Maanvi",))
print(cursor_a.fetchone())

cursor_b.execute("BEGIN")
cursor_b.execute("UPDATE accounts SET balance = balance + 200 WHERE name = ?", ("Maanvi",))
try:
    cursor_b.execute("COMMIT")
except sqlite3.OperationalError as e:
    print(f"B's commit failed: {e}")
    cursor_b.execute("ROLLBACK")

cursor_a.execute("SELECT * FROM accounts WHERE name = ?", ("Maanvi",))
print(cursor_a.fetchone())
cursor_a.execute("COMMIT")

con_a.close()
con_b.close()


# --- Homework 2: isolation level judgment across 3 real scenarios ---
# Goal: apply "name the anomaly, assess real harm, pick the weakest
# level that still protects against what actually matters" -- not a
# blanket "always strict" or "always loose" rule.
#
# (a) Stock-trading system (buy/sell orders):
#     A dirty read (acting on an uncommitted price) or a non-repeatable
#     read (balance check giving two different answers mid-trade) could
#     both cause real, irreversible financial harm.
#     -> SERIALIZABLE. The cost of some transactions waiting/retrying
#        is clearly justified against the cost of an incorrect trade.
#
# (b) "Likes" counter on a social media post:
#     None of dirty/non-repeatable/phantom reads cause any real harm to
#     a rough, cosmetic, occasionally-read counter.
#     -> READ COMMITTED (or weaker). Maximize concurrency; correctness
#        requirements here are extremely loose.
#
# (c) Inventory "is this item in stock" check before a purchase:
#     Not quite a classic dirty/non-repeatable/phantom read -- this is
#     a LOST UPDATE / race condition: two transactions both read the
#     same stale count, both proceed, second write silently overwrites
#     the effect of the first (selling 2 units when only 1 existed).
#     -> SERIALIZABLE, or a dedicated locking mechanism (SELECT ... FOR
#        UPDATE / optimistic concurrency with a version check). Real,
#        irreversible business harm (overselling) justifies the cost.


# --- DSA Micro-drill: detect_non_repeatable_read ---
# Goal: group reads by (transaction_id, row_id) -- mirrors Topic 13's
# find_redundant_facts grouping pattern -- and flag True the moment any
# single transaction's repeated read of the same row disagrees with a
# value it saw earlier for that same row.

def detect_non_repeatable_read(read_log):
    values = {}
    for value in read_log:
        key = (value[0], value[1])
        if key in values:
            if values[key] == value[2]:
                return False
        else:
            values[key] = value[2]
    return True


print(detect_non_repeatable_read([("A", 1, 1000), ("B", 1, 1000), ("A", 1, 900)]))
# True -- "A" read row 1 as 1000, then later as 900 (a real disagreement)

print(detect_non_repeatable_read([("A", 1, 1000), ("B", 2, 500), ("A", 1, 1000)]))
# False -- "A" read row 1 twice, but got the SAME value both times
