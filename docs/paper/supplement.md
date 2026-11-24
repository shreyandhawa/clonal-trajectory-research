<!--
Supplement to draft.md. Numbers are wrapped in n-tags and checked by tests/unit/test_paper_numbers.py, as in the
draft. Reference numbers refer to the draft's reference list.
-->

# Supplementary material

## S1. The verdict rule and its calibration

lumencell's four levels are "supported" (every criterion that is read passes), "not shown to be a tree" (shown in
place of supported while the rule's verification has failed), "weak" (the clone check, C5, failed) and "not
supported" (C1 failed: under 95% of cells got a pseudotime). C2 is the PAGA tree-likeness of the cell clusters, C3
the agreement of lineages between the reference run and subsample reruns, and C4 the same for pseudotime. C5 passes
when the headline clone p is at most 0.01 and Δη is above 0.

The calibration rule (`benchmarks/thresholds.toml`, `[tree_support.calibration]`) set each threshold halfway between
the trees' 10% quantile and the controls' 90% quantile, and left a criterion out if the trees' quantile was not above
the controls'. C2 had also to discriminate at Leiden resolution x0.5, x1 and x2. On seeds 0-2 none of C2, C3 and C4
did, so no threshold was set. The verification used fresh seeds 3-5, four tree topologies and four control kinds,
three methods each, with the pass bar `max_controls_supported = 0`.

In the diagnosis (explanation c), each left-out criterion was given a bar from the trees alone, their 10% quantile,
as the diagnosis declaration fixed. This is not the calibrated threshold, which would also have used the controls'
90% quantile. One at a time, at that bar, C1 passes <!--n:verdict.c1_alone-->28 of 31<!--/n--> recorded controls, C2
<!--n:verdict.c2_alone-->13 of 31<!--/n-->, C3 <!--n:verdict.c3_alone-->18 of 31<!--/n--> and C4
<!--n:verdict.c4_alone-->7 of 31<!--/n-->. All four together pass <!--n:verdict.all_four_q10-->2 of 31<!--/n-->
(<!--n:verdict.all_four_min-->4 of 31<!--/n--> at the trees' minimum). Every control that C1 passes has coverage 1.0
against the bar of 0.95.

The bug test re-derived all <!--n:verdict.n_verdicts-->67<!--/n--> recorded verdicts mechanically from the rule text
and also worked five by hand (`docs/paper/diagnosis-verdict.md`).

## S2. Measures of tree structure that the rule does not read

All on the 30 principal components the cell graph uses, for every verification and calibration dataset (24 controls,
24 trees).

- Connected components of the kNN graph. The two-group controls have two; every tree has one.
- Intrinsic dimension by TwoNN [21]. It was about 20 for every dataset, because count noise dominates it, as the
  declaration warned, so it separated only the blob controls and, narrowly, the two-group controls.
- Four-point defect. 300 landmark cells drawn in the largest connected part, graph distances between them, and for
  200,000 random landmark quadruples the gap between the largest and middle of the three pair sums divided by the
  diameter. The statistic is the 99th percentile, and it is 0 for a tree metric. Ranges: trees
  <!--n:verdict.defect.trees-->0.099-0.168<!--/n-->, blob <!--n:verdict.defect.blob-->0.293-0.327<!--/n-->, two groups
  <!--n:verdict.defect.two_groups-->0.280-0.387<!--/n-->, sheet <!--n:verdict.defect.sheet-->0.280-0.297<!--/n-->, loop
  <!--n:verdict.defect.loop-->0.540-0.581<!--/n-->.

For explanation (d), the latent coordinate was the angular distance from the root for the loop, the distance from
the root corner for the sheet, and the true pseudotime for trees (median absolute Spearman
<!--n:verdict.rho.loop-->0.98<!--/n-->, <!--n:verdict.rho.sheet-->0.93<!--/n--> and <!--n:verdict.rho.trees-->0.98<!--/n-->).
The declared test also needed at least half of the loop and sheet runs inside the trees' range on C1, C3 and C4, and
the pseudotime stability of loop runs mostly lies above any tree's, which the "inside the range" wording counts as
outside.

## S3. Clone scoring and the clone bootstrap

Clones. A cell's clone is the sorted set of its one or two distinct TRA and one or two distinct TRB CDR3 nucleotide
sequences, keyed by patient. A cell with only one chain detected, or with more than two distinct CDR3s on a chain,
gets no clone label. The GEO tables carry no productive, high-confidence or full-length flag, so no filter was
applied.

Scored cells. Only cells whose whole lineage weight is on one lineage are scored, and only clones with at least two
such cells (m = 2; m = 3 is a sensitivity check reported in the case study). For a clone k with cells spread over L
lineages in shares p_kl, H_k = -sum_l p_kl log p_kl / log L, and H is the mean of H_k weighted by the clone's scored
cells. η = 1 − H_obs / E[H], with E[H] the mean of H over 1,000 shuffles of clone labels.

Nulls. N1 shuffles clone labels among a patient's scored cells. N2 shuffles within patient and within strata of
pseudotime: tenths of the scored cells' pseudotime, cut again at each lineage's onset (the smallest pseudotime among
cells wholly on that lineage). This onset cut is the amendment of 2026-11-17, adopted after the original decile
version failed a depth control in calibration. N3 shuffles within patient and time point. The headline p is the
largest of the three one-sided p-values. In calibration, N1 rejected in <!--n:calib.depth_only_N1-->200 of 200<!--/n-->
cases where clones followed pseudotime depth with no lineage signal, as that control was built to show.

Baseline. k-means (`scipy.cluster.vq.kmeans2`, seeded) with as many groups as the run has lineages, on the same
principal components, scored on the same cells. Δη = η(N1) − η(k-means), with a paired permutation p over the same
N1 shuffles, which is reported in the case study but is not part of the pass rule.

Clone bootstrap. For each run, its scored clones are drawn with replacement as many times as there are clones, each
draw keeping all of that clone's scored cells under a new clone id, 500 replicates, each rescored with 100 shuffles
per null, with the run's lineages, pseudotime, strata and k-means groups held fixed. The interval is the 2.5 and
97.5 percentiles. R is computed only in replicates with η(N1) of at least 0.05. The point values were recomputed on
lumencell 0.5.0; the largest difference from the recorded case study in η against N1 is
<!--n:clonal.max_drift-->0.000<!--/n--> at three decimals.

## S4. Synthetic check of a time confound

Declared in `docs/paper/declaration-clonal-confound.md`. Seeds 600-639 (<!--n:clonal.syn.n_seeds-->40<!--/n-->),
three branching topologies, one donor, four time points made from noisy quartiles of the true pseudotime at two
noise levels (0.1 and 0.4). Clones were planted in four arms: no structure, clones confined to one time point with
no lineage signal (T1), lineage signal only (T2), and both (T3). Scored with the true lineages (oracle) and with
PAGA's own output.

With time-only clones (T1), the median η against N1 was <!--n:clonal.syn.T1.eta_N1.0.1-->0.013<!--/n--> and
<!--n:clonal.syn.T1.eta_N1.0.4-->0.005<!--/n--> with the true lineages at the two noise levels, and
<!--n:clonal.syn.T1.eta_N1.paga_dpt.0.1-->0.026<!--/n--> and <!--n:clonal.syn.T1.eta_N1.paga_dpt.0.4-->0.011<!--/n-->
with PAGA's lineages. The declared test needed at least 0.05. N1's p-value over-rejected at the lower noise, in
<!--n:clonal.syn.T1.rej_N1.oracle.0.1-->15<!--/n--> of 40 seeds with the true lineages and
<!--n:clonal.syn.T1.rej_N1.paga_dpt.0.1-->18<!--/n--> with PAGA's, against a bound of <!--n:clonal.syn.bound-->6<!--/n-->
(at the higher noise, <!--n:clonal.syn.T1.rej_N1.oracle.0.4-->6<!--/n--> and
<!--n:clonal.syn.T1.rej_N1.paga_dpt.0.4-->10<!--/n-->). With lineage signal, the median ratio η(N3)/η(N1) was
<!--n:clonal.syn.T2.R.0.1-->1.00<!--/n--> (T2) and <!--n:clonal.syn.T3.R.0.1-->1.00<!--/n--> (T3) at the lower noise,
and <!--n:clonal.syn.T2.R.0.4-->1.00<!--/n--> and <!--n:clonal.syn.T3.R.0.4-->1.00<!--/n--> at the higher. The
declared outcome is that the time-only test <!--n:clonal.syn.D1-->fails<!--/n--> at both noise levels and in both
modes. The full table is in `docs/paper/diagnosis-clonal.md`.

## S5. Calibration evidence on other data

These datasets show how the checks behave and carry no claim of the paper. Results: `benchmarks/results/real-2026-11-10.json`,
`real-2026-11-13.json`, `real-2026-11-17.json`, `real-2026-11-20.json`; the synthetic tree matrix and the clone-null
calibrations in `benchmarks/results/clonal-calibration-2026-11-13.json` and
`clonal-calibration-n2-amended-2026-11-17.json`; the verdict calibration in `verdict-calibration-2026-11-17.json`.
The tables are rendered in `docs/benchmarks.md`.

- Mouse pancreas, E15.5 [24].
- Human CD34+ bone marrow [16].
- Mouse gastrulation, erythroid lineage [22], file reprocessed by [23].
- Synthetic tree matrix: four topologies, several seeds, the `[synthetic]` preset.

Two calibration results are recorded failures and stay so: the original pseudotime null failed its depth control
(57 of 200 rejections against a bound of 18), which led to the amended N2, and the verdict verification failed as
described in section 3.
