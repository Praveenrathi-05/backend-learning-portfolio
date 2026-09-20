import sqlite3
from datetime import datetime
from pathlib import Path
import time
import threading

file_name = Path(__file__).resolve().parent / "booking.db"

connection = sqlite3.connect(file_name)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS seats(
                id INTEGER PRIMARY KEY,
                seat_number TEXT UNIQUE,
                is_booked INTEGER DEFAULT 0
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bookings(
                id INTEGER PRIMARY KEY,
                seat_id INTEGER,
                customer_name TEXT,
                booked_at TEXT
)
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_bookings_seat_id ON bookings(seat_id)")

seats = [
    ("A1",), ("A2",), ("A3",), ("A4",), ("A5",),
    ("B1",), ("B2",), ("B3",), ("B4",), ("B5",)
]

cursor.execute("SELECT 1 FROM seats LIMIT 1")
row = cursor.fetchone()

if row is None:
    cursor.executemany(
        "INSERT INTO seats (seat_number) VALUES (?)",
        seats
    )

connection.commit()


def book_seat_unsafe(cursor, connection, seat_id, customer_name):
    """
    Deliberately naive booking, built to demonstrate the lost-update
    race condition, not to be used for real bookings. time.sleep(2)
    between the read and the write deliberately widens the race window
    so the bug reproduces reliably rather than depending on luck.

    Verified via real threading.Thread concurrency (not just two
    sequential connections): BOTH threads print "Seat Booked!" and the
    bookings table ends up with 2 rows for the same seat, every time.
    """
    cursor.execute("SELECT * FROM seats where id = ?", (seat_id,))
    seat = cursor.fetchone()
    if seat:
        is_seat_booked = seat[2]
        if is_seat_booked == 0:
            time.sleep(2)
            cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = ?", (seat_id,))
            cursor.execute(
                "INSERT INTO bookings (seat_id, customer_name, booked_at) VALUES (?,?,?)",
                (seat_id, customer_name, datetime.now().isoformat())
            )
            connection.commit()
            return "Seat Booked!"
        else:
            return "Seat already booked!"
    else:
        return "No Seat Like this Exists!"


def simulate_concurrent_booking(seat_id):
    """
    Uses real OS-level threads (each with its own sqlite3 connection,
    since connections aren't safely shared across threads by default)
    to force two customers to attempt booking the same seat at nearly
    the exact same instant.
    """
    def attempt_booking(customer_name):
        conn = sqlite3.connect(file_name)
        new_cursor = conn.cursor()
        print(book_seat_unsafe(new_cursor, conn, seat_id, customer_name))
        conn.close()

    thread_a = threading.Thread(target=attempt_booking, args=("Praveen",))
    thread_b = threading.Thread(target=attempt_booking, args=("Maanvi",))
    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()


def book_seat_safe(cursor, connection, seat_id, customer_name, max_retries=3):
    """
    The real fix: check-and-book fused into a single atomic transaction,
    with bounded retries on lock conflicts (Topic 14 Day 3's pattern).

    Verified under real thread concurrency across 5 trials: exactly one
    thread books successfully, the other correctly reports "Seat
    already booked!", and exactly 1 row lands in bookings -- never 2,
    never 0. The retry loop's real job isn't just "survive an error" --
    it's ensuring the LOSING thread gets to re-read the now-updated
    is_booked value and report the genuinely correct outcome, rather
    than crashing or reporting stale information.
    """
    for attempt in range(max_retries):
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute("SELECT * FROM seats where id = ?", (seat_id,))
            seat = cursor.fetchone()
            if seat:
                is_seat_booked = seat[2]
                if is_seat_booked == 0:
                    cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = ?", (seat_id,))
                    cursor.execute(
                        "INSERT INTO bookings (seat_id, customer_name, booked_at) VALUES (?,?,?)",
                        (seat_id, customer_name, datetime.now().isoformat())
                    )
                    connection.commit()
                    return "Seat Booked!"
                else:
                    connection.rollback()
                    return "Seat already booked!"
            else:
                connection.rollback()
                return "No Seat Like this Exists!"
        except sqlite3.OperationalError as e:
            connection.rollback()
            if "locked" in str(e):
                print(f"Attempt {attempt + 1} failed ({e}), retrying...")
                time.sleep(0.1)
            else:
                return str(e)
    return "Booking failed after all retries."


def book_seat_with_lock_ordering(cursor, connection, seat_ids, customer_name):
    """
    Multi-seat booking, always processing seats in ascending id order
    regardless of the order the customer specified them in -- Topic 14
    Day 3's consistent lock ordering, preventing an entire class of
    deadlocks structurally.

    Check-and-update are fused into ONE pass per seat (not a separate
    "check all, then update all" pass) -- an earlier version had a real
    gap here: checking every seat first and only updating afterward
    reopened a smaller version of the exact race condition
    book_seat_unsafe had, just for a multi-seat booking instead of a
    single seat. Fixed by checking and immediately booking each seat
    before moving to the next, all within one continuous transaction.

    Verified under real overlapping concurrent bookings (customer A
    requesting [1,2,3], customer B requesting [4,3,2] -- deliberately
    opposite orderings, sharing seat 2) across 5 trials: zero double
    bookings, zero deadlocks/hangs, every seat's booking count exactly
    1. The internal sorted() call is what makes this safe regardless
    of the order either customer specified their seats in.
    """
    if len(seat_ids) == 0:
        return "No seats selected"
    seat_ids = set(seat_ids)
    sorted_seat_ids = sorted(seat_ids)
    for attempt in range(3):
        try:
            cursor.execute("BEGIN TRANSACTION")
            for seat_id in sorted_seat_ids:
                cursor.execute("SELECT * FROM seats where id = ?", (seat_id,))
                seat = cursor.fetchone()
                if seat:
                    is_seat_booked = seat[2]
                    if is_seat_booked == 1:
                        connection.rollback()
                        return "Seat already booked!"
                    else:
                        cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = ?", (seat_id,))
                        cursor.execute(
                            "INSERT INTO bookings (seat_id, customer_name, booked_at) VALUES (?,?,?)",
                            (seat_id, customer_name, datetime.now().isoformat())
                        )
                else:
                    connection.rollback()
                    return "Seat doesn't exist"
            connection.commit()
            return "Booked all seats"
        except sqlite3.OperationalError as e:
            connection.rollback()
            if "locked" in str(e):
                print(f"Attempt {attempt + 1} failed ({e}), retrying...")
                time.sleep(0.1)
            else:
                return str(e)
        except Exception as e:
            connection.rollback()
            return str(e)
    return "Booking failed."


def view_seats(cursor):
    cursor.execute("SELECT * FROM seats")
    seats = cursor.fetchall()
    if len(seats) == 0:
        print("Currently No Seats Added")
        return
    for seat in seats:
        if seat[2] == 1:
            print(f"{seat[1]} - Booked")
        else:
            print(f"{seat[1]} - Available")


def view_booking_history(cursor):
    cursor.execute("""SELECT b.customer_name, s.seat_number, b.booked_at FROM bookings b
                    INNER JOIN seats s ON s.id = b.seat_id
        """)
    history = cursor.fetchall()
    if len(history) == 0:
        print("No booking history")
        return
    for entry in history:
        print(f"{entry[0]} booked {entry[1]} at {entry[2]}")


def main():
    while True:
        print("1. Book a seat\n2. View all seats\n3. Run concurrent booking demo\n4. View booking history\n5. Exit")
        task = input("Enter task number: ")
        try:
            task = int(task)
        except ValueError:
            print("Enter a number")
        else:
            if task == 1:
                while True:
                    seat_id = input("Enter Seat Id: ")
                    try:
                        seat_id = int(seat_id)
                        if seat_id > 0:
                            break
                    except ValueError:
                        continue
                while True:
                    name = input("Enter Customer Name: ").strip()
                    if name != "":
                        break
                print(book_seat_safe(cursor, connection, seat_id, name))
            elif task == 2:
                view_seats(cursor)
            elif task == 3:
                while True:
                    seat_id = input("Enter Seat Id: ")
                    try:
                        seat_id = int(seat_id)
                        if seat_id > 0:
                            break
                    except ValueError:
                        continue
                simulate_concurrent_booking(seat_id)
            elif task == 4:
                view_booking_history(cursor)
            elif task == 5:
                connection.close()
                break
            else:
                print("Enter a valid task number.")


if __name__ == "__main__":
    main()
