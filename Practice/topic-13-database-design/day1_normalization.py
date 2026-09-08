"""
Topic 13, Day 1: Normalization (1NF / 2NF / 3NF)

Covered: normalization eliminates redundancy and prevents three named
anomalies -- update (a fact stored in many places, all must be kept in
sync or they silently contradict each other), insertion (can't record a
true fact because it's trapped inside a table meant for something else),
and deletion (deleting one record accidentally erases an unrelated fact
as a side effect).

1NF: every cell holds exactly one atomic value -- no lists/repeating
groups crammed into a field (the formal version of Topic 5's
comma-separated-file lesson, and exactly why Topic 11 taught splitting
related data into separate tables via foreign keys).

2NF: every non-key column must depend on the ENTIRE composite key, not
just part of it (a composite key = a primary key made of 2+ columns
together, needed when no single column uniquely identifies a row).

3NF: every non-key column must depend DIRECTLY on the primary key, not
transitively through another non-key column already sitting in the row
(e.g. product_price depending on product_name, not on order_id itself).

Precise test for a genuine 3NF violation: does this value belong to
THIS row, or to some other, shared concept this row merely references?
A calculated/historical value (like a bill's amount, or an expense's
amount) is fine on its own row; a SHARED, reusable fact (like a rate or
a price) copied directly onto many rows instead of referenced from one
lookup table is the actual violation.

Normalization is a genuine trade-off, not an absolute rule: more
normalized tables mean more joins and more complexity; some systems
deliberately denormalize for read performance, accepting update-anomaly
risk in exchange.
"""

import sqlite3

connection = sqlite3.connect("gym.db")
cursor = connection.cursor()

# --- Homework 1 (design, documented here) ---
# Original bad table:
#   gym_memberships(membership_id, member_name, member_email,
#                    trainer_name, trainer_specialty, plan_name,
#                    plan_price, start_date)
#
# Violations found:
#   - trainer_specialty depends on trainer_name, not membership_id
#     -> UPDATE anomaly risk (correcting a trainer's specialty means
#        updating every membership row that mentions them)
#   - plan_price depends on plan_name, not membership_id
#     -> UPDATE anomaly risk (a price change needs updating on every
#        membership using that plan)
#
# Normalized to 3NF:
#   trainer(id PK, name, specialty)
#   plan(id PK, name, price)
#   member(id PK, trainer_id FK -> trainer.id, plan_id FK -> plan.id,
#          name, email, start_date)


# --- Homework 2: build the normalized schema, prove a JOIN reassembles it ---
# Goal: show the normalized design still lets you reconstruct the full,
# human-readable "flat view" the original bad table had, but with every
# fact (a trainer's specialty, a plan's price) now living in exactly one
# place.

cursor.execute("""
CREATE TABLE IF NOT EXISTS trainer (
    id INTEGER PRIMARY KEY,
    name TEXT,
    specialty TEXT
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS plan (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY,
    trainer_id INTEGER,
    plan_id INTEGER,
    name TEXT,
    email TEXT,
    start_date TEXT
);
""")

cursor.execute("INSERT INTO trainer (name, specialty) VALUES (?, ?)", ("Amit", "Yoga"))
trainer_amit_id = cursor.lastrowid

cursor.execute("INSERT INTO trainer (name, specialty) VALUES (?, ?)", ("Riya", "Strength"))
trainer_riya_id = cursor.lastrowid

cursor.execute("INSERT INTO plan (name, price) VALUES (?, ?)", ("Beginner", 12000))
beginner_plan_id = cursor.lastrowid

cursor.execute("INSERT INTO plan (name, price) VALUES (?, ?)", ("Premium", 18000))
premium_plan_id = cursor.lastrowid

cursor.execute(
    "INSERT INTO member (trainer_id, plan_id, name, email, start_date) VALUES (?, ?, ?, ?, ?)",
    (trainer_amit_id, beginner_plan_id, "Sonali", "sonali@gmail.com", "07-08-2026")
)
cursor.execute(
    "INSERT INTO member (trainer_id, plan_id, name, email, start_date) VALUES (?, ?, ?, ?, ?)",
    (trainer_riya_id, premium_plan_id, "Sanyam", "sanyam@gmail.com", "04-03-2026")
)

cursor.execute("""
    SELECT member.name, trainer.name, plan.name, plan.price
    FROM member
    INNER JOIN trainer ON member.trainer_id = trainer.id
    INNER JOIN plan ON member.plan_id = plan.id;
""")
print(cursor.fetchall())
# [('Sonali', 'Amit', 'Beginner', 12000), ('Sanyam', 'Riya', 'Premium', 18000)]

connection.commit()


# --- DSA Micro-drill: find_redundant_facts ---
# Goal: a hands-on tool to DETECT whether data has already suffered the
# exact redundancy problem this lesson describes -- group by trainer
# (mirrors Topic 11's group_by_key), then within each trainer's group,
# check whether every record agrees using set() (a list has exactly one
# distinct value iff converting it to a set leaves length 1).
#
# Note: this version reports per-trainer detail ({"Amit": {"trainer_
# specialty": False}, "Kabir": {...True}}) rather than a single flat
# per-key answer -- arguably more useful, since it shows WHERE the
# inconsistency is, not just THAT one exists somewhere in the table.

def find_redundant_facts(records):
    data = {}
    for record in records:
        name = record['trainer_name']
        if name not in data:
            data[name] = {}
        for key, value in record.items():
            if key == 'trainer_name':
                continue
            if key in data[name]:
                data[name][key].append(value)
            else:
                data[name][key] = [value]
    result = {}
    for pair in data:
        result[pair] = {}
        for item in data[pair]:
            result[pair][item] = len(set(data[pair][item])) == 1
    return result


records = [
    {"trainer_name": "Amit", "trainer_specialty": "Yoga"},
    {"trainer_name": "Amit", "trainer_specialty": "Cardio"},   # inconsistent!
    {"trainer_name": "Kabir", "trainer_specialty": "Boxing"},
    {"trainer_name": "Kabir", "trainer_specialty": "Boxing"},
]
print(find_redundant_facts(records))
# {'Amit': {'trainer_specialty': False}, 'Kabir': {'trainer_specialty': True}}

connection.close()
