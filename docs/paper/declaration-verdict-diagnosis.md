# Declaration: why did the verdict rule rate 28 of 31 negative controls "supported"?

Declared 2026-11-23, in a PR that is merged before any check below is run. Nothing here changes a
rule, threshold, seed, control or null. The checks are code in `src/ctr/diagnosis_verdict.py`
(tested on toy data only). Results go in a later PR as
`benchmarks/results/diagnosis-verdict-<date>.json` and `docs/paper/diagnosis-verdict.md`.

## What I had already seen (so nobody reads a foreseeable result as a blind test)

Before writing this I read the project handoff (removed from the repo on 2026-11-24; last in git at commit fd0c974) (its Task 8, Task 9 and phase 2 final review
sections), `benchmarks/thresholds.toml`, `src/ctr/verdict_calibration.py`, and I printed the 31 control
rows of `verdict-verification-2026-11-17.json` (coverage, tree-likeness, C3, C4, lineage count). The
HANDOFF already says the verdict was coverage alone ("supported means connected, not a tree").
So explanations (a) and (c) below are confirmations of a documented reading, and I say so in the
results. I have **not** looked at anything that checks (b) or (d): no intrinsic dimension, no
geodesic four-point value, no pseudotime-versus-latent correlation. Those are the real tests.

## Facts settled from the repo before any run (they need no declaration, they are reading)

1. **What the failed rule reads.** In the verification, every tau is `None`
   (`[tree_support.calibrated]`: C2, C3 and C4 non-discriminating) and no clones are configured, so
   C5 is not applicable. `_level` in `lumencell/engine/tree_support.py` then returns `supported`
   whenever C1 (coverage >= 0.95) passes. The 28 of 31 is a **coverage-only** rule. The literature
   note's "reads coverage and clonal support" is right for the Sheih case study (C1 and C5) and wrong
   for the 31-run verification (C1 alone). "Tree-support" is therefore the wrong name for what was
   verified: the module is called `tree_support`, but the verified rule checks connectivity only.
   Suggested name in the paper: "the verdict rule (connectivity-only as verified)".
2. **Was the 31-run check declared in advance? Mostly yes; the literature note is partly wrong.**
   `[tree_support.verification]` (fresh seeds 3-5, the four control kinds, `max_controls_supported = 0`,
   `on_failure = "provisional"`) was added in commit `fdc200a` (2026-11-17 03:53 -0600). The calibration
   record is `b24ad66` (05:50) and the verification record is `56fa741` (06:25), same day. So the
   check, its seeds, its controls and its pass bar were declared in a dated commit about 2.5 hours
   before it ran. What was **not** declared is the number 31: it is 36 control runs minus 5 whose
   reference run failed (a count that fell out of the run). Also true, and the reason to avoid the
   word: there is no public registry entry. The repo supports "declared in a dated commit before the
   run", not "pre-registered".
3. **Where the numbers sit.** 72 records, 5 left out (all `two_groups`), 67 verdicts, 31 of them
   controls: 28 supported (blob 9, loop 9, sheet 9, two_groups 1), 3 not_supported (two_groups
   paga_dpt, coverage 0.48-0.51). Matrix: 36 of 36 supported.

## Check R: which number does the paper report, and against which lumencell?

The recorded file says `commit 37197c84dcecdc195191f58c56c4f2584af7c98d` (a lumenCell_V2 commit; I only
read it, with `git archive` into a scratch folder, never a worktree or checkout there). The disconnected-graph
error (`DisconnectedGraphError`, `engine/graph.py::require_connected`) arrived in lumenCell_V2 commit
`35ac459` (2026-11-19, PR #40), after that run. The HANDOFF explains the expected consequence (palantir
`two_groups` runs now raise); R checks it instead of trusting it.

- **R1 (reproduce at the recording commit).** Extract `37197c8` from lumenCell_V2 read-only
  (`git archive`), put its `src` first on `PYTHONPATH`, rerun the declared verification (seeds 3-5,
  the four controls and four topologies, three methods, 72 runs) with the unchanged
  `ctr.verdict_calibration.collect_records` and `verify`. Compare to the recorded file field by field:
  `coverage`, each tree-likeness value, `lineage_stability`, `pseudotime_stability`, `n_lineages`,
  `error` equal within 1e-9 (numbers) or exactly (strings and counts); and the 28 of 31.
- **R2 (the same run on the pinned lumencell 0.5.0).** Same call, installed 0.5.0. Report the count
  and every record that differs from the recorded file, with the exception text.
- **R3 (why two_groups/seed5 palantir changed).** On both versions: build `two_groups/seed5`, run prep,
  count connected components of the kNN graph and of the Palantir kernel graph, and print the
  exception. Prediction (from the HANDOFF): two parts on both versions; ran at 37197c8, raises
  `DisconnectedGraphError` at 0.5.0.
- **Which number the paper reports (rule fixed now).** If R1 reproduces every record, the paper
  reports **28 of 31, at lumenCell_V2 commit 37197c8**, and one sentence says that lumencell 0.5.0
  gives 27 of 30 because a method now refuses a disconnected graph. If R1 does not reproduce, the
  paper reports the R2 number against 0.5.0 (the pinned release anyone can install) and the recorded
  file is described as a record that no longer reproduces, with the differing records listed.
  Either way the claim "most negative controls were rated supported" holds if (and only if) the
  results say so; the count, not the wording, is what R fixes.

## The four explanations

Population for all of them: the 31 recorded control verdicts (the 30 of R2 are reported alongside).

### (a) Bug

**Test.** (i) Hand re-derivation: for three recorded control runs I derive the verdict from the saved numbers
and the rule text in `thresholds.toml` alone, in the results document, step by step. The three are
fixed now, so I cannot pick convenient ones: `blob/seed4 paga_dpt`, `loop/seed4 paga_dpt`,
`sheet/seed4 paga_dpt` (one supported run per kind, one method that ran on every kind), plus the one
odd supported run `two_groups/seed5 palantir` and one not_supported run `two_groups/seed4 paga_dpt`
as a fifth and sixth case. (ii) Mechanical re-derivation: `diagnosis_verdict.hand_verdict`, written from
the rule text (C1 pass iff coverage >= `coverage_min`; C2, C3 and C4 excluded when their tau is absent;
C5 not applicable without clones; `not_supported` if C1 fails; `supported` otherwise) and not from the
tool's code, applied to all 67 recorded verdicts. (iii) The tool's own `verdict(..., verified=True)`
on the same inputs.
**Decision.** A bug is supported if any of the 67 recorded levels differs from (ii) or (iii). Zero
differences refutes it. If it is a bug, I report it and **stop**: no fix, no rerun, no new threshold.

### (b) Bad controls: do the negative controls lack tree structure?

Measured with three things that do not use C1-C5, the verdict, or any method's output:

- **Intrinsic dimension** (TwoNN, Facco et al. 2017, doi:10.1038/s41598-017-11873-y): on the 30 PCs the
  kNN graph uses (`PrepParams.neighbors_pcs`), `d = (n - 1) / sum(log(r2 / r1))` over cells with `r1 > 0`,
  Euclidean, no discard.
- **Connected components** of the prep kNN graph (`connectivities`, edges = non-zero entries).
- **Four-point tree defect** (Gromov): 300 landmarks (seeded draw, `default_rng(0)`) inside the largest
  connected part, geodesic distances on the kNN `distances` graph; for 200,000 random landmark quadruples
  (same seed) the defect is `(largest - middle) / diameter` of the three pair sums
  `d(x,y)+d(z,w), d(x,z)+d(y,w), d(x,w)+d(y,z)`; the statistic is its 99th percentile. A tree metric has
  defect 0. Caveat I know now: a structureless blob is star-like and can score low, which is why the
  statistic is read together with the dimension, not alone.

Datasets: every verification and calibration dataset (seeds 0-5): 24 control datasets (6 per kind) and
24 tree datasets (4 topologies x 6 seeds). No fitted threshold is involved, so reusing those seeds
leaks nothing.
**Decision (per control kind, fixed now).** The kind is **separated from trees** if, on at least one of the
three measures, its six values and the 24 tree values do not overlap (no kind value falls in
[min, max] of the trees, and for the dimension and defect the kind lies wholly on one side). The kind is
**not separated** if on all three measures it overlaps. "Bad controls" is supported for a kind only if it
is not separated. If a kind is not separated, the results say plainly that these measures cannot tell it
from a tree and that its supported rows are not clean false positives. Predictions: blob separates on
dimension; two_groups on components; sheet on dimension or defect; loop only on defect, and it may not
separate (a loop minus its seam is a path, and a linear trajectory is a valid tree in the matrix).
I also report the construction audit: what each generator in `lumencell/bench/synth_controls.py` builds
(blob: no latent coordinate; two_groups: two groups, 2x programme scale; loop: angle with cosine
programmes; sheet: two independent uniform coordinates).

### (c) Permissive rule: which criterion lets controls through, and by how much?

**Test, from saved numbers only.** For each of C1-C4, the share of the 31 verification controls that pass
that criterion **alone**, with each of C2-C4 given the bar the calibration rule would use if the check
had discriminated: the matrix 10% quantile (the declared `matrix_quantile`, numpy linear) and, as a
second bar, the matrix minimum, both taken from the calibration file's 36-run matrix (C2: its 12
datasets, NaN counted as 0, factor 1.0). C1's bar is the fixed 0.95. For each criterion: pass count,
the median, minimum and maximum margin (value minus bar) among controls that pass, and the pass count
of every combination C1+C2, C1+C3, C1+C4 and all four.
**Decision.** The criterion that lets the most controls through is named. "Permissive rule" is supported
if the verdict's supported count equals the pass count of C1 alone (it must, by construction) **and** the
pass count of all four criteria at the matrix-q10 bars is smaller than that: the permissiveness then
comes from the criteria that were left out, not from C1's bar. If all four at the matrix-q10 bars still
pass at least half of the 31 controls, the checks themselves cannot tell these controls from trees, and
the results say that instead.

### (d) Real property: do the methods give stable, connected, tree-like output on non-tree data?

**Test.** On every control run (reference run only, no stability rerun) in the verification seeds 3-5, on the
version R fixes: (1) the verified C1, C3 and C4 values from the saved records, compared with the tree
datasets' range from the same file (q10 to max); (2) the lineage count; (3) |Spearman| between the
method's pseudotime and the generator's latent coordinate over cells with a finite pseudotime: loop,
`min(angle, 2pi - angle)` (angular distance from the root); sheet, `sqrt(x^2 + y^2)` (distance from the
root corner); two_groups, the group indicator; blob has none and is reported as "no latent coordinate".
For tree datasets the coordinate is `true_pseudotime`, as a reference.
**Decision.** "Real property" is supported for loop and sheet if their median |Spearman| is at least 0.5
and at least half of their runs have C1, C3 and C4 inside the tree range, so the methods return a
connected, stable, ordered output that is simply not evidence of a tree. It is supported for a kind
that has no latent coordinate (blob) only on stability and coverage, and the results say that there the
output is not ordered by anything. The 0.5 cut-off is declared before the number is seen. It is not
tuned.

## What can be said at the end (templates fixed now, one is chosen by the outcome)

- (a) refuted, (c) supported, (b) not separated or partly separated, (d) supported for loop and sheet:
  "The verdict rule as verified reads connectivity only; on controls the methods return connected,
  stable, ordered output, so connectivity cannot tell a tree from them."
- (a) refuted, (c) supported, (b) separated for every kind: "...the controls are not trees by independent
  measures, and the connectivity-only rule rates them supported; the failure is the rule."
- (a) supported: "A defect in the rule's implementation is documented; no claim about the rule is made.
  Stopped."

## Limits, stated now

Six seeds per kind. TwoNN on count PCs can be dominated by noise dimensions. The four-point statistic is
sampled. The latent coordinates are my choice, declared above. None of this evaluates a redesigned rule.
