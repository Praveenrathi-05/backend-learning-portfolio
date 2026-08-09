# Topic 7, Day 2 -- Branching

## What I practiced (hands-on, on the real backend-learning-portfolio repo)

- `git branch` -- listing all branches (each one is a lightweight pointer
  to a commit, NOT a separate copy of the files on disk)
- `git checkout -b practice-branch` -- created and switched to a new branch
  in one step
- Made a small change, committed it on `practice-branch`
- Switched to `main` -- confirmed the change was NOT there
- Switched back to `practice-branch` -- confirmed the change WAS there
- `git checkout main` then `git merge practice-branch` -- merged the work
  back in, confirmed the change now appears on `main` too

## Key concepts

**Branches are pointers, not copies.** Switching branches doesn't copy
files into a new folder -- it repoints the working directory to whatever
commit that branch's pointer currently points at. This is why creating
a branch is instant, and why work on one branch is completely invisible
on another until a merge happens.

**Why teams rely on branches:** without them, multiple engineers editing
`main` directly would either overwrite each other's work or leave `main`
in a constantly broken, half-finished state. Branches let each person
work in isolation until their piece is genuinely done and tested, keeping
`main` (or `production`) always in a working state.

**Merge conflicts:** happen when two branches changed the same lines
differently. Git marks both versions directly in the file with
`<<<<<<<` / `=======` / `>>>>>>>` markers -- it's not a crash, just Git
correctly refusing to guess which version is right.
