# Topic 8 — Day 2: grep, History, Tab Completion, Editor Shortcuts

## Searching Inside Files with grep
| Command | What it does |
|---|---|
| `grep "text" file` | Print every line in `file` containing "text" |
| `grep -r "text" .` | Recursive — search "text" in every file, every subfolder, from here |
| `grep -r "def " . \| grep ".py"` | Chained: find every function def, then narrow to only matches from `.py` files |
| `grep -rl "text" .` | `-l` (lowercase L) — list only the **filenames** that match, not every matching line |

## Terminal Speed Habits
- `history` — shows numbered list of recent commands
- **Up arrow** — cycle backward through recent commands instead of retyping
- **Tab completion** — auto-completes file/folder names; if it *doesn't*
  complete, that's a signal something's misspelled or you're in the wrong
  place, *before* you run something risky

## VSCode Shortcuts Worth Knowing Cold
| Shortcut | What it does |
|---|---|
| `Ctrl + P` | Quick-open any file by typing its name |
| `` Ctrl + ` `` | Open/close the integrated terminal |
| `Ctrl + /` | Comment/uncomment current line or selection |
| `Ctrl + D` | Select next occurrence of the selected word — multi-cursor rename |
| `Ctrl + Shift + F` | Search across the entire project (VSCode's version of `grep -r`) |
| `Alt + Up/Down` | Move the current line up or down |
| `Ctrl + Z` / `Ctrl + Shift + Z` | Undo / redo |

**Ctrl + D mechanism:** click/select the first occurrence of a word, press
`Ctrl + D` repeatedly to add each next occurrence to a multi-cursor
selection, then type once to replace all of them simultaneously.

## DSA Micro-Drill: rotate_list(lst, k)
Rotate a list right by `k` positions.

Example:
```
rotate_list([1, 2, 3, 4, 5], 2) -> [4, 5, 1, 2, 3]
```

Core idea: split the list into two pieces at a cut point (the last `k`
elements, and everything before them), then swap their order — last piece
first, then first piece — using slicing and `+` concatenation.

See `day2_rotate_list.py` for the solution, including two edge cases found
while testing: `k` larger than the list length, and an empty list.
