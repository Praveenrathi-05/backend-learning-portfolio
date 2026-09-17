"""
Topic 14, Day 3: Locking & Deadlocks

Covered: shared (read) locks can coexist across many transactions
simultaneously; exclusive (write) locks are held by exactly one
transaction at a time and block others. A deadlock is a CIRCULAR wait
-- transaction A holds what B wants, B holds what A wants, and neither
releases anything until it commits/rolls back, which neither can do
while blocked. This cannot resolve itself by waiting longer, unlike a
normal (non-circular) lock wait.

Real databases run deadlock detection and forcibly roll back one
"victim" transaction to break the cycle -- this is NOT a sign of a bug
in that transaction's own code; it's a normal, expected outcome of
concurrent systems. Production transactional code should treat lock
conflicts/deadlocks as expected, recoverable failures and retry, the
same way ConnectionError/Timeout/IntegrityError were treated as
expected failure modes earlier in this curriculum -- never as
infinite retries, always bounded.

Consistent lock ordering (always acquire locks in the same order,
e.g. ascending id, regardless of logical transfer direction) prevents
an entire CLASS of deadlocks structurally -- it removes the possibility
of circular waiting by design, rather than just detecting and
recovering from it after the fact.
"""

import sqlite3
import time

connection = sqlite3.connect("bank.db")
cursor = connection.cursor()


# --- Homework 1: transfer with bounded retry logic ---
# Goal: production-shaped transactional code -- treats a lock conflict
# as an expected, recoverable failure (bounded retries + brief pause),
# not a fatal error. Confirmed: succeeds on the first attempt under
# normal (non-contended) conditions.

def transfer(cursor, connection, from_account, to_account, amount, max_tries=3):
    for attempt in range(max_tries):
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_account))
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_account))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"Attempt {attempt + 1} failed ({e}), retrying...")
            time.sleep(0.1)
    print("Transfer failed after all retries.")
    return False


transfer(cursor, connection, 2, 1, 500)
connection.commit()
connection.close()


# --- Homework 2: deadlock risk assessment, Weekly Project #6 ---
# Goal: identify whether a real project has any genuine write-contention
# risk, not just assume "no writes = no risk" or "has writes = deadlock
# risk" without tracing precisely.
#
# The reporting functions (category_totals, above_average_categories,
# spending_with_category_average, ranked_expenses_per_category,
# top_expense_per_category) are entirely read-only (SELECT only) --
# shared locks only, genuinely deadlock-safe, can run concurrently
# without contention.
#
# BUT the seed-data block at the top of the file (INSERT INTO
# categories / INSERT INTO expenses) IS a write path. If two processes
# ran this script concurrently against the same fresh store.db, they
# could hit real write-lock contention -- and with categories.name
# UNIQUE (Topic 13), a genuine IntegrityError/lock conflict is possible.
# This is lock CONTENTION, not necessarily a true CIRCULAR deadlock
# (a straightforward sequential insert script doesn't naturally lock
# two different rows in opposite orders the way the bill-transfer
# scenario does) -- but it's a real risk worth being aware of, not "no
# risk at all" just because the reporting side is read-only.


# --- DSA Micro-drill: has_deadlock (cycle detection via DFS) ---
# Goal: detect a deadlock as a CYCLE in a "who's waiting on whom" graph.
# First version only checked wait_graph[node][0] -- silently ignored a
# transaction waiting on MULTIPLE others, missing real cycles (e.g.
# {"A": ["B", "C"], "B": [], "C": ["A"]}, where A->C->A is a genuine
# cycle never reached by following only the first neighbor).
#
# Fixed with proper depth-first search: two SEPARATE sets doing two
# different jobs --
#   current_path: nodes on the ACTIVE chain being explored right now.
#     Re-encountering one of these = a genuine cycle.
#   visited: nodes ALREADY fully explored and confirmed cycle-free.
#     Safe to skip re-exploring -- because full exploration already
#     happened once, a later re-encounter can't be hiding an undetected
#     cycle.

def has_deadlock(wait_graph):
    visited = set()
    current_path = set()

    def dfs(node):
        if node in current_path:
            return True
        if node in visited:
            return False

        current_path.add(node)
        for neighbor in wait_graph[node]:
            if dfs(neighbor):
                return True
        current_path.remove(node)
        visited.add(node)
        return False

    for node in wait_graph:
        if dfs(node):
            return True
    return False


print(has_deadlock({"A": ["B"], "B": ["A"]}))
# True -- direct cycle

print(has_deadlock({"A": ["B"], "B": ["C"], "C": []}))
# False -- chain resolves, no cycle

print(has_deadlock({"A": ["B"], "B": ["C"], "C": ["A"]}))
# True -- longer cycle

print(has_deadlock({"A": ["B", "C"], "B": [], "C": ["A"]}))
# True -- the bug the first ([0]-only) version missed: A waits on BOTH
# B and C; A->C->A is a real cycle only found by checking every neighbor

print(has_deadlock({"A": ["B"], "B": ["C"], "C": [], "D": ["B"]}))
# False -- B is reachable from two different starting points (A and D)
# but genuinely has no cycle; confirms the `visited` shortcut doesn't
# cause a false positive or false negative
