#!/usr/bin/env bash
# Saves the GitHub API responses behind docs/paper/declarations.md. Read-only calls; needs `gh auth login`.
# Run from the repo root: bash docs/paper/evidence/fetch.sh
# Each file is the API's JSON body, all pages wrapped in one outer array (gh api --paginate --slurp).
# *.headers keep the first page's status line, Date (GitHub's own clock) and X-GitHub-Request-Id; headers that
# describe the caller's token (scopes, rate limits) are dropped.
set -euo pipefail
out=docs/paper/evidence
lc=repos/shreyandhawa/lumenCell_V2
ctr=repos/shreyandhawa/clonal-trajectory-research

get() {  # get <api path> <file stem>
  gh api --paginate --slurp "$1" > "$out/$2.json"
  gh api --include "$1" | sed -n '1,/^\r\{0,1\}$/p' | grep -i -E '^(HTTP/|date:|x-github-request-id:)' > "$out/$2.headers"
}

get "$lc/events?per_page=100" lumenCell_V2-events
get "$ctr/events?per_page=100" clonal-trajectory-research-events
get "$lc/pulls?state=all&per_page=100" lumenCell_V2-pulls
get "$ctr/pulls?state=all&per_page=100" clonal-trajectory-research-pulls
for n in 7 12 14 26 30 32 33 38 45 51 52 53 54 55 56 57; do
  get "$lc/pulls/$n/commits?per_page=100" "lumenCell_V2-pr$n-commits"
done
for n in 4 5 7 8; do
  get "$ctr/pulls/$n/commits?per_page=100" "clonal-trajectory-research-pr$n-commits"
  get "$ctr/issues/$n/timeline?per_page=100" "clonal-trajectory-research-pr$n-timeline"
done
{ date -u +"fetched %Y-%m-%dT%H:%M:%SZ (local clock)"; gh --version | head -1; } > "$out/FETCHED"
