# GitHub records behind the declaration timeline

These are the raw GitHub API responses used for [declarations.md](../declarations.md). They are saved here
because GitHub's repository event log, the source of the push and branch-creation times, keeps at most 300 events
for 90 days. This copy goes into the archive before that log expires.

**How they were fetched.** `bash docs/paper/evidence/fetch.sh`, from the repo root, on 2026-11-24 at about 03:10 UTC
(`FETCHED` holds the local clock and the gh version; each `.headers` file holds GitHub's own `Date` and request id).
The script makes read-only calls with `gh api --paginate --slurp`, so each `.json` file is an array of pages, each
page being the API's JSON array as returned. Nothing was edited after the fetch.

| Files | API path | Used for |
|---|---|---|
| `lumenCell_V2-events.json` | `repos/shreyandhawa/lumenCell_V2/events` | push and branch-creation times (300 events, 2026-11-12 13:57 to 2026-11-23 14:47 UTC) |
| `clonal-trajectory-research-events.json` | `repos/shreyandhawa/clonal-trajectory-research/events` | PR opened and merged events, rows 9-10 |
| `*-pulls.json` | `repos/<repo>/pulls?state=all` | PR opened and merged times, merge commits |
| `lumenCell_V2-pr<n>-commits.json` | `repos/shreyandhawa/lumenCell_V2/pulls/<n>/commits` | declaration and run commits in each PR, rows 1-8 |
| `clonal-trajectory-research-pr<n>-commits.json`, `-timeline.json` | `.../pulls/<n>/commits`, `.../issues/<n>/timeline` | rows 9-10, including the force-pushes |

**What this copy proves, and what it does not.** It is a copy made by the author, not a record signed by GitHub,
so it is only as trustworthy as the author. While GitHub still serves the same data, a reader can re-run
`fetch.sh` and compare. After that, the copy stands on its own, and the commit hashes it names can still be
checked against the git history (and against the Software Heritage snapshot, if that has been made; see
[archive-steps.md](../archive-steps.md)).

The responses include each commit's author name and email. The same details are already in this repository's
public git history.
