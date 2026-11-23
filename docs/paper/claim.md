# Claim and scope of the paper

Written 2026-11-23 from the diagnosis pages ([verdict](diagnosis-verdict.md), [clonal](diagnosis-clonal.md)),
their declarations, the [literature check](literature.md) and the result files named below. No analysis was run
for this page. Every number below is read from a result file. The draft takes its wording from here.

## The claim

> **1.** The verdict rule of the trajectory tool lumencell, as it was checked, looks at one thing: whether at
> least 95% of cells get a pseudotime. On lumencell 0.5.0 it rated <!--n:verdict.r2-->27 of 30<!--/n--> negative-control runs
> "supported" (every blob, loop and sheet run), although a tree measure that uses none of the rule's inputs
> separates all four control kinds from the tree datasets.[^verdict]
>
> **2.** In one public CAR-T dataset (Sheih et al. 2020: four patients, three methods, <!--n:clonal.n_runs-->12<!--/n--> runs), agreement
> between T-cell-receptor clones and the returned lineages, scored against a clone shuffle within time point,
> is under half its value against a shuffle within patient in the point estimate of every run (ratio <!--n:clonal.R_range-->0.03 to
> 0.49<!--/n-->; the two highest bootstrap intervals reach <!--n:clonal.NHL-7/palantir.R_hi-->0.625<!--/n--> and <!--n:clonal.NHL-7/scfates_ppt.R_hi-->0.770<!--/n-->). A k-means clustering that uses no trajectory
> comes within <!--n:clonal.delta_abs_max-->0.05<!--/n--> of the score in every run; the lift's bootstrap interval is above zero in <!--n:clonal.delta_ci_above-->4<!--/n--> runs and
> wholly below zero in <!--n:clonal.delta_ci_below-->3<!--/n-->.[^clonal]

The two are separate findings and the paper keeps them in separate sentences. Both are about these checks on
this data. Neither is a claim about trajectory methods in general, about any method's correctness, or about
the biology of CAR-T cells.

[^verdict]: `benchmarks/results/diagnosis-verdict-2026-11-23.json`, `reproduce_on_0_5_0.n_controls_supported`
    = 27 of 30 scored (6 of 36 control runs left out because the method raised); the four-point tree defect
    is under `structure` (trees 0.099-0.168; blob 0.293-0.327, two_groups 0.280-0.387, sheet 0.280-0.297,
    loop 0.540-0.581). The verification recorded on 2026-11-17
    (`benchmarks/results/verdict-verification-2026-11-17.json`, lumenCell_V2 commit `37197c8`) gave <!--n:verdict.recorded-->28 of 31<!--/n-->.
    That record does not reproduce exactly even at its own commit: rerun there with today's libraries, <!--n:verdict.r1_match-->69 of
    72<!--/n--> records match and the count is <!--n:verdict.r1-->31 of 34<!--/n-->, because three `two_groups` scfates_ppt runs that raised
    `IndexError` now complete (`reproduce_at_37197c8`). Which library changed was not found.

[^clonal]: `benchmarks/results/diagnosis-clonal-2026-11-23.json`, `sheih_bootstrap` (clone bootstrap, 500
    replicates, 95% percentile intervals). Ratio intervals: NHL-7 palantir <!--n:clonal.NHL-7/palantir.R-->0.439 [0.179, 0.625]<!--/n-->, NHL-7
    scfates_ppt <!--n:clonal.NHL-7/scfates_ppt.R-->0.491 [0.245, 0.770]<!--/n-->. The diagnosis page rounds the first upper bound
    to 0.62; it is 0.6253, so two decimals give 0.63, and this page gives three. Lift (Δη) point values -0.050 to +0.049; intervals above zero: CLL-1
    paga_dpt, CLL-2 paga_dpt, NHL-7 paga_dpt, NHL-7 scfates_ppt; wholly below: CLL-1 palantir, NHL-6 palantir,
    NHL-6 scfates_ppt. The intervals do not cover the method run, the k-means partition, or which patients
    were sampled.

## What goes with the claim (stated in the paper, not part of the claim sentence)

- **The failure is the rule.** The recorded verdicts equal a re-derivation from the rule text in 67 of 67 cases
  (no bug). Adding the three criteria the rule left out, at bars taken from the tree datasets (their 10%
  quantile), <!--n:verdict.all_four_q10-->2 of 31<!--/n--> recorded controls pass all four (<!--n:verdict.all_four_min-->4 of 31<!--/n--> at the tree minimum).[^combos] This count is
  on the 31 recorded controls, not on the 30 of lumencell 0.5.0.
- **What follows from the failure.** A "supported" verdict from this rule means "connected", nothing more. The
  tool therefore never shows "supported" on real data; it caps it at "not shown to be a tree".
- **What is open.** Synthetic data with clones confined to time points did not raise the within-patient score
  (median 0.013 and 0.005, against the 0.05 the declared test needed), and a real lineage signal kept its score
  under the time-point shuffle (ratio 1.00). So neither "time inflates the score" nor "the time-point shuffle
  over-corrects" reproduces the Sheih drop. What does explain it is an open question, and the paper says so.
  The paper does not call the score confounded.[^synth]
- **Not shown.** That the left-out criteria could never work, anything about a redesigned rule, any tree in
  Sheih, any direction of differentiation (the root is assumed), or anything beyond four patients.

[^combos]: `diagnosis-verdict-2026-11-23.json`, `criteria.combos["C1+C2+C3+C4@matrix_q"]` = 2,
    `["C1+C2+C3+C4@matrix_min"]` = 4; `criteria.criteria["C1@fixed"].passes` = 28.

[^synth]: `diagnosis-clonal-2026-11-23.json`, `synthetic.summary` and `synthetic.decisions` (40 seeds,
    600-639; outcome "D1 fails").

## Wording rules

| Write | Not |
|---|---|
| "declared in advance in the public repository, with commit timestamps" | "pre-registered" (there is no registry entry) |
| "a coverage-based verdict", "the verdict rule as checked" | "tree-support rule", "tree-likeness verdict" |
| "shuffle within time point", "shuffle within pseudotime bin" | "time- and depth-matched" (depth here is pseudotime, not sequencing depth) |
| "under half in the point estimate of all 12 runs", with the intervals | "vanished", "under half in all 12 runs" with no qualifier |
| "within 0.05 of a k-means clustering", with the intervals | "4 of 12 pass" as the only statement of the k-means result |
| "one dataset, four patients" | anything implying a second dataset (Daniel 2022 was declined) |

## What is already known, and must be cited

The literature check finds the claim **partly known**. The paper does not present any of these as new, and
cites each where the point comes up. All are in the main tables of [literature.md](literature.md) (title and
DOI matched; most read at abstract level only).

| Known point | Cite |
|---|---|
| T-cell clones or lineage barcodes used to check or build trajectories | Zhang 2018 (STARTRAC, doi:10.1038/s41586-018-0694-x); Xie 2023 (LRT, doi:10.1371/journal.pcbi.1011300); Weinreb 2020 (doi:10.1126/science.aaw3381); Wilson 2022, CAR-T (doi:10.1158/2159-8290.CD-21-1508); Fu 2025 (Clonotrace, preprint, doi:10.1101/2025.09.01.673503); Guryleva 2026 (PhyloTrajectory, preprint, doi:10.64898/2026.06.29.735205) |
| Shuffling clone labels as a null, including inside strata | Zheng 2022 (within-patient shuffle, Bio-protocol preprint, doi:10.21769/p1562); Swift 2023 (within lane and mutation status, doi:10.26508/lsa.202201792); Xie 2023 (cluster shuffle) |
| Trajectory methods return a trajectory whether or not one exists; negative controls for trajectory presence | Tenha and Song 2022 (doi:10.1371/journal.pcbi.1009829) |
| Timing and sample size distort apparent clone overlap | Cottrell 2021 (bulk TCR, doi:10.1136/jitc-2021-002642) |
| Cells of one clone are alike in expression, so clustering is a fair baseline | Wang and Ji 2023 (preprint, doi:10.1101/2023.11.27.568912) |
| Trajectory benchmarks rely on proxy labels, not lineage tracing | Saelens 2019 (doi:10.1038/s41587-019-0071-9; only the bioRxiv v1 text was read, so check the point against the journal version before citing it for this) |
| The dataset | Sheih 2020 (doi:10.1038/s41467-019-13880-1) |

So the claim is narrowed to what the search did not find: (1) a negative-control failure of a composite
trajectory verdict rule, and the choice to cap the verdict rather than retune it; Tenha and Song ran negative
controls on a presence statistic, not on a verdict; (2) on this dataset, the comparison of one clone score
against three shuffles (within patient, within pseudotime bin, within time point) plus a k-means baseline,
across three methods and four patients. The paper says these were not found by the search, not that they are
new: the search read mostly abstracts and a reviewer may know a paper it missed.

## Scope

- **Main text:** the verdict-rule failure and its diagnosis; the Sheih 2020 case study with per-patient values
  and bootstrap intervals.
- **Supplement (calibration evidence only):** the pancreas, bone marrow and gastrulation real-data runs
  (`real-2026-11-20.json`), the synthetic tree matrix, the clone-score calibration
  (`clonal-calibration-2026-11-13.json`, `clonal-calibration-n2-amended-2026-11-17.json`) and the verdict
  calibration (`verdict-calibration-2026-11-17.json`). They show how the checks behave; they carry no claim of
  their own.
- **Software:** lumencell is cited as archived software (PyPI 0.5.x, source github.com/shreyandhawa/lumenCell_V2,
  archive DOI to come). It is the instrument, not a contribution of the paper.
- **One disclosed deviation:** the rerun at the old commit `37197c8` counted supported controls with
  `hand_verdict` (a re-derivation from the rule text), because that commit's `verdict()` has no `verified`
  argument. `hand_verdict` equals the tool's verdict on all 67 recorded cases. This changed how the run was
  driven after the declaration, not a rule, threshold or seed.

## Glossary: private terms and the plain words the paper uses

The paper uses the right-hand column only. Internal names appear once, in Methods, where a reader needs them
to find the code.

| Term in the repo | Plain words in the paper |
|---|---|
| verdict | the tool's summary rating of a trajectory run (one of four levels below) |
| supported | the run passed every check the rule reads; as checked, this means "connected" |
| provisional | "not shown to be a tree": a run that would have been rated supported, shown with the cap because the rule failed its check |
| weak | the clone check failed: clones do not back these lineages |
| not_supported | too few cells got a pseudotime (under 95%) |
| C1-C5 | the rule's five criteria: C1 share of cells with a pseudotime; C2 how tree-like the cell clusters are; C3 lineage stability on rerun; C4 pseudotime stability on rerun; C5 the clone check |
| gate, gated | a pass/fail threshold fixed before a run (for example, pseudotime must correlate with known stage at 0.70 or more) |
| trust panel | the part of the tool's interface that shows a run's warnings and checks; not used in the paper |
| clone | cells in one patient that share the same paired T-cell-receptor chains |
| η (eta) | clone agreement score: how much more clone-pure the lineages are than under a shuffle of clone labels (1 minus observed clone entropy over the shuffled mean; 0 means no better than chance) |
| N1 | the clone shuffle within patient |
| N2 | the clone shuffle within patient and pseudotime bin (tenths of pseudotime) |
| N2a | the amended N2 in use since 2026-11-17: the pseudotime bins are also split where each lineage begins. In the paper this is simply "the shuffle within pseudotime bin"; the amendment is stated once in Methods |
| N3 | the clone shuffle within patient and time point |
| headline p | the largest p-value over the three shuffles |
| R | the ratio of the score against the time-point shuffle to the score against the within-patient shuffle |
| η_base, Δη | the same score for a k-means clustering of the cells with as many groups as lineages; the lift is the score minus that |
| matrix | the synthetic tree datasets (four tree shapes, several seeds) |
| negative controls (blob, two_groups, loop, sheet) | synthetic datasets with no tree: one cloud, two separate groups, a ring, a flat sheet |
| m = 2, m = 3 | clones of at least 2 cells (main), at least 3 (sensitivity check) |

## How the binding points check against the pages

Each point given for the paper was compared with the diagnosis pages and the result files. All hold. Three
need care in wording:

1. **"Adding the other three criteria drops the supported controls from 28 of 31 to 2."** True as written on
   the page, but the 2 is out of the 31 recorded controls, while the headline count is 27 of 30 on lumencell
   0.5.0. The paper gives the 2 (and 4 at the tree minimum) with "of the 31 recorded controls", and says the
   bars are the tree datasets' 10% quantile.
2. **"The verified rule reads coverage alone."** True of the 31-run check (no clones, so C5 does not apply). On
   Sheih, the same rule also reads the clone check (C5). The literature page's "reads coverage and clonal
   support" describes the case study, not the check (the verdict declaration, fact 1, says so).
3. **"Time structure does not explain the Sheih drop."** The page's result is narrower: time structure *of the
   kind simulated* (clones confined to time points, one synthetic family, one clone model) does not raise the
   within-patient score. The paper keeps "of this kind, in synthetic data".

Two pages carry wording the paper must not copy: `docs/results.md` ("What it does not show") says the score is
below half "against the time-point null or the pseudotime-depth null" in every run, but against the pseudotime
shuffle it is not (CLL-1 paga_dpt 0.695 to 0.363); the under-half result is for the time-point shuffle only. It
also gives the k-means result as a bare "at most 0.050" with no intervals. The literature page's suggested claim
uses 28 of 31, "in all 12 runs" with no qualifier, and "coverage and clonal support"; the claim above replaces it.
