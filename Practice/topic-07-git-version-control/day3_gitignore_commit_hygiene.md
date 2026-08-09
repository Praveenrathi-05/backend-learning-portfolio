# Topic 7, Day 3 -- .gitignore, Commit Messages & Real-World Habits

## What I practiced (hands-on, on the real backend-learning-portfolio repo)

- Created a `.gitignore` file listing `__pycache__/`, `*.pyc`, and the
  personal data files my projects generate (movies.txt, expenses.txt,
  scores.txt, etc.)
- Committed `.gitignore` with a clear message
- Confirmed via `git status` that none of those files show up as
  untracked, even though they exist in the project folders

## Key concepts

**`.gitignore` only prevents FUTURE tracking.** If a file was already
committed before being added to `.gitignore`, it stays in history --
`.gitignore` won't retroactively remove it. Correct order: create and
commit `.gitignore` FIRST, before committing anything it's meant to hide.

**Commit messages are messages to future-you (or a teammate).**
Vague messages like "fixed stuff" or "changes" become genuinely useless
across a large history -- there's no way to find the commit that touched
a specific thing without manually reading every diff. Convention worth
using: `Fix: ...`, `Add: ...`, `Update: ...`, `Remove: ...` prefixes,
so `git log` is scannable at a glance.

**Commit in small, logical chunks, not one giant commit at the end.**
Smaller commits = more save points to return to. One giant commit for
a whole session means you can only go back to "before" or "after"
the entire session, with nothing usable in between.

## Example .gitignore used in this project

```
__pycache__/
*.pyc
movies.txt
expenses.txt
scores.txt
.env
```
