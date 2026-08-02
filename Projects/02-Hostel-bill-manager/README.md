# Hostel/Society Bill Manager (CLI)

A command-line application for tracking residents and their bills across
multiple categories — electricity, water, and internet — in a hostel or
housing society.

## The Problem

Across Indian housing societies, hostels, and PGs, residents are billed
separately for electricity, water, maintenance, and internet — often on
paper or scattered across disconnected messages and spreadsheets. There's
rarely one place to see what a single resident owes, across everything,
at a glance. This is a real, ongoing admin problem, and the same space
that companies like NoBrokerHood and ApnaComplex operate in.

## What It Does

- Add residents (name + room number)
- Add bills to a resident across three different bill types:
  - **Electricity** — calculated from units consumed × rate per unit
  - **Water** — a flat amount
  - **Internet** — a base amount plus GST
- View a single resident's total dues
- View all residents' dues at once
- View total collection across the entire hostel
- Sort residents by amount owed (via a custom comparison)
- Fully validated input at every step — no crashes on invalid menu
  choices or non-numeric input

## What I Practiced

- **Inheritance** — `ElectricityBill`, `WaterBill`, and `InternetBill` all
  extend a common `Bill` base class, using `super().__init__()` to avoid
  duplicating logic
- **Polymorphism** — `Resident.total_due()` calls `.calculate_total()` on
  every bill in its list without ever checking which bill type it is
- **Composition** — a `Hostel` *has* `Resident`s, and each `Resident`
  *has* `Bill`s — modeling real "has-a" relationships instead of forcing
  inheritance where it didn't belong
- **Magic methods** — `__str__` for clean printing, `__lt__` to make
  residents directly sortable by `sorted()`
- **Defensive input handling** — validating every numeric input before
  conversion, and handling "resident not found" and "invalid bill type"
  explicitly rather than failing silently

## How to Run

```bash
python hostel_manager.py
```

## Possible Future Improvements

- Persist residents and bills to a file so data survives between runs
- Add due dates and track partial/overdue payments
- Add a `RentBill` type and generalize the bill sub-menu to be driven by
  a list/dict of available bill types instead of a hardcoded if/elif chain