# Diagnosis: why the verdict rule rated 28 of 31 negative controls "supported"

Run 2026-11-23 under [the declaration](declaration-verdict-diagnosis.md) (PR #4). Numbers:
`benchmarks/results/diagnosis-verdict-2026-11-23.json`. Code: `src/ctr/diagnosis_verdict.py`.

**Answer.** The rule that was verified reads coverage alone, so any run in which 95% of cells get a pseudotime is
"supported". The controls are not trees by an independent measure, and the methods give them a pseudotime
that follows their latent coordinate. This is a rule failure, not a bug and not a bad control set.

## Evidence

| Explanation | Result | Decision (declared) |
|---|---|---|
| (a) Bug | 0 of 67 recorded levels differ from my re-derivation from the rule text, or from the tool's `verdict(verified=True)` | **Refuted** |
| (b) Bad controls | Every control kind is separated from the 24 tree datasets (seeds 0-5) on the four-point tree defect: trees 0.099-0.168, blob 0.293-0.327, two_groups 0.280-0.387, sheet 0.280-0.297, loop 0.540-0.581. two_groups also has 2 kNN components (trees 1). TwoNN dimension is about 20 for everything (trees 19.7-22.5, loop 20.6-21.4, sheet 21.0-22.2): count noise swamps it, as the declaration warned, so it only separates blob (23.3-24.4) and, by 0.14, two_groups (22.6-23.3) | **Refuted for all four kinds** |
| (c) Permissive rule | C1 (coverage >= 0.95) alone passes 28 of 31 controls, with a margin of exactly 0.05 (their coverage is 1.0). Adding the three left-out checks at the matrix 10% quantile bars, 2 of 31 pass all four (4 at the matrix minimum). Alone: C2 13, C3 18, C4 7 (11 at the minimum) | **Supported**: the permissiveness is the missing criteria, not C1's bar |
| (d) Real property | Median abs Spearman of pseudotime with the latent coordinate: trees 0.98, loop 0.98, sheet 0.93 (blob has none; two_groups is undefined, since one group has no pseudotime). But only 0 of 9 loop and 2 of 9 sheet runs have C1, C3 and C4 all inside the tree range | **Not supported as declared** (the second half of the rule fails) |

Reading (d) fairly: the methods order the cells of a loop or a sheet as the generator does, and C3 is often 1.0
there. C4 is the criterion that leaves the tree range, and for six loop runs it leaves it by being higher than
any tree (0.9996 and up), which the "inside the range" wording counts as outside.

**Hand derivations** (rule text only: C1 passes if coverage >= 0.95; C2-C4 left out, no tau; C5 does not apply;
not_supported if C1 fails, else supported): `blob/seed4 paga_dpt`, `loop/seed4 paga_dpt`, `sheet/seed4 paga_dpt` and
`two_groups/seed5 palantir` all have coverage 1.0, so supported. `two_groups/seed4 paga_dpt` has coverage 0.498,
so C1 fails and it is not_supported. All five match the file.

## Which number, and against which lumencell (Check R)

- **R1 did not reproduce.** At lumenCell_V2 `37197c8` (read through `git archive`, with today's libraries), 66 of 72
  records match the recorded file within 1e-9, including all 28 supported controls. The 6 that differ are
  `two_groups` scfates_ppt, seeds 3-5 (3 runs, two records each): they recorded `IndexError`, now run
  with coverage 1.0 and so are rated supported. That makes 31 of 34 at the recording commit on today's libraries.
  The code is the same, so the difference is in what is installed around it; I did not find which library
  (untested).
- **R2, lumencell 0.5.0: 27 of 30** (blob 9, loop 9, sheet 9, two_groups 0; 6 runs left out). Against the record, only
  `two_groups` palantir and scfates_ppt differ: `DisconnectedGraphError` replaces `InvariantError` and
  `IndexError`, and seed 5 palantir, which ran and was supported, now raises. Every other record is equal.
- **R3.** All six `two_groups` datasets have 2 kNN components. On 0.5.0, Palantir's own kernel graph for seed 5
  has 2 parts (1,454 and 1,546 cells) and the method refuses. At `37197c8` I reproduced the run that completed
  (coverage 1.0, 3 lineages); I did not measure that version's kernel graph.
- **Rule fixed in the declaration, applied:** R1 does not reproduce, so the paper reports **27 of 30 against
  lumencell 0.5.0**, and describes the recorded 28 of 31 (2026-11-17, `37197c8`) as a record that no longer
  reproduces exactly. Either count says the same thing: every blob, loop and sheet run is rated supported.
- **Harness note.** `37197c8`'s `verdict()` has no `verified` argument (the cap commit added it), so `reproduce`
  now counts supported controls with `hand_verdict`, which (a) shows equals the tool. The R2 run used `verify`.
  This changed the run harness after the declaration, not a rule, threshold or seed.

## What this lets the paper claim

A connectivity-only verdict rated every blob, loop and sheet control "supported" (27 of 30 control runs on
lumencell 0.5.0), although an independent four-point measure separates those controls from trees, so
"supported" from that rule means "connected" and nothing more.

Not shown: that C2-C4 could never work (they were non-discriminating on these six seeds), or anything about a
redesigned rule.
