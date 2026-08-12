# Topic 8 — Day 1: Shell & Command-Line Foundations

## Navigation
| Command | What it does |
|---|---|
| `pwd` | Print working directory — where am I right now |
| `ls` | List files/folders in the current location |
| `cd <folder>` | Move into a folder |
| `cd ..` | Move up one level (parent folder) |
| `cd ../..` | Move up two levels in one command |
| `cd .` | Refers to the current folder (used constantly in commands like `git add .`) |

## File & Folder Manipulation
| Command | What it does |
|---|---|
| `mkdir <name>` | Create a new folder |
| `touch <file>` | Create a new, empty file |
| `rm <file>` | Delete a file — **permanent, no undo, no recycle bin** |
| `rm -r <folder>` | Delete a folder and everything inside it — same permanence, higher stakes |
| `cp <src> <dest>` | Copy a file |
| `mv <src> <dest>` | Move or rename a file |

## Reading Files & Chaining Commands
| Command | What it does |
|---|---|
| `cat <file>` | Print a file's entire contents directly into the terminal |
| `\|` (pipe) | Feeds one command's output as the next command's input |

Example: `ls | grep "topic"` — lists everything in the current folder, then
filters that list down to only lines containing "topic".

## Core Habit
Always verify before acting, especially before anything destructive:
`pwd` → confirm where you are → `ls` → confirm what's actually there →
*then* run the risky command. Cheap insurance, expensive to skip.

## DSA Micro-Drill: merge_sorted(list1, list2)
Merge two already-sorted lists into one sorted list, without concatenating
and calling `sorted()` — walk both lists with two pointers, always taking
the smaller front element, then append whatever's left over once one list
runs out (already sorted, so no more comparisons needed).

See `day1_merge_sorted.py` for the solution.
