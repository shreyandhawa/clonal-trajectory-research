# Archiving the two repositories (for you to do)

Nothing here has been done. A Zenodo DOI and a Software Heritage snapshot are permanent and public, so you run
every step. Read 2026-11-23: both repositories are public and MIT-licensed. lumenCell_V2 has the tag `v0.5.0`
(`24f3fdd`), and PyPI's lumencell 0.5.0 was uploaded 2026-11-23 15:01 UTC. clonal-trajectory-research has no tags.

## Order

1. Merge PR 3 (the draft), so the archive holds the text it supports.
2. Reserve both DOIs on Zenodo (steps A1 and B1). Reserving gives the DOI without publishing anything.
3. Put both DOIs in the draft's references and the README, and merge that.
4. Tag and archive clonal-trajectory-research (B2 to B4), then archive lumencell (A2 to A3).
5. Save both repositories at Software Heritage (C).

## A. lumencell (github.com/shreyandhawa/lumenCell_V2, tag v0.5.0)

The paper's numbers were made with lumencell 0.5.0 from PyPI. One footnote also uses lumenCell_V2 commit
`37197c8`, which is not a release. A Zenodo archive holds only the files at the tag, not the git history, so
`37197c8` is kept by step C.

A1. Zenodo → New upload. Upload type: Software. Click "Reserve DOI" and copy it. Do not publish yet.

A2. On your machine, make the archive from the existing tag (this reads the repo; it changes nothing):

```bash
git clone --bare https://github.com/shreyandhawa/lumenCell_V2.git /tmp/lc.git
```

```bash
git -C /tmp/lc.git archive --format=zip --prefix=lumencell-0.5.0/ -o /tmp/lumencell-0.5.0.zip v0.5.0
```

Optionally also attach the two PyPI files for 0.5.0 (the wheel and the sdist, from pypi.org/project/lumencell/0.5.0/#files).

A3. Upload the zip to the draft. Metadata: Title "lumencell 0.5.0"; Creator: your name, "Independent researcher",
ORCID; Version 0.5.0; Licence MIT; Related identifier "is supplement to" the GitHub tag URL
`https://github.com/shreyandhawa/lumenCell_V2/tree/v0.5.0`. Check the preview, then press Publish.

(Another route: Zenodo's GitHub integration archives each new GitHub release automatically. It only reacts to
releases made after you turn it on, and it publishes with no draft to check, so the manual upload above is safer
for a one-off.)

## B. clonal-trajectory-research (this repository)

B1. Zenodo → New upload → Software → "Reserve DOI". Keep the draft unpublished.

B2. Add a `CITATION.cff` at the root with your name, ORCID and the two DOIs. A template (fill in the angle brackets):

```yaml
cff-version: 1.2.0
title: "clonal-trajectory-research: an evaluation of trust checks for single-cell trajectory inference"
version: 0.1.0
doi: <reserved DOI from B1>
license: MIT
repository-code: https://github.com/shreyandhawa/clonal-trajectory-research
authors:
  - family-names: <family name>
    given-names: <given name>
    affiliation: Independent researcher
    orcid: https://orcid.org/<ORCID>
references:
  - type: software
    title: lumencell
    version: 0.5.0
    doi: <DOI from A1>
```

Merge it through a PR as usual.

B3. Tag the merged commit on main and push the tag:

```bash
git switch main && git pull --ff-only
```

```bash
git tag -a v0.1.0 -m "Archive for the preprint"
```

```bash
git push origin v0.1.0
```

Then make a GitHub release from the tag (GitHub → Releases → Draft a new release → choose v0.1.0 → Publish), or
with `gh release create v0.1.0 --title "v0.1.0: archive for the preprint" --notes "Code, declarations and results behind the preprint."`.

B4. Make the zip from the tag and upload it to the B1 draft:

```bash
git archive --format=zip --prefix=clonal-trajectory-research-0.1.0/ -o /tmp/ctr-0.1.0.zip v0.1.0
```

Metadata: as in A3, Version 0.1.0, Related identifiers "is supplement to" the GitHub release URL and "requires"
the lumencell DOI. Check the preview, then Publish.

Check before publishing: the zip holds `benchmarks/results/`, `docs/paper/`, `src/`, `uv.lock` and the `Makefile`,
and `make paper-numbers` runs from an unzipped copy after `uv sync`.

## C. Software Heritage (keeps every commit)

The timeline in [preregistration.md](preregistration.md) rests on commit hashes, including lumenCell_V2 commits
that are in no release. Software Heritage archives the whole history with its hashes:

1. Open https://archive.softwareheritage.org/save/ .
2. Origin type "git", URL `https://github.com/shreyandhawa/lumenCell_V2`, submit. Repeat for
   `https://github.com/shreyandhawa/clonal-trajectory-research`.
3. When each save shows "succeeded", copy its SWHID for the commits the paper names (`37197c8` and the declaration
   commits) and add them to preregistration.md if you want permanent references.

## What is not archived anywhere yet

- GitHub's event log (push times used in preregistration.md) keeps at most 300 events for 90 days. The raw
  responses were saved on 2026-11-24 in [evidence/](evidence/README.md), so they go into the archive with the repo.
- The cached datasets are not archived by you; each is cited by its own accession ([data.md](data.md)).
