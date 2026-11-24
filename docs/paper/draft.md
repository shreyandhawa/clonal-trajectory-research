<!--
Draft for review. Every result number is wrapped in an n-tag (format in tests/unit/test_paper_numbers.py) and is
checked against the result files by that test (keys are computed in src/ctr/paper_numbers.py). Times and commits
in section 2 come from docs/paper/declarations.md and the raw GitHub records in docs/paper/evidence/. Method detail
is in docs/paper/supplement.md (cited as S1-S5). Placeholders to fill: ORCID, funding, the two archive DOIs.
-->

# Testing two trust checks for single-cell trajectories: a coverage-based verdict on negative controls, and T-cell clone agreement in CAR-T data

Shreyan Dhawa, Independent researcher. ORCID: 0000-0000-0000-0000 [placeholder]

## Abstract

Trajectory inference methods return a trajectory whether or not the data hold one, so a tool that rates its own
output needs checks that can fail. I tested two such checks in the open-source tool lumencell, with the rules,
thresholds and nulls written down in a public repository before the data were scored, except where section 2
says otherwise. The first check is the tool's summary verdict. As it was checked, the rule reads only whether at
least 95% of cells get a pseudotime, and on lumencell 0.5.0 it rated <!--n:verdict.r2-->27 of 30<!--/n-->
negative-control runs "supported" (every blob, loop and sheet run), although a tree measure that uses none of the
rule's inputs separates all four control kinds from the tree datasets. The second check scores how well T-cell
receptor clones agree with the returned lineages. In one public CAR-T dataset (Sheih et al. 2020: four patients,
three methods, <!--n:clonal.n_runs-->12<!--/n--> runs), the score against a clone shuffle within time point is under
half its value against a shuffle within patient in the point estimate of every run (ratio
<!--n:clonal.R_range-->0.03 to 0.49<!--/n-->), with two bootstrap intervals reaching
<!--n:clonal.NHL-7/palantir.R_hi-->0.625<!--/n--> and <!--n:clonal.NHL-7/scfates_ppt.R_hi-->0.770<!--/n-->, and a
k-means clustering that uses no trajectory comes within <!--n:clonal.delta_abs_max-->0.05<!--/n--> of the score in
every run as a point estimate (the bootstrap interval of the difference is above zero in
<!--n:clonal.delta_ci_above-->4<!--/n--> runs and wholly below zero in <!--n:clonal.delta_ci_below-->3<!--/n-->).
These are results about these checks on this data, one dataset and four patients, and not about trajectory methods
in general.

## 1. The claim

Trajectory inference orders single cells along a pseudotime and splits them into lineages, and the methods return
an answer even when the data have no trajectory in them [2]. A large benchmark of 45 methods scored them against
labels such as sampling origin or sorted cell types, not lineage tracing [1]. So a user of these methods has to
decide whether to trust the result, and a tool that helps with that is only useful if its checks fail when they
should. I wrote lumencell [17], a tool that runs three published methods (PAGA with diffusion pseudotime [15, 20],
Palantir [16] and scFates [19]) and puts a set of checks next to each result. lumencell is cited as archived
software. It is the instrument for this study and not a contribution of the paper. This paper asks whether two of
its checks hold up, and the claim has two parts that I keep separate, as stated in the abstract. The verdict rule
failed the check declared for it. The clone check failed no declared check, but in Sheih et al. 2020 [14] its score
is under half its size under a shuffle within time point, in the point estimate of every run though not in every
interval, and a clustering with no trajectory matches most of it.

Parts of this are already known, and I do not present them as new. T-cell clones and lineage barcodes have been
used to check or build trajectories before [4-9], including in CAR-T data [7]. Shuffling clone labels as a null,
and doing it inside strata, has been done before [5, 10, 11]. That methods return a trajectory when there is none,
and that negative controls can test a trajectory statistic, is shown by Tenha and Song [2, 3]. That timing and
sample size distort apparent clone overlap was shown in bulk TCR data [12], and that cells of one clone tend to
share expression, which makes clustering a fair baseline, was reported by Wang and Ji [13]. What my search did not
find is a negative-control failure of a composite verdict rule for trajectories, and on this dataset, a comparison
of one clone score against three shuffles plus a k-means baseline across three methods and four patients. I say
"did not find" because the search read mostly abstracts, and a reviewer may know a paper it missed.

The main text covers the verdict failure and the Sheih case study. The pancreas [24], bone marrow [16] and
gastrulation [22, 23] datasets and the synthetic tree matrix are calibration evidence only (S5).

## 2. What was declared in advance

With the exceptions stated below, every rule, threshold, seed, control and null used here was written into the
public repository before the data it governs were scored. I call this "declared in advance in the public
repository, with commit timestamps". It is not an entry in a public registry. The timeline, with commits, pull requests and GitHub's
server times, is in `docs/paper/declarations.md`, with the raw GitHub records in `docs/paper/evidence/`. For the
verdict rule (public about two and a half hours before its verification ran) and the Sheih plan (merged five hours
before its numbers were made public) the order is provable from GitHub's own times.

There are five things a reader should know about this record, and I state them here rather than only in the
supplement.

First, the timing of the two diagnosis runs rests on local file times. The result files of both diagnoses record
no run time and no commit. GitHub shows that the declarations were merged 21 and 27 minutes before the results were
pushed, but the only evidence that the runs started after the merge is the creation times of their log files on my
machine (from 17:01:41 UTC on), which a reader cannot check.

Second, one decision was made after a result was seen. After the verdict rule failed its verification on
2026-11-17, I ruled on 2026-11-19 (ruling H-1, pull request #38 in the lumencell repository) that under the cap
only a "supported" verdict is capped, so a failed clone check is shown as "weak" rather than capped to "not shown to
be a tree". This changes how verdicts are displayed, not any rule, threshold or null, but it was decided with the
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
rule for counting undefined p-values in that first calibration (2026-11-13), and the amended pseudotime null and its
calibration (2026-11-17). For these the record is the commit ancestry and the author's commit times only. Two of
the three carry no claim in the main text. The third does: the amended pseudotime shuffle is one of the three nulls
behind every Sheih run's headline p, and so behind the pass count and the pseudotime ratio in section 4.

## 3. The verdict rule failure and its diagnosis

### 3.1 The rule and its check

lumencell rates each run "supported", "not shown to be a tree", "weak" (the clone check failed) or "not supported"
(under 95% of cells got a pseudotime). The rule has five criteria: C1, the share of cells with a pseudotime; C2,
how tree-like the cell clusters are; C3 and C4, the stability of the lineages and of the pseudotime on rerun; and
C5, the clone check. C2 to C4 were to get thresholds from a calibration on synthetic trees against four kinds of
synthetic negative control (a structureless cloud, two separate groups, a ring and a flat sheet). None of the three
separated trees from controls in that calibration, so by the declared rule none got a threshold and all were left
out (S1). The verification on fresh seeds had no clone labels, so C5 did not apply, and the rule that was verified
reads C1 alone.

The declared pass bar was that no control run be rated supported. The recorded verification (2026-11-17, at
lumencell commit `37197c8`) rated <!--n:verdict.recorded-->28 of 31<!--/n--> control runs supported, so the check
failed.[^v1] The rule was not changed to fix this. Instead every "supported" verdict the tool shows is capped at
"not shown to be a tree", which is why no run in this paper is shown as supported.

The headline count is <!--n:verdict.r2-->27 of 30<!--/n--> on lumencell 0.5.0, the pinned release anyone can
install (by kind: <!--n:verdict.r2_by_kind-->blob 9, loop 9, sheet 9, two_groups 0<!--/n-->). The other
<!--n:verdict.r2_failed-->6<!--/n--> of the 36 control runs are left out because the method refused a disconnected
graph. The recorded <!--n:verdict.recorded-->28 of 31<!--/n--> does not reproduce exactly even at its own commit,
and the footnote says why.[^v2] Either count says the same thing: every blob, loop and sheet run was rated
supported.

### 3.2 Four explanations, tested as declared

I declared four explanations and a decision rule for each before running any check
(`docs/paper/declaration-verdict-diagnosis.md`). The declaration also says what I had already seen: the project
notes already read the verdict as coverage alone, so the tests for a bug and for a permissive rule confirm a
reading that was known, while the tests for bad controls and for a real property used measures I had not looked at.

A bug. I re-derived every recorded verdict from the rule text alone. It agrees with both the recorded level and the
tool's own verdict function in <!--n:verdict.rederive-->67 of 67<!--/n--> cases, so the explanation is refuted.

Bad controls, meaning the controls are trees after all. I measured each dataset with things the rule never reads:
connected components of the cell graph, an intrinsic dimension estimate (TwoNN [21]) and the four-point condition
on graph distances, which is zero for a tree metric (S2). On the four-point defect every control kind lies wholly
outside the range of the 24 tree datasets: trees <!--n:verdict.defect.trees-->0.099-0.168<!--/n-->, blob
<!--n:verdict.defect.blob-->0.293-0.327<!--/n-->, two groups <!--n:verdict.defect.two_groups-->0.280-0.387<!--/n-->,
sheet <!--n:verdict.defect.sheet-->0.280-0.297<!--/n-->, loop <!--n:verdict.defect.loop-->0.540-0.581<!--/n-->. By the
declared rule each kind is separated from trees, and the explanation is refuted for all four.

A permissive rule. C1 alone passes <!--n:verdict.c1_alone-->28 of 31<!--/n--> recorded controls. With C2, C3 and C4
given a bar from the trees alone (their 10% quantile), only <!--n:verdict.all_four_q10-->2 of 31<!--/n--> pass all
four (<!--n:verdict.all_four_min-->4 of 31<!--/n--> at the trees' minimum). These counts are out of the 31 recorded
controls, not the 30 of lumencell 0.5.0. The permissiveness comes from the criteria that were left out, not from
C1's bar, so this explanation is supported (S1 gives each criterion alone).

A real property, meaning the methods return ordered, stable output on non-tree data. The methods do order loop and
sheet cells along the generator's own coordinate (median absolute Spearman <!--n:verdict.rho.loop-->0.98<!--/n--> for
loop and <!--n:verdict.rho.sheet-->0.93<!--/n--> for sheet, against <!--n:verdict.rho.trees-->0.98<!--/n--> for
trees), but the declared test also required most of those runs to fall inside the trees' range on C1, C3 and C4,
and they did not. So this explanation is not supported as declared.

The failure is the rule: "supported" from a rule that reads only coverage means "connected" and nothing more. This does not show that C2
to C4 could never work, since they were non-discriminating on these six seeds only, and it says nothing about a
redesigned rule.

## 4. The Sheih 2020 case study

### 4.1 Data and scoring

Sheih et al. [14] profiled CD8 CAR-T cells from four patients (CLL-1 and CLL-2 with chronic lymphocytic leukaemia,
NHL-6 and NHL-7 with non-Hodgkin lymphoma) at the infusion product and three later blood samples, with paired
T-cell receptor sequences. A clone is the set of cells in one patient that share the same paired receptor chains, so
the same receptor in two patients is two clones (S3). Each patient was run alone with each of the three methods,
which gives 12 runs, rooted at the infusion product. The root is an assumption: the paper treats the infusion
product as the source of the later repertoire but names no trajectory root.

The clone agreement score is η = 1 − H_obs / E[H], where H_obs is the mean entropy of each clone's cells over the
lineages and E[H] is its mean under a shuffle of clone labels, so η is 0 when the lineages are no more clone-pure
than chance. Only cells in exactly one lineage are scored, so each method is scored on its own cells (S3). I report
η against three shuffles, all within patient: N1 across the whole patient, N2 within strata of pseudotime, and N3
within time point, so clones that expand at one sample do not count as lineage agreement. The headline p is the
largest of the three p-values. A significant p against N1 alone carries little information here: in the earlier
calibration, N1 rejected in <!--n:calib.depth_only_N1-->200 of 200<!--/n--> synthetic cases where clones followed
pseudotime depth with no lineage signal. The baseline is a k-means clustering into as many groups as lineages, with
no trajectory, and the lift Δη is η against N1 minus the same score for the k-means groups. A run passes the clone
check when its headline p is at most 0.01 and Δη is above 0. Intervals are from a clone bootstrap with 500
replicates, because the cells of one clone are not independent (S3).

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

The k-means lift ranges from <!--n:clonal.delta_range-->-0.050 to +0.049<!--/n--> as point estimates, so the
lineages add at most <!--n:clonal.delta_abs_max-->0.05<!--/n--> over a clustering that uses no trajectory. The
intervals are wider. <!--n:clonal.delta_ci_above-->4<!--/n--> runs have an interval wholly above zero and
<!--n:clonal.delta_ci_below-->3<!--/n--> wholly below. <!--n:clonal.p_sig-->7 of 12<!--/n--> runs have a headline p
of at most 0.01, and <!--n:clonal.pass-->4 of 12<!--/n--> runs pass the clone check.

### 4.3 Testing a time confound

A natural reading is that clones tied to time points inflate the score against N1. I declared a synthetic test of
this before running it (`docs/paper/declaration-clonal-confound.md`, details in S4). On
<!--n:clonal.syn.n_seeds-->40<!--/n--> synthetic trees with clones confined to time points and no lineage signal,
the median score against N1 with the true lineages was only <!--n:clonal.syn.T1.eta_N1.0.1-->0.013<!--/n--> and
<!--n:clonal.syn.T1.eta_N1.0.4-->0.005<!--/n--> at two levels of time noise, below the 0.05 the declared test
needed, although N1's p-value over-rejected. With real lineage signal, the score against N3 kept its value (median
ratio <!--n:clonal.syn.T2.R.0.1-->1.00<!--/n-->), also when clones were tied to time
(<!--n:clonal.syn.T3.R.0.1-->1.00<!--/n-->). The declared outcome is that the time-only test
<!--n:clonal.syn.D1-->fails<!--/n-->: time structure of this kind does not inflate the score against N1 in synthetic
data, so it does not explain the Sheih drop, and I do not call the score confounded. What does explain the drop is
an open question. One reading the synthetic check does not rule out is that in Sheih the lineages themselves follow
time point, because the root is the infusion product and pseudotime runs from it, so a shuffle within time point
may remove real lineage signal as well as time structure. The synthetic check only shows that N3 keeps signal when
lineage and time can be told apart.

So I report the time-point score with its interval as the headline, note that <!--n:clonal.p_sig-->7 of 12<!--/n-->
runs keep a headline p of at most 0.01 with that shuffle included, and make no claim about any tree, direction of
differentiation or biology in these patients.

## 5. Limits

The verdict result does not show a tree anywhere, and it does not show that the left-out criteria could never work.
"Not shown to be a tree" is never support. The diagnosis used six seeds per control kind, a sampled four-point
statistic, and latent coordinates I chose and declared.

The case study is one dataset and four patients, two with CLL and two with NHL, blood only, and nothing here
applies beyond them. A second clonal dataset (Daniel et al. 2022 [25], mouse LCMV) was considered and declined,
because this paper treats Sheih 2020 as a single case study. The declaration also gives reasons it could not have
confirmed the Sheih result: a different species and biology, a root that sits late in every method's pseudotime,
only two time points, and clone counts that had already been seen. Clones give no direction: shared clones say two
states are related, not which came first, so the direction comes from the assumed root at the infusion product,
which is a cultured, stimulated population. lumencell has no batch correction, so patients were never pooled for a
headline result. Each method scores its own cells, so the three methods are not compared like for like. The GEO clone tables carry
no productive-chain flag, so none was applied, and whether the authors kept only productive chains is not stated.

The intervals leave out the method's own run-to-run variation and the k-means partition, and four patients cannot
give a patient-level interval. The ratio is undefined in a bootstrap replicate whose score against N1 is below
0.05, and those replicates are left out of its interval, which matters for runs with a small score against N1 such
as NHL-7 palantir. The pass rule's Δη above 0 is a point condition, not a test, and Δη is measured against N1. The
0.01 bar is per run, the smallest possible p with 1,000 shuffles (0.000999) is above a Bonferroni bar of 0.01/12,
and the runs are not independent, so no family-wise claim is made.

The synthetic check used one family of synthetic trees, one clone model and a time-point model I chose, and it
tests only two simple stories. Why the Sheih score falls under the time-point shuffle remains open.

The record of what was declared when has the limits listed in section 2.

## 6. Reproducibility

Code, declarations and every result file are in the repository github.com/shreyandhawa/clonal-trajectory-research
[18] (archived at DOI [placeholder]), and lumencell 0.5.0 is on PyPI and archived at DOI [placeholder]. `make
paper-numbers` prints every headline number from the saved result files, and `make paper-reproduce` re-runs both
diagnoses from the cached datasets and checks that each number comes out the same. On the author's machine every
number reproduced (the command prints the count). A test (`tests/unit/test_paper_numbers.py`) checks every number
marked in this text and in the supplement against the result files.

One deviation from the verdict-diagnosis declaration is disclosed: lumencell's verdict function at commit `37197c8`
has no argument for the verification cap, so the rerun at that commit counted supported controls with a
re-derivation from the rule text (`hand_verdict`), which matches the tool's own verdict in all 67 recorded cases.
This changed how that run was driven, not a rule, threshold or seed.

Data. Sheih et al. 2020 [14]: GEO GSE125881, processed files only. NCBI places no restriction on their use, and the
article is CC BY 4.0. Human CD34+ bone marrow (Setty et al. 2019 [16]): figshare 14465559 (CC BY 4.0), originally
deposited as Human Cell Atlas project 091cf39b-01bc-42e5-9437-f419a66c8a45 (the project link in the paper no longer
resolves). Mouse gastrulation, erythroid lineage: Pijuan-Sala et al. 2019 [22], ArrayExpress E-MTAB-6967, with the
file used from figshare 14465562 (CC BY 4.0), which holds counts reprocessed by Barile et al. [23]; both are cited.
Mouse pancreas (Bastidas-Ponce et al. 2019 [24]): GEO GSE132188. The processed file used, from the scvelo notebooks
repository, has no stated licence, so it is not redistributed here, and the code only downloads it from its host.
No data are redistributed by this repository. Each file is downloaded from its host and checked against a recorded
SHA-256 (details in `docs/paper/data.md`).

Use of AI. I used an AI assistant (Claude, Anthropic) to write analysis code, run the checks, and draft and edit
this text, under my direction. I checked the numbers against the result files and I am responsible for all content.

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

[19] Faure L, Soldatov R, Kharchenko PV, Adameyko I. scFates: a scalable python package for advanced pseudotime and bifurcation analysis from single-cell data. Bioinformatics 39(1):btac746, 2023. doi:10.1093/bioinformatics/btac746

[20] Haghverdi L, Büttner M, Wolf FA, Buettner F, Theis FJ. Diffusion pseudotime robustly reconstructs lineage branching. Nat Methods 13(10):845-848, 2016. doi:10.1038/nmeth.3971

[21] Facco E, d'Errico M, Rodriguez A, Laio A. Estimating the intrinsic dimension of datasets by a minimal neighborhood information. Sci Rep 7:12140, 2017. doi:10.1038/s41598-017-11873-y

[22] Pijuan-Sala B, Griffiths JA, Guibentif C, et al. A single-cell molecular map of mouse gastrulation and early organogenesis. Nature 566(7745):490-495, 2019. doi:10.1038/s41586-019-0933-9

[23] Barile M, Imaz-Rosshandler I, Inzani I, et al. Coordinated changes in gene expression kinetics underlie both mouse and human erythroid maturation. bioRxiv, 2020 (preprint). doi:10.1101/2020.12.21.423773

[24] Bastidas-Ponce A, Tritschler S, Dony L, et al. Comprehensive single cell mRNA profiling reveals a detailed roadmap for pancreatic endocrinogenesis. Development 146(12):dev173849, 2019. doi:10.1242/dev.173849

[25] Daniel B, Yost KE, Hsiung S, et al. Divergent clonal differentiation trajectories of T cell exhaustion. Nat Immunol 23(11):1614-1627, 2022. doi:10.1038/s41590-022-01337-5

How the references were checked. [1]-[16] are in the literature check (`docs/paper/literature.md`), where each was
opened at a primary or indexing page. [19]-[25] were checked on the Crossref API on 2026-11-24 for title, authors,
year, venue and DOI. Still to confirm: whether [23] has a journal version (Crossref records none), and that the
figshare file behind [23] was made from E-MTAB-6967 (the figshare record cites [23] but does not say).

[^v1]: `benchmarks/results/verdict-verification-2026-11-17.json` (controls_supported and records).
[^v2]: `benchmarks/results/diagnosis-verdict-2026-11-23.json`, `reproduce_at_37197c8` and `reproduce_on_0_5_0`. Rerun at `37197c8` with today's libraries, <!--n:verdict.r1_match-->69 of 72<!--/n--> records match the recorded file and the count is <!--n:verdict.r1-->31 of 34<!--/n-->, because three two-group scFates runs that raised an error in the record now complete. The library responsible was not identified. On 0.5.0 the two-group Palantir and scFates runs refuse a disconnected graph. All other section 3 numbers are from the same file (`rederive`, `criteria`, `structure`).
[^c1]: `benchmarks/results/diagnosis-clonal-2026-11-23.json`, `sheih_bootstrap` (point values and intervals) and `synthetic` (section 4.3), and `benchmarks/results/clonal-calibration-2026-11-13.json` (the N1 calibration count); the recorded case study is `benchmarks/case_studies/results/sheih2020-2026-11-20.json`.
