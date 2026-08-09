# Topic 7, Day 1 -- Git Foundations

## What I practiced (hands-on, on the real backend-learning-portfolio repo)

- `git status` -- checking what's modified / staged / committed at any point
- `git add <file>` -- staging a specific change (the "shopping cart" step)
- `git commit -m "message"` -- permanently saving a snapshot locally
- `git log` -- viewing commit history

## Key concepts

**The three-stage model:**
```
Working Directory  -->  Staging Area  -->  Repository
   (editing)            (git add)          (git commit)
```

**Key insight:** `git add` does NOT save anything permanently -- only
`git commit` does. If the computer crashed after `add` but before `commit`,
the staged change would be lost -- same idea as an unclosed file buffer
not being saved (Topic 5).

**Why staging exists as a separate step:** it lets you group unrelated
changes into separate, focused commits instead of one messy commit that
mixes everything you happened to touch in a session.
