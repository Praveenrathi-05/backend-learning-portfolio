# Topic 8 — Day 3: Edge Cases, Production Reality, Real-World Problems

## Edge Cases & Trade-offs

**grep and special characters:** `grep` patterns are actually regex under
the hood, even for "plain" searches. Characters like `(`, `)`, `$` have
special meaning (`$` = end of line, `()` = grouping). Searching for a
literal `price ($)` can silently misbehave unless those characters are
escaped -- a direct preview of Topic 9 (Regular Expressions).

**`rm -r` vs `rm -ri`:** `-r` deletes immediately, no confirmation.
`-ri` asks "are you sure?" per item -- slower, but worth it when unsure
exactly what's about to be deleted.

**Verification costs time, but saves more:** `pwd`/`ls` before a
destructive command costs a few seconds. An unrecoverable mistake costs
far more -- same "cheap insurance" logic as a guard clause in code.

## Useful Chained Command
```bash
grep -r "TODO" . --include="*.py" | wc -l
```
`--include="*.py"` restricts the search to only `.py` files. `wc -l`
("word count, lines") counts how many lines came through the pipe --
turning "show me every match" into "tell me how many matches."

## Production Reality
- `grep` is the practical first line of defense before touching any file
  in a codebase too large to read manually.
- Tab completion doubles as typo-prevention: if it doesn't complete,
  something's wrong before you've run anything.
- Multi-cursor editing (`Ctrl+D`) is safe and reversible; eyeballing a
  `grep -r` rename across many files by hand is how subtle bugs sneak in
  (catch 8 of 9 occurrences, miss one).

## Real-World Problems

**Problem 1 — Developers on unreliable/metered mobile data:**
- *Online angle:* Cloud log-analysis tools (Datadog, Splunk) work well but
  need a stable, often costly connection, and send data to a third party.
- *Offline angle:* `grep`, `cat`, and piping work entirely locally, zero
  network dependency, zero data leaving the machine -- the fallback that
  always works.

**Problem 2 — New developers making irreversible `rm -r` mistakes:**
- *Online angle:* Cloud platforms increasingly offer soft-delete/versioned
  backups (S3 versioning, Drive trash) -- but only if configured in advance.
- *Offline angle:* `pwd`/`ls` discipline plus small, frequent Git commits
  means even local files are protected -- a committed file can always be
  recovered with `git checkout`, even with zero internet connection.

## DSA Micro-Drill: is_rotation(list1, list2)
Given two lists, determine whether `list2` is some rotation of `list1`.

Example:
```
is_rotation([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]) -> True   (k=2 rotation)
is_rotation([1, 2, 3], [1, 3, 2]) -> False              (same elements, wrong order)
```

Core idea: reuse `rotate_list` rather than writing rotation logic again --
try every rotation amount from 0 to len(l1)-1 and check for a match.

See `day3_is_rotation.py` for the solution, including the empty-list edge
case (`[] == []` is trivially a rotation of itself).
