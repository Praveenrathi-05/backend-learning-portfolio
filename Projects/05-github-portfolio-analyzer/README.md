# GitHub Portfolio Analyzer

A command-line tool that pulls live data about my own GitHub profile via
the GitHub API, combines it with a local scan of my actual portfolio repo,
and tracks how both change over time.

## The Problem

After 10 topics of building this portfolio, there was no easy way to see
it summarized — total public repos, how many Python files exist, how many
TODOs are still outstanding — without manually clicking through GitHub and
folders. This is also a genuinely common real category of developer tool:
GitHub profile analyzers and contribution trackers exist because engineers
want visibility into their own output over time.

## What It Does

- Fetches live profile data (public repo count, followers, bio) from the
  real GitHub API, with full error handling: bad status codes, connection
  failures, and timeouts are all handled distinctly, never crashing the
  program
- Scans the actual local repo folder for `.py` files, counts function
  definitions (`def `), and finds every `TODO`/`FIXME` comment using regex
- Combines both sources into one summary and saves it as a timestamped
  JSON report
- Loads the previous report and shows exactly what changed since last time
  (e.g. `Public repos: 3 → 4 (+1)`)
- Times every GitHub API call via a `@timer` decorator
- Refuses to save or compare a report built from failed/missing GitHub
  data, rather than silently persisting a broken value that would crash a
  later comparison — guarded at both the point data is generated and the
  point it's consumed

## What I Practiced

- Composition across three levels (`PortfolioReport` has-a `GitHubProfile`
  and has-a `RepoScanner`)
- Real HTTP requests with full status-code / `ConnectionError` / `Timeout`
  handling
- Regex (`re.findall`) applied to real, local file content, not toy strings
- JSON persistence with delta comparison between two saved reports
- A decorator (`@timer`) applied to a method, not just a plain function
- Tracing and fixing a real self-found bug: an unhandled failed API fetch
  silently corrupting a later report comparison (`int - None`) — fixed
  with validation at both the save point and the load point

## How to Run

```bash
python portfolio_analyzer.py
```

Update the `RepoScanner(...)` path and the `GitHubProfile(...)` username
at the bottom of the file to point at your own repo and GitHub account.

## Possible Future Improvements

- Run automatically on a schedule instead of manually via the menu
  (a direct preview of CI/CD and scheduled jobs)
- Track history across more than just the single most recent report,
  instead of only comparing against the last save
- Scan for additional signals (commit message quality, test coverage)

## Open Scalability Question

If this needed to check GitHub stats automatically every day without
being run manually, what would need to change? Not yet answered — a
direct preview of scheduled/background jobs and CI/CD (Topic 71).
