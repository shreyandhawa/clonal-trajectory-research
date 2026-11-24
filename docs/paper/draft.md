<!--
Draft for review. Every result number is wrapped in an n-tag (format in tests/unit/test_paper_numbers.py) and is checked against the result
files by tests/unit/test_paper_numbers.py (keys are computed in src/ctr/paper_numbers.py). Times and commits in
section 2 come from docs/paper/preregistration.md and the raw GitHub records in docs/paper/evidence/.
Placeholders to fill: ORCID, funding, the two archive DOIs.
-->

# Testing two trust checks for single-cell trajectories: a coverage-based verdict on negative controls, and T-cell clone agreement in CAR-T data

Shreyan Dhawa, Independent researcher. ORCID: 0000-0000-0000-0000 [placeholder]

## Abstract

Trajectory inference methods return a trajectory whether or not the data hold one, so a tool that rates its own
output needs checks that can fail. I tested two such checks in the open-source tool lumencell, with the rules,
thresholds and nulls written down in a public repository before the data were scored, except where section 2
says otherwise. The first check is the
tool's summary verdict. As it was checked, the rule reads only whether at least 95% of cells get a pseudotime, and
on lumencell 0.5.0 it rated <!--n:verdict.r2-->27 of 30<!--/n--> negative-control runs "supported" (every blob, loop
and sheet run), although a tree measure that uses none of the rule's inputs separates all four control kinds from
the tree datasets. The second check scores how well T-cell receptor clones agree with the returned lineages. In one
public CAR-T dataset (Sheih et al. 2020: four patients, three methods, <!--n:clonal.n_runs-->12<!--/n--> runs), the
score against a clone shuffle within time point is under half its value against a shuffle within patient in the
point estimate of every run (ratio <!--n:clonal.R_range-->0.03 to 0.49<!--/n-->), with two bootstrap intervals
reaching <!--n:clonal.NHL-7/palantir.R_hi-->0.625<!--/n--> and <!--n:clonal.NHL-7/scfates_ppt.R_hi-->0.770<!--/n-->,
and a k-means clustering that uses no trajectory comes within <!--n:clonal.delta_abs_max-->0.05<!--/n--> of the
score in every run as a point estimate (the bootstrap interval of the difference is above zero in
<!--n:clonal.delta_ci_above-->4<!--/n--> runs and wholly below zero in <!--n:clonal.delta_ci_below-->3<!--/n-->). These are results about these checks on this data, one dataset and four patients, and not
about trajectory methods in general.

## 1. The claim

Trajectory inference orders single cells along a pseudotime and splits them into lineages, and the methods return
an answer even when the data have no trajectory in them [2]. A large benchmark of 45 methods scored them against labels
such as sampling origin or sorted cell types, not lineage tracing [1]. So a user of one of these methods has to decide
whether to trust the result, and a tool that helps with that decision is only useful if its checks fail when they
should. I wrote lumencell [17], a tool that runs three published methods (PAGA with diffusion pseudotime [15, U2],
Palantir [16] and scFates [U1]) and puts a set of checks next to each result. This paper asks whether two of those
checks hold up. The verdict rule failed the check declared for it. The clone check failed no declared check, but its
score is much smaller under a stricter shuffle, and a clustering with no trajectory matches most of it. lumencell is cited here as archived
software. It is the instrument for the study and not a contribution of the paper.

The claim has two parts, and I keep them separate. The first is that the verdict rule, as it was checked, looks
at one thing, whether at least 95% of cells get a pseudotime, so it rated <!--n:verdict.r2-->27 of 30<!--/n-->
negative-control runs "supported" on lumencell 0.5.0 even though an independent tree measure separates every control
kind from the tree datasets. The second is that in Sheih et al. 2020 [14], the agreement between T-cell receptor
clones and the returned lineages falls to under half when the clone shuffle is done within time point, in the point
estimate of every run though not in every bootstrap interval, and that a k-means clustering with no trajectory
matches most of it (the lineages' lift over it is above zero, by its interval, in only
<!--n:clonal.delta_ci_above-->4<!--/n--> of <!--n:clonal.n_runs-->12<!--/n--> runs).

Parts of this are already known, and I do not present them as new. T-cell clones and lineage barcodes have been used
to check or build trajectories before [4-9], including in CAR-T data [7]. Shuffling clone labels as a null, and doing
it inside strata, has been done before [5, 10, 11]. That methods return a trajectory when there is none, and that
negative controls can test a trajectory statistic, is shown by Tenha and Song [2, 3]. That timing and sample size
distort apparent clone overlap was shown in bulk TCR data [12], and that cells of one clone tend to share expression,
which makes clustering a fair baseline, was reported by Wang and Ji [13]. What my search did not find is a
negative-control failure of a composite verdict rule for trajectories, and on this dataset, a comparison of one
clone score against three shuffles plus a k-means baseline across three methods and four patients. I say "did not
find" because the search read mostly abstracts, and a reviewer may know a paper it missed.

The main text covers the verdict failure and the Sheih case study. The pancreas [U6], bone marrow [16] and
gastrulation [U4, U5] datasets and the synthetic tree matrix are calibration evidence only, and their results are in
the repository (`benchmarks/results/real-2026-11-20.json` and the calibration files), not claims of this paper.

## 2. What was declared in advance

With the exceptions stated below, every rule, threshold, seed, control and null used here was written into the
public repository before the data it governs were scored. I call this "declared in advance in the public repository, with commit timestamps". It is not
an entry in a public registry. The full timeline, with each declaration's commit and pull request, the GitHub server
times, and the first run that used it, is in `docs/paper/preregistration.md`, and the raw GitHub records behind it
are saved in `docs/paper/evidence/`.

The ordering is provable for the parts the main text leans on, with the limits below. The verdict rule, its
controls, its fresh verification seeds and its pass bar (no control run may be rated supported) were pushed to
GitHub on 2026-11-17 at 09:54 UTC, and the verification ran at a commit descending from that declaration about two
and a half hours later. The Sheih plan (clone definition, patient as the clone namespace, time point as the stratum
for the third null, the infusion product as the root, each patient run alone) was merged on 2026-11-20 at 08:15 UTC,
and the case-study numbers were made at a commit descending from it, first made public at 13:30 UTC. The two
diagnoses in sections 3 and 4 were declared in pull requests merged on 2026-11-23 at 17:01 UTC.

There are five things a reader should know about this record, and I state them here rather than only in the
supplement.

First, the timing of the two diagnosis runs rests on local file times. The result files of both diagnoses record
no run time and no commit. GitHub shows that the declarations were merged 21 and 27 minutes before the results were
pushed, but the only evidence that the runs started after the merge is the creation times of their log files on my
machine (from 17:01:41 UTC on), which a reader cannot check.

Second, one decision was made after a result was seen. After the verdict rule failed its verification on
2026-11-17, I ruled on 2026-11-19 (ruling H-1, pull request #38 in the lumencell repository) that under the cap only
a "supported" verdict is capped, so a failed clone check is shown as "weak" rather than capped to "not shown to be
a tree". This changes how verdicts are displayed, not any rule, threshold or null, but it was decided with the
failure in view.

Third, the Sheih data were opened before the Sheih declaration. A check on 2026-11-19 opened the TCR tables and the
expression matrix header to confirm that cell barcodes join between them. Its note records a freeze rule: only
headers, barcodes and counts were printed, and no clone, CDR3 or gene value was printed or tabulated. The derived
dataset was built after the declaration.

Fourth, the first calibration of the clone-score nulls (2026-11-13) ran on code that was not yet committed. The
result file says so itself. A later re-run of 40 of its 200 seeds on the committed code matched the p-values
exactly. This calibration is supplement material.

Fifth, for three declarations the order cannot be shown by anything a reader can check, because the declaration
reached GitHub together with its result or before GitHub's event log begins: the real-data gates (2026-11-10), the
rule for counting undefined p-values in that first calibration (2026-11-13), and the amended pseudotime null and
its calibration (2026-11-17). For these the record is the commit ancestry and the author's commit times only. Two of
the three carry no claim in the main text. The third does: the amended pseudotime shuffle is one of the three nulls
behind every Sheih run's headline p, and so behind the pass count and the pseudotime ratio in section 4.

## 3. The verdict rule failure and its diagnosis

### 3.1 The rule and its check

lumencell rates each run with one of four levels: "supported", "not shown to be a tree" (provisional), "weak" (the
clone check failed) and "not supported" (under 95% of cells got a pseudotime). The rule has five criteria: C1, the
share of cells with a pseudotime; C2, how tree-like the cell clusters are; C3 and C4, the stability of the lineages
and of the pseudotime when the method is rerun on subsamples; and C5, the clone check, which needs clone labels. C2
to C4 were to get thresholds from a calibration on synthetic trees against four kinds of synthetic negative control
(one structureless cloud, "blob"; two separate groups; a ring, "loop"; and a flat sheet), with the threshold halfway
between the trees' 10% quantile and the controls' 90% quantile. In that calibration none of C2, C3 and C4 separated
trees from controls, so by the declared rule none got a threshold and all three were left out. The verification on
fresh seeds 3 to 5 then had no clone labels, so C5 did not apply either, and the rule that was verified reads C1
alone.

The declared pass bar was that no control run be rated supported. The recorded verification (2026-11-17, at lumencell
commit `37197c8`) rated <!--n:verdict.recorded-->28 of 31<!--/n--> control runs supported, so the check failed.[^v1]
The rule was not changed to fix this. Instead every "supported" verdict the tool shows is capped at "not shown to be
a tree", which is why no run in this paper is shown as supported.

The headline count is <!--n:verdict.r2-->27 of 30<!--/n--> on lumencell 0.5.0, the pinned release anyone can install
(by kind: <!--n:verdict.r2_by_kind-->blob 9, loop 9, sheet 9, two_groups 0<!--/n-->). The other <!--n:verdict.r2_failed-->6<!--/n-->
of the 36 control runs are left out because the method refused a disconnected graph. The recorded <!--n:verdict.recorded-->28 of 31<!--/n--> does not
reproduce exactly even at its own commit, and the footnote says why.[^v2] Either count says the same thing: every
blob, loop and sheet run was rated supported.

### 3.2 Four explanations, tested as declared

I declared four explanations and a decision rule for each before running any check (`docs/paper/declaration-verdict-diagnosis.md`).
The declaration also says what I had already seen: the project notes already read the verdict as coverage alone,
so the tests for a bug and for a permissive rule confirm a reading that was known, while the tests for bad controls
and for a real property used measures I had not looked at.

A bug. I re-derived every recorded verdict from the rule text alone and compared it with both the recorded level and
the tool's own verdict function. They agree in <!--n:verdict.rederive-->67 of 67<!--/n--> cases, including five
worked by hand, so the explanation is refuted.

Bad controls, meaning the controls are trees after all. I measured each dataset with things the rule never reads:
connected components of the cell graph, an intrinsic dimension estimate (TwoNN [U3]), and the four-point condition
on graph distances, which is zero for a tree metric. For the last, I took 300 landmark cells in the largest
connected part, computed graph distances between them, and for 200,000 random quadruples took the gap between the
largest and middle of the three pair sums divided by the diameter, reporting its 99th percentile. On the four-point defect every control kind lies wholly outside the range
of the 24 tree datasets: trees <!--n:verdict.defect.trees-->0.099-0.168<!--/n-->, blob
<!--n:verdict.defect.blob-->0.293-0.327<!--/n-->, two groups <!--n:verdict.defect.two_groups-->0.280-0.387<!--/n-->,
sheet <!--n:verdict.defect.sheet-->0.280-0.297<!--/n-->, loop <!--n:verdict.defect.loop-->0.540-0.581<!--/n-->. The
intrinsic dimension was about 20 for everything, because count noise dominates it, as the declaration warned, so it
separated little. By the declared rule, each kind is separated from trees, and the explanation is refuted for all
four.

A permissive rule. C1 alone passes <!--n:verdict.c1_alone-->28 of 31<!--/n--> recorded controls, and the controls'
coverage is 1.0 against a bar of 0.95. Giving C2, C3 and C4 a bar taken from the trees alone (their 10% quantile, as the declaration fixed;
the calibrated threshold would also have used the controls' 90% quantile), they pass <!--n:verdict.c2_alone-->13 of 31<!--/n-->,
<!--n:verdict.c3_alone-->18 of 31<!--/n--> and <!--n:verdict.c4_alone-->7 of 31<!--/n--> controls one at a time, and
only <!--n:verdict.all_four_q10-->2 of 31<!--/n--> pass all four (<!--n:verdict.all_four_min-->4 of 31<!--/n--> at
the trees' minimum). These two counts are out of the 31 recorded controls, not the 30 of lumencell 0.5.0. So the
permissiveness comes from the criteria that were left out, not from C1's bar, and this explanation is supported.

A real property, meaning the methods return ordered, stable output on non-tree data, so connectivity cannot tell the
difference. The methods do order loop and sheet cells along the generator's own coordinate (median absolute
Spearman <!--n:verdict.rho.loop-->0.98<!--/n--> for loop and <!--n:verdict.rho.sheet-->0.93<!--/n--> for sheet, against
<!--n:verdict.rho.trees-->0.98<!--/n--> for trees). But the declared test also required most of those runs to fall
inside the trees' range on C1, C3 and C4, and they did not, mostly because pseudotime stability on loop runs is
higher than on any tree. So this explanation is not supported as declared.

### 3.3 What this shows

The failure is the rule. The controls are not trees by an independent measure, and a rule that reads only coverage
rates them supported, so "supported" from that rule means "connected" and nothing more. This does not show that C2
to C4 could never work, since they were non-discriminating on these six seeds only, and it says nothing about a
redesigned rule.

## 4. The Sheih 2020 case study

### 4.1 Data and scoring

Sheih et al. [14] profiled CD8 CAR-T cells from four patients (two with chronic lymphocytic leukaemia, CLL-1 and
CLL-2, and two with non-Hodgkin lymphoma, NHL-6 and NHL-7) at the infusion product and three later blood samples,
with paired T-cell receptor sequences (GEO GSE125881). A clone is the set of cells in one patient that share the
same paired receptor chains (one or two distinct TRA and one or two distinct TRB CDR3 nucleotide sequences), so the
same receptor in two patients is two clones. The GEO tables carry no productive-chain flag, so none was applied. Each patient was run alone with
each of the three methods, which gives 12 runs, rooted at the infusion product. The root is an assumption: the
paper treats the infusion product as the source of the later repertoire but names no trajectory root.

Only cells that sit in exactly one of a run's lineages and belong to a clone of at least two such cells are scored,
so each method is scored on its own cells. For each clone, H is the entropy of its cells over the lineages
(normalised by the log of the number of lineages), and H_obs is the mean of H over clones weighted by their cell
counts. The clone agreement score is η = 1 − H_obs / E[H], where E[H] is the mean of the same quantity under a
shuffle of clone labels. It is 0 when the lineages are no more clone-pure than chance. I report it against three
shuffles, all within patient. N1 shuffles across the whole patient. N2 shuffles within strata of pseudotime, made
by cutting pseudotime into tenths and cutting again at the pseudotime where each lineage begins (an amendment
calibrated before this study). N3 shuffles within time point, so clones that expand at one sample do not count as
lineage agreement. The headline p is the largest of the three p-values (1,000 shuffles each). A significant p
against N1 alone carries little information here: in the earlier calibration, N1 rejected in
<!--n:calib.depth_only_N1-->200 of 200<!--/n--> synthetic cases where clones followed pseudotime depth with no
lineage signal, and in the synthetic check of section 4.3 it over-rejected when clones were tied to time. The baseline is a k-means clustering of the cells into as many groups as
lineages, on the same principal components, with no trajectory, and the lift Δη is η against N1 minus the same
score for the k-means groups. A run passes the clone check when its headline p is at most 0.01 and Δη is above 0. Two cautions go with that
rule. Δη above 0 is a point condition, not a test (a paired permutation p for Δη is computed and reported in the
case study but is not part of the rule), and Δη is measured against N1. The 0.01 bar is per run, and with 1,000
shuffles the smallest possible p (0.000999) is above a Bonferroni bar of 0.01/12, and the runs are not independent,
so no family-wise claim is made.

The intervals are from a clone bootstrap, because the cells of one clone are not independent: for each run, its
clones are drawn with replacement 500 times, each replicate rescored with 100 shuffles per null, and the 2.5 and
97.5 percentiles reported. R is undefined in a replicate whose η against N1 is below 0.05, and such replicates are
left out of R's interval, which matters for the runs with small η against N1, such as NHL-7 palantir. They do not cover the method's own run-to-run variation, the k-means partition, or which
patients were sampled. The point values were recomputed on lumencell 0.5.0, and the largest difference from the recorded
case study in η against N1 is <!--n:clonal.max_drift-->0.000<!--/n--> at three decimals.

### 4.2 Results

| Run | Clones | η (N1) | η (N3) | R | Headline p | Δη | Pass |
|---|---|---|---|---|---|---|---|
| CLL-1 paga_dpt | <!--n:clonal.CLL-1/paga_dpt.clones-->652<!--/n--> | <!--n:clonal.CLL-1/paga_dpt.eta_N1-->0.695 [0.627, 0.755]<!--/n--> | <!--n:clonal.CLL-1/paga_dpt.eta_N3-->0.247 [0.183, 0.319]<!--/n--> | <!--n:clonal.CLL-1/paga_dpt.R-->0.355 [0.284, 0.433]<!--/n--> | <!--n:clonal.CLL-1/paga_dpt.p-->0.001<!--/n--> | <!--n:clonal.CLL-1/paga_dpt.delta-->0.036 [0.007, 0.067]<!--/n--> | <!--n:clonal.CLL-1/paga_dpt.pass-->pass<!--/n--> |
| CLL-1 palantir | <!--n:clonal.CLL-1/palantir.clones-->786<!--/n--> | <!--n:clonal.CLL-1/palantir.eta_N1-->0.125 [0.076, 0.172]<!--/n--> | <!--n:clonal.CLL-1/palantir.eta_N3-->0.020 [-0.008, 0.054]<!--/n--> | <!--n:clonal.CLL-1/palantir.R-->0.157 [-0.102, 0.360]<!--/n--> | <!--n:clonal.CLL-1/palantir.p-->0.076<!--/n--> | <!--n:clonal.CLL-1/palantir.delta-->-0.031 [-0.058, -0.004]<!--/n--> | <!--n:clonal.CLL-1/palantir.pass-->no<!--/n--> |
| CLL-1 scfates_ppt | <!--n:clonal.CLL-1/scfates_ppt.clones-->631<!--/n--> | <!--n:clonal.CLL-1/scfates_ppt.eta_N1-->0.571 [0.510, 0.630]<!--/n--> | <!--n:clonal.CLL-1/scfates_ppt.eta_N3-->0.073 [0.044, 0.107]<!--/n--> | <!--n:clonal.CLL-1/scfates_ppt.R-->0.129 [0.083, 0.176]<!--/n--> | <!--n:clonal.CLL-1/scfates_ppt.p-->0.001<!--/n--> | <!--n:clonal.CLL-1/scfates_ppt.delta-->-0.005 [-0.036, 0.026]<!--/n--> | <!--n:clonal.CLL-1/scfates_ppt.pass-->no<!--/n--> |
| CLL-2 paga_dpt | <!--n:clonal.CLL-2/paga_dpt.clones-->1271<!--/n--> | <!--n:clonal.CLL-2/paga_dpt.eta_N1-->0.213 [0.177, 0.248]<!--/n--> | <!--n:clonal.CLL-2/paga_dpt.eta_N3-->0.024 [0.007, 0.038]<!--/n--> | <!--n:clonal.CLL-2/paga_dpt.R-->0.112 [0.036, 0.173]<!--/n--> | <!--n:clonal.CLL-2/paga_dpt.p-->0.001<!--/n--> | <!--n:clonal.CLL-2/paga_dpt.delta-->0.024 [0.006, 0.042]<!--/n--> | <!--n:clonal.CLL-2/paga_dpt.pass-->pass<!--/n--> |
| CLL-2 palantir | <!--n:clonal.CLL-2/palantir.clones-->1177<!--/n--> | <!--n:clonal.CLL-2/palantir.eta_N1-->0.114 [0.079, 0.147]<!--/n--> | <!--n:clonal.CLL-2/palantir.eta_N3-->0.021 [-0.006, 0.048]<!--/n--> | <!--n:clonal.CLL-2/palantir.R-->0.185 [-0.075, 0.357]<!--/n--> | <!--n:clonal.CLL-2/palantir.p-->0.070<!--/n--> | <!--n:clonal.CLL-2/palantir.delta-->-0.011 [-0.040, 0.016]<!--/n--> | <!--n:clonal.CLL-2/palantir.pass-->no<!--/n--> |
| CLL-2 scfates_ppt | <!--n:clonal.CLL-2/scfates_ppt.clones-->968<!--/n--> | <!--n:clonal.CLL-2/scfates_ppt.eta_N1-->0.143 [0.104, 0.187]<!--/n--> | <!--n:clonal.CLL-2/scfates_ppt.eta_N3-->0.011 [-0.008, 0.032]<!--/n--> | <!--n:clonal.CLL-2/scfates_ppt.R-->0.075 [-0.067, 0.215]<!--/n--> | <!--n:clonal.CLL-2/scfates_ppt.p-->0.155<!--/n--> | <!--n:clonal.CLL-2/scfates_ppt.delta-->0.018 [-0.024, 0.054]<!--/n--> | <!--n:clonal.CLL-2/scfates_ppt.pass-->no<!--/n--> |
| NHL-6 paga_dpt | <!--n:clonal.NHL-6/paga_dpt.clones-->548<!--/n--> | <!--n:clonal.NHL-6/paga_dpt.eta_N1-->0.415 [0.351, 0.472]<!--/n--> | <!--n:clonal.NHL-6/paga_dpt.eta_N3-->0.089 [0.051, 0.123]<!--/n--> | <!--n:clonal.NHL-6/paga_dpt.R-->0.216 [0.133, 0.280]<!--/n--> | <!--n:clonal.NHL-6/paga_dpt.p-->0.001<!--/n--> | <!--n:clonal.NHL-6/paga_dpt.delta-->-0.008 [-0.023, 0.006]<!--/n--> | <!--n:clonal.NHL-6/paga_dpt.pass-->no<!--/n--> |
| NHL-6 palantir | <!--n:clonal.NHL-6/palantir.clones-->458<!--/n--> | <!--n:clonal.NHL-6/palantir.eta_N1-->0.138 [0.073, 0.207]<!--/n--> | <!--n:clonal.NHL-6/palantir.eta_N3-->0.031 [0.012, 0.053]<!--/n--> | <!--n:clonal.NHL-6/palantir.R-->0.228 [0.123, 0.350]<!--/n--> | <!--n:clonal.NHL-6/palantir.p-->0.001<!--/n--> | <!--n:clonal.NHL-6/palantir.delta-->-0.022 [-0.041, -0.007]<!--/n--> | <!--n:clonal.NHL-6/palantir.pass-->no<!--/n--> |
| NHL-6 scfates_ppt | <!--n:clonal.NHL-6/scfates_ppt.clones-->320<!--/n--> | <!--n:clonal.NHL-6/scfates_ppt.eta_N1-->0.313 [0.246, 0.391]<!--/n--> | <!--n:clonal.NHL-6/scfates_ppt.eta_N3-->0.011 [0.003, 0.022]<!--/n--> | <!--n:clonal.NHL-6/scfates_ppt.R-->0.034 [0.011, 0.062]<!--/n--> | <!--n:clonal.NHL-6/scfates_ppt.p-->0.026<!--/n--> | <!--n:clonal.NHL-6/scfates_ppt.delta-->-0.050 [-0.061, -0.037]<!--/n--> | <!--n:clonal.NHL-6/scfates_ppt.pass-->no<!--/n--> |
| NHL-7 paga_dpt | <!--n:clonal.NHL-7/paga_dpt.clones-->299<!--/n--> | <!--n:clonal.NHL-7/paga_dpt.eta_N1-->0.216 [0.171, 0.265]<!--/n--> | <!--n:clonal.NHL-7/paga_dpt.eta_N3-->0.009 [-0.000, 0.021]<!--/n--> | <!--n:clonal.NHL-7/paga_dpt.R-->0.043 [-0.001, 0.095]<!--/n--> | <!--n:clonal.NHL-7/paga_dpt.p-->0.015<!--/n--> | <!--n:clonal.NHL-7/paga_dpt.delta-->0.032 [0.002, 0.065]<!--/n--> | <!--n:clonal.NHL-7/paga_dpt.pass-->no<!--/n--> |
| NHL-7 palantir | <!--n:clonal.NHL-7/palantir.clones-->276<!--/n--> | <!--n:clonal.NHL-7/palantir.eta_N1-->0.064 [0.033, 0.093]<!--/n--> | <!--n:clonal.NHL-7/palantir.eta_N3-->0.028 [0.002, 0.050]<!--/n--> | <!--n:clonal.NHL-7/palantir.R-->0.439 [0.179, 0.625]<!--/n--> | <!--n:clonal.NHL-7/palantir.p-->0.005<!--/n--> | <!--n:clonal.NHL-7/palantir.delta-->0.010 [-0.002, 0.022]<!--/n--> | <!--n:clonal.NHL-7/palantir.pass-->pass<!--/n--> |
| NHL-7 scfates_ppt | <!--n:clonal.NHL-7/scfates_ppt.clones-->185<!--/n--> | <!--n:clonal.NHL-7/scfates_ppt.eta_N1-->0.070 [0.031, 0.112]<!--/n--> | <!--n:clonal.NHL-7/scfates_ppt.eta_N3-->0.034 [0.009, 0.068]<!--/n--> | <!--n:clonal.NHL-7/scfates_ppt.R-->0.491 [0.245, 0.770]<!--/n--> | <!--n:clonal.NHL-7/scfates_ppt.p-->0.001<!--/n--> | <!--n:clonal.NHL-7/scfates_ppt.delta-->0.049 [0.008, 0.088]<!--/n--> | <!--n:clonal.NHL-7/scfates_ppt.pass-->pass<!--/n--> |

Table 1. Per-run results.[^c1] Clones are clones of at least two scored cells. η values and the ratio R = η(N3) /
η(N1) are shown with 95% clone-bootstrap intervals. Δη is the lift over k-means. "Pass" means headline p at most
0.01 and Δη above 0.

The score against the time-point shuffle is under half its value against the within-patient shuffle in
<!--n:clonal.R_under_half-->12 of 12<!--/n--> point estimates, with ratios from <!--n:clonal.R_range-->0.03 to
0.49<!--/n-->. This does not hold for every interval. The two NHL-7 runs closest to half have intervals reaching
<!--n:clonal.NHL-7/palantir.R_hi-->0.625<!--/n--> (palantir) and <!--n:clonal.NHL-7/scfates_ppt.R_hi-->0.770<!--/n-->
(scfates_ppt), and <!--n:clonal.R_ci_includes_zero-->4<!--/n--> runs whose score against N3 is near zero have ratio
intervals that include zero. Against the pseudotime shuffle the score is not under half in every run (CLL-1 paga_dpt
keeps a ratio of <!--n:clonal.CLL-1/paga_dpt.R_N2-->0.52<!--/n-->), so the under-half result holds for the
time-point shuffle only, although the score also drops a lot against the pseudotime shuffle in some runs.

The k-means lift ranges from <!--n:clonal.delta_range-->-0.050 to +0.049<!--/n--> as point estimates, so the lineages
add at most <!--n:clonal.delta_abs_max-->0.05<!--/n--> over a clustering that uses no trajectory. The intervals are
wider. <!--n:clonal.delta_ci_above-->4<!--/n--> runs have an interval wholly above zero and
<!--n:clonal.delta_ci_below-->3<!--/n--> wholly below. <!--n:clonal.p_sig-->7 of 12<!--/n--> runs have a headline p
of at most 0.01, and <!--n:clonal.pass-->4 of 12<!--/n--> runs pass the clone check.

### 4.3 Testing a time confound

A natural reading is that clones tied to time points inflate the score against N1, and N3 removes that. I declared a
synthetic test of this before running it (`docs/paper/declaration-clonal-confound.md`). On <!--n:clonal.syn.n_seeds-->40<!--/n-->
synthetic trees I planted clones in four arms (no structure, clones confined to one time point only, real lineage
signal only, and both) and scored them with the true lineages and with PAGA's own output. With clones confined to
time points and no lineage signal, the median score against N1 with the true lineages was only
<!--n:clonal.syn.T1.eta_N1.0.1-->0.013<!--/n--> and <!--n:clonal.syn.T1.eta_N1.0.4-->0.005<!--/n--> at the two levels
of time noise (<!--n:clonal.syn.T1.eta_N1.paga_dpt.0.1-->0.026<!--/n--> and
<!--n:clonal.syn.T1.eta_N1.paga_dpt.0.4-->0.011<!--/n--> with PAGA's lineages), below the 0.05 the declared test
needed. N1's p-value did over-reject at the lower noise, in <!--n:clonal.syn.T1.rej_N1.oracle.0.1-->15<!--/n--> of 40
seeds with the true lineages and <!--n:clonal.syn.T1.rej_N1.paga_dpt.0.1-->18<!--/n--> with PAGA's, against a bound of
<!--n:clonal.syn.bound-->6<!--/n-->. With real lineage signal, the score against N3 kept its value (median ratio
<!--n:clonal.syn.T2.R.0.1-->1.00<!--/n-->), also when clones were tied to time (<!--n:clonal.syn.T3.R.0.1-->1.00<!--/n-->).
The declared outcome is that the time-only test <!--n:clonal.syn.D1-->fails<!--/n-->: time structure of this kind does
not inflate the score against N1 in synthetic data, so it does not explain the Sheih drop, and I do not call the
score confounded. What does explain the drop is an open question. One reading the
synthetic check does not rule out is that in Sheih the lineages themselves follow time point, because the root is
the infusion product and pseudotime runs from it, so a shuffle within time point may remove real lineage signal as
well as time structure. The synthetic check only shows that N3 keeps signal when lineage and time can be told apart.

### 4.4 What this shows

In four patients' CAR-T cells, the size of the clone agreement score falls to under half when the clones are
shuffled within time point rather than within patient, in the point estimate of every run, although
<!--n:clonal.p_sig-->7 of 12<!--/n--> runs keep a headline p of at most 0.01 with that shuffle included, and
expression clustering alone matches most of the score. I report
the time-point score with its interval as the headline, and I make no claim about any tree, direction of
differentiation or biology in these patients.

## 5. Limits

The verdict result does not show a tree anywhere, and it does not show that the left-out criteria could never work.
"Not shown to be a tree" is never support. The diagnosis used six seeds per control kind, a sampled four-point
statistic, and latent coordinates I chose and declared.

The case study is one dataset and four patients, two with CLL and two with NHL, blood only, and nothing here applies
beyond them. A second clonal dataset (Daniel et al. 2022 [U7], mouse LCMV) was considered and declined, because this
paper treats Sheih 2020 as a single case study. The declaration also gives reasons it could not have confirmed the
Sheih result: a different species and biology, a root that sits late in every method's pseudotime, only two time
points, and clone counts that had already been seen. Clones give no direction: shared clones say two states are related,
not which came first, so the direction comes from the assumed root at the infusion product, which is a cultured,
stimulated population. lumencell has no batch correction, so patients were never pooled for a headline result. Each
method scores its own cells, so the three methods are not compared like for like. The intervals leave out the
method's own variation and the k-means partition, and four patients cannot give a patient-level interval.

The synthetic check used one family of synthetic trees, one clone model and a time-point model I chose, and it
tests only two simple stories. Why the Sheih score falls under the time-point shuffle remains open.

The record of what was declared when has the limits listed in section 2.

## 6. Reproducibility

Code, declarations and every result file are in the repository github.com/shreyandhawa/clonal-trajectory-research
[18] (archived at DOI [placeholder]), and lumencell 0.5.0 is on PyPI and archived at DOI [placeholder]. `make
paper-numbers` prints every headline number from the saved result files, and `make paper-reproduce` re-runs both
diagnoses from the cached datasets and checks that each number comes out the same. On the author's machine every number
reproduced (the command prints the count). A test (`tests/unit/test_paper_numbers.py`) checks every number marked in this text against
the result files.

One deviation from the verdict-diagnosis declaration is disclosed: lumencell's verdict function at commit `37197c8`
has no argument for the verification cap, so the rerun at that commit counted supported controls with a
re-derivation from the rule text (`hand_verdict`), which matches the tool's own verdict in all 67 recorded cases.
This changed how that run was driven, not a rule, threshold or seed.

Data. Sheih et al. 2020: GEO GSE125881 (processed files only; NCBI places no restriction on their use, and the
article is CC BY 4.0). Human CD34+ bone marrow (Setty et al. 2019 [16]): figshare 14465559 (CC BY 4.0); the original
deposit is Human Cell Atlas project 091cf39b-01bc-42e5-9437-f419a66c8a45 (the project link in the paper no longer
resolves). Mouse gastrulation, erythroid lineage: Pijuan-Sala et al. 2019 [U4], ArrayExpress E-MTAB-6967; the file
used is figshare 14465562 (CC BY 4.0), which holds counts reprocessed by a later study [U5], and both are cited.
Mouse pancreas (Bastidas-Ponce et al. 2019 [U6]): GEO GSE132188; the processed file used, from the scvelo notebooks
repository, has no stated licence, so it is not redistributed here, and the code only downloads it from its host.
No data are redistributed by this repository; each file is downloaded from its host and checked against a recorded
SHA-256. Details: `docs/paper/data.md`.

Use of AI. I used an AI assistant (Claude, Anthropic) to write analysis code, run the checks, and draft and edit
this text, under my direction. I checked the numbers against the result files and I am responsible for all
content.

Competing interests. I wrote lumencell, the software whose checks are evaluated here.

Funding. [placeholder: state the funding, or that there was none]

## References

[1] Saelens W, Cannoodt R, Todorov H, Saeys Y. A comparison of single-cell trajectory inference methods. Nat Biotechnol 37(5):547-554, 2019. doi:10.1038/s41587-019-0071-9

[2] Tenha L, Song M. Inference of trajectory presence by tree dimension and subset specificity by subtree cover. PLoS Comput Biol 18(2):e1009829, 2022. doi:10.1371/journal.pcbi.1009829

[3] Tenha L, Song M. Statistical evidence for the presence of trajectory in single-cell data. BMC Bioinformatics 23(Suppl 8), 2022. doi:10.1186/s12859-022-04875-9

[4] Zhang L, et al. Lineage tracking reveals dynamic relationships of T cells in colorectal cancer. Nature 564(7735), 2018. doi:10.1038/s41586-018-0694-x

[5] Xie J, et al. LRT: Integrative analysis of scRNA-seq and scTCR-seq data to investigate clonal differentiation heterogeneity. PLoS Comput Biol 19(7), 2023. doi:10.1371/journal.pcbi.1011300

[6] Weinreb C, et al. Lineage tracing on transcriptional landscapes links state to fate during differentiation. Science 367(6479), 2020. doi:10.1126/science.aaw3381

[7] Wilson TL, et al. Common trajectories of highly effective CD19-specific CAR T cells identified by endogenous T-cell receptor lineages. Cancer Discov 12(9):2098-2119, 2022. doi:10.1158/2159-8290.CD-21-1508

[8] Fu Y, et al. Deciphering cell fate and clonal dynamics via integrative single-cell lineage modeling. bioRxiv, 2025 (preprint). doi:10.1101/2025.09.01.673503

[9] Guryleva M, et al. Inferring differentiation trajectories from T cell clonotype distributions. bioRxiv, 2026 (preprint). doi:10.64898/2026.06.29.735205

[10] Zheng L, Qin S, Hu X, Zhang Z. Indexes characterizing meta-clusters and STARTRAC analysis. Bio-protocol Preprint 1562, 2022. doi:10.21769/p1562

[11] Swift M, Horns F, Quake SR. Lineage tracing reveals fate bias and transcriptional memory in human B cells. Life Sci Alliance 6(3):e202201792, 2023. doi:10.26508/lsa.202201792

[12] Cottrell T, et al. Evaluating T-cell cross-reactivity between tumors and immune-related adverse events with TCR sequencing: pitfalls in interpretations of functional relevance. J Immunother Cancer 9(7), 2021. doi:10.1136/jitc-2021-002642

[13] Wang H, Ji Z. T cell transcriptional landscapes are shaped by TCR sequence similarity. bioRxiv, 2023 (preprint). doi:10.1101/2023.11.27.568912

[14] Sheih A, et al. Clonal kinetics and single-cell transcriptional profiling of CAR-T cells in patients undergoing CD19 CAR-T immunotherapy. Nat Commun 11:219, 2020. doi:10.1038/s41467-019-13880-1

[15] Wolf FA, et al. PAGA: graph abstraction reconciles clustering with trajectory inference through a topology preserving map of single cells. Genome Biol 20:59, 2019. doi:10.1186/s13059-019-1663-x

[16] Setty M, et al. Characterization of cell fate probabilities in single-cell data with Palantir. Nat Biotechnol 37(4):451-460, 2019. doi:10.1038/s41587-019-0068-4

[17] Dhawa S. lumencell, version 0.5.0 [software]. 2026. https://github.com/shreyandhawa/lumenCell_V2, archive DOI [placeholder]

[18] Dhawa S. clonal-trajectory-research [code and results]. 2026. https://github.com/shreyandhawa/clonal-trajectory-research, archive DOI [placeholder]

### References still to verify before submission

These are cited above but are not marked verified in `docs/paper/literature.md`. Check each title, author list and
DOI on a primary page before submitting.

[U1] Faure L, Soldatov R, Kharchenko PV, Adameyko I. scFates: a scalable python package for advanced pseudotime and bifurcation analysis from single-cell data. Bioinformatics 39(1), 2023. doi:10.1093/bioinformatics/btac746 (from memory; not checked)

[U2] Haghverdi L, et al. Diffusion pseudotime robustly reconstructs lineage branching. Nat Methods 13:845-848, 2016. doi:10.1038/nmeth.3971 (from memory; not checked; cite with [15] where diffusion pseudotime is named)

[U3] Facco E, d'Errico M, Rodriguez A, Laio A. Estimating the intrinsic dimension of datasets by a minimal neighborhood information. Sci Rep 7, 2017. doi:10.1038/s41598-017-11873-y (DOI from the declaration; title and authors from memory)

[U4] Pijuan-Sala B, et al. A single-cell molecular map of mouse gastrulation and early organogenesis. Nature 566:490-495, 2019. doi:10.1038/s41586-019-0933-9 (DOI confirmed only through the ArrayExpress record; title from memory)

[U5] The study behind figshare 14465562, bioRxiv doi:10.1101/2020.12.21.423773 ("Perspectives in RNA velocity" is the figshare collection's title; the paper's title and authors were not read)

[U6] Bastidas-Ponce A, et al. Comprehensive single cell mRNA profiling reveals a detailed roadmap for pancreatic endocrinogenesis. Development 146(12):dev173849, 2019 (title from memory; journal and number from the GEO record and the Development page)

[U7] Daniel et al. Nat Immunol 23:1614-1627, 2022. doi:10.1038/s41590-022-01337-5 (journal, pages and DOI from the repository's dataset registry; title and authors not checked)

[^v1]: `benchmarks/results/verdict-verification-2026-11-17.json` (controls_supported and records).
[^v2]: `benchmarks/results/diagnosis-verdict-2026-11-23.json`, `reproduce_at_37197c8` and `reproduce_on_0_5_0`. Rerun at `37197c8` with today's libraries, <!--n:verdict.r1_match-->69 of 72<!--/n--> records match the recorded file and the count is <!--n:verdict.r1-->31 of 34<!--/n-->, because three two-group scFates runs that raised an error in the record now complete. The library responsible was not identified. On 0.5.0 the two-group Palantir and scFates runs refuse a disconnected graph. All other section 3 numbers are from the same file (`rederive`, `criteria`, `structure`).
[^c1]: `benchmarks/results/diagnosis-clonal-2026-11-23.json`, `sheih_bootstrap` (point values and intervals) and `synthetic` (section 4.3); the recorded case study is `benchmarks/case_studies/results/sheih2020-2026-11-20.json`.
