"""
Topic 14, Day 1: Transactions & Atomicity

Covered: a transaction groups operations into one indivisible unit --
all succeed together (commit) or none take effect at all (rollback).
Critically: an uncommitted transaction is undone automatically on crash
recovery too, NOT only via an explicit rollback() call -- commit() is
the one and only moment changes become permanent; anything before that
point is "pencil, not pen."

ACID, precisely distinguished:
- Atomicity: all-or-nothing for a GROUP of operations -- if any one
  fails, every statement in that transaction is undone, not just the
  failing one.
- Consistency: the database refuses to let a transaction complete if it
  would violate its own rules (e.g. a UNIQUE constraint) -- defines
  WHAT'S valid, not what happens to the rest of the transaction.
- Isolation: concurrent transactions shouldn't see each other's
  half-finished work (Day 2).
- Durability: once commit() genuinely happens, that change survives
  even a crash immediately after.

Explicit BEGIN TRANSACTION is needed specifically when multiple
operations must succeed/fail TOGETHER as one atomic unit -- a single,
independent statement is already safely auto-committed on its own.

A bare `except Exception` is a deliberate, justified exception to
Topic 5's "never use a broad except" rule here: a rollback's entire job
is to catch ANYTHING that could go wrong mid-transaction, regardless of
cause, and undo it -- one of the few places broad exception handling is
the correct, deliberate choice rather than a lazy shortcut.
"""

import sqlite3

connection = sqlite3.connect("bank.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    balance INTEGER
)
""")

cursor.execute("SELECT COUNT(*) FROM accounts")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ("Maanvi", 1000))
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ("Vandana", 2500))
    connection.commit()


def transfer(cursor, connection, from_account, to_account, amount, simulate_crash=False):
    cursor.execute("BEGIN TRANSACTION")
    try:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_account))
        if simulate_crash:
            raise ValueError("simulated crash")
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_account))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Transaction failed, all changes undone: {e}")


# --- Homework 1: force a failure mid-transaction, prove rollback protects data ---
# Goal: don't just read about atomicity -- deliberately break the transaction
# between the two UPDATEs and confirm neither balance actually changed.

cursor.execute("SELECT id FROM accounts WHERE name = ?", ("Maanvi",))
maanvi_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM accounts WHERE name = ?", ("Vandana",))
vandana_id = cursor.fetchone()[0]

transfer(cursor, connection, maanvi_id, vandana_id, 200, simulate_crash=True)
cursor.execute("SELECT * FROM accounts")
print(cursor.fetchall())
# Both balances unchanged -- the debit genuinely ran, but was never committed,
# so it was rolled back along with everything else in the transaction.


# --- Homework 2: let the transfer succeed, verify the happy path too ---
# Goal: confirm the success path is ALSO correct -- money moved, none
# created or destroyed (balances still sum to the original total).

transfer(cursor, connection, maanvi_id, vandana_id, 200, simulate_crash=False)
cursor.execute("SELECT * FROM accounts")
print(cursor.fetchall())
# Both balances changed correctly, summing to the same total as before.

connection.commit()


# --- DSA Micro-drill: simulate_transaction ---
# Goal: all-or-nothing semantics in plain Python, no database involved --
# work on a COPY (working_copy) throughout, so a partial failure never
# leaks into the object the caller originally passed in. Named
# deliberately as "working_copy" rather than something similar-looking
# to the original parameter name, specifically to make it harder to
# accidentally mutate the real original by a typo later.

def simulate_transaction(operations, state):
    working_copy = dict(state)
    try:
        for operation in operations:
            working_copy = operation(working_copy)
        return working_copy
    except Exception as e:
        print(e)
        return state


def debit_savings(state):
    state["savings"] -= 500
    return state


def credit_checking(state):
    state["checking"] += 500
    return state


def broken_operation(state):
    raise ValueError("simulated failure")


starting_state = {"savings": 1000, "checking": 200}

print(simulate_transaction([debit_savings, credit_checking], starting_state))
# {'savings': 500, 'checking': 700} -- both succeeded

print(simulate_transaction([debit_savings, broken_operation], starting_state))
# simulated failure
# {'savings': 1000, 'checking': 200} -- UNCHANGED, even though debit_savings
# genuinely ran before the failure

print(starting_state)
# {'savings': 1000, 'checking': 200} -- confirmed: the ORIGINAL object was
# never touched on either call, since the copy is made before any
# operation runs, and every operation only ever receives the copy

connection.close()
