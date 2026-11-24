# Diagnosis: is the clonal agreement score confounded by time?

Run 2026-11-23 under [the declaration](declaration-clonal-confound.md) (PR #5). Numbers:
`benchmarks/results/diagnosis-clonal-2026-11-23.json`. Code: `src/ctr/diagnosis_clonal.py`.

**Answer.** Not shown. The existing calibration answers half of it (N1's p is unreliable under a depth confound). In
synthetic data with clones tied to time points, time structure alone did **not** raise eta against the within-patient
null (N1) above 0.013, and a real lineage signal kept its eta under the time-point null (N3) (ratio 1.0). So neither
simple story, "time inflates eta" or "N3 over-corrects", reproduces the Sheih drop. Where that drop comes from is open.

## 1. Existing calibration

`depth_only/N1` rejects 200 of 200 with no lineage signal, and the amended N2 fixes it (8 of 200), so a significant
p against N1 means nothing when clones follow depth. It stored p-values only, and N3 was never calibrated (declaration, section 1).

## 2. Synthetic check (40 seeds, 600-639; bound 6 of 40; median eta, rejections of N1/N2/N3, median R with seeds where R is defined)

| mode | sigma | arm | eta N1 | eta N3 | rejections | R (n) |
|---|---|---|---|---|---|---|
| oracle | 0.1 | T0 no structure | -0.001 | -0.000 | 2/2/2 | – (0) |
| oracle | 0.1 | T1 time only | 0.013 | -0.005 | 15/2/2 | -0.05 (11) |
| oracle | 0.1 | T2 lineage only | 0.767 | 0.764 | 40/40/40 | 1.00 (40) |
| oracle | 0.1 | T3 both | 0.727 | 0.714 | 40/40/40 | 1.00 (40) |
| oracle | 0.4 | T0 no structure | -0.001 | -0.001 | 2/2/2 | – (0) |
| oracle | 0.4 | T1 time only | 0.005 | -0.000 | 6/1/1 | 0.49 (3) |
| oracle | 0.4 | T2 lineage only | 0.767 | 0.767 | 40/40/40 | 1.00 (40) |
| oracle | 0.4 | T3 both | 0.735 | 0.734 | 40/40/40 | 1.00 (40) |
| paga_dpt | 0.1 | T0 no structure | 0.003 | 0.003 | 4/5/4 | 1.05 (2) |
| paga_dpt | 0.1 | T1 time only | 0.026 | 0.000 | 18/1/1 | -0.03 (16) |
| paga_dpt | 0.1 | T2 lineage only | 0.743 | 0.741 | 40/40/40 | 1.00 (40) |
| paga_dpt | 0.1 | T3 both | 0.712 | 0.696 | 40/40/40 | 0.99 (40) |
| paga_dpt | 0.4 | T0 no structure | 0.003 | 0.003 | 4/5/4 | 1.02 (2) |
| paga_dpt | 0.4 | T1 time only | 0.011 | 0.008 | 10/4/3 | 0.56 (7) |
| paga_dpt | 0.4 | T2 lineage only | 0.743 | 0.742 | 40/40/40 | 1.00 (40) |
| paga_dpt | 0.4 | T3 both | 0.721 | 0.715 | 40/40/40 | 1.00 (40) |

Declared rules: D0 holds (T0 rejects 5 of 40 at most, in either mode). **D1 fails**: with time-only clones, median eta(N1) is 0.013
(sigma 0.1) and 0.005 (0.4), below the 0.05 the rule requires, although N1's p over-rejects at sigma 0.1 (15 and 18 of 40 against a
bound of 6; at sigma 0.4 it is 6 and 10). D2 and D3 hold (eta(N3) keeps 99-100% of eta(N1) with real signal, with or without
clones tied to time). The declared outcome is therefore: **time structure of this kind does not inflate eta(N1), so the Sheih pattern is
not explained by it.** Both sigma and both modes agree. R for T1 is a ratio of near-zero numbers over 3-16 seeds and carries no weight.

## 3. Sheih 2020, per run (clone bootstrap, 500 replicates, 95% percentile; headline p is the largest of N1-N3)

Fresh re-run on lumencell 0.5.0 reproduces the recorded eta(N1) of all 12 runs (no run moved by more than 0.02).

| run | clones | eta N1 | eta N3 | R = N3/N1 | headline p | delta_eta vs k-means | share delta>0 | share R<0.5 | C5 |
|---|---|---|---|---|---|---|---|---|---|
| CLL-1 paga_dpt | 652 | 0.695 [0.627, 0.755] | 0.247 [0.183, 0.319] | 0.355 [0.284, 0.433] | 0.001 | 0.036 [0.007, 0.067] | 0.99 | 1.00 | pass |
| CLL-1 palantir | 786 | 0.125 [0.076, 0.172] | 0.020 [-0.008, 0.054] | 0.157 [-0.102, 0.360] | 0.076 | -0.031 [-0.058, -0.004] | 0.01 | 1.00 | no |
| CLL-1 scfates_ppt | 631 | 0.571 [0.510, 0.630] | 0.073 [0.044, 0.107] | 0.129 [0.083, 0.176] | 0.001 | -0.005 [-0.036, 0.026] | 0.38 | 1.00 | no |
| CLL-2 paga_dpt | 1271 | 0.213 [0.177, 0.248] | 0.024 [0.007, 0.038] | 0.112 [0.036, 0.173] | 0.001 | 0.024 [0.006, 0.042] | 0.99 | 1.00 | pass |
| CLL-2 palantir | 1177 | 0.114 [0.079, 0.147] | 0.021 [-0.006, 0.048] | 0.185 [-0.075, 0.357] | 0.070 | -0.011 [-0.040, 0.016] | 0.20 | 1.00 | no |
| CLL-2 scfates_ppt | 968 | 0.143 [0.104, 0.187] | 0.011 [-0.008, 0.032] | 0.075 [-0.067, 0.215] | 0.155 | 0.018 [-0.024, 0.054] | 0.83 | 1.00 | no |
| NHL-6 paga_dpt | 548 | 0.415 [0.351, 0.472] | 0.089 [0.051, 0.123] | 0.216 [0.133, 0.280] | 0.001 | -0.008 [-0.023, 0.006] | 0.13 | 1.00 | no |
| NHL-6 palantir | 458 | 0.138 [0.073, 0.207] | 0.031 [0.012, 0.053] | 0.228 [0.123, 0.350] | 0.001 | -0.022 [-0.041, -0.007] | 0.00 | 1.00 | no |
| NHL-6 scfates_ppt | 320 | 0.313 [0.246, 0.391] | 0.011 [0.003, 0.022] | 0.034 [0.011, 0.062] | 0.026 | -0.050 [-0.061, -0.037] | 0.00 | 1.00 | no |
| NHL-7 paga_dpt | 299 | 0.216 [0.171, 0.265] | 0.009 [-0.000, 0.021] | 0.043 [-0.001, 0.095] | 0.015 | 0.032 [0.002, 0.065] | 0.98 | 1.00 | no |
| NHL-7 palantir | 276 | 0.064 [0.033, 0.093] | 0.028 [0.002, 0.050] | 0.439 [0.179, 0.625] | 0.005 | 0.010 [-0.002, 0.022] | 0.96 | 0.71 | pass |
| NHL-7 scfates_ppt | 185 | 0.070 [0.031, 0.112] | 0.034 [0.009, 0.068] | 0.491 [0.245, 0.770] | 0.001 | 0.049 [0.008, 0.088] | 0.99 | 0.46 | pass |

- **R below 0.5 in 12 of 12 holds for the point estimates, not for every interval.** NHL-7 palantir (R 0.439, interval 0.179 to 0.625,
  0.71 of replicates below 0.5) and NHL-7 scfates_ppt (0.491, 0.245 to 0.770, 0.46) are not safely under half, and the
  four runs with eta(N3) near zero (CLL-1 palantir, CLL-2 palantir, CLL-2 scfates_ppt, NHL-7 paga_dpt) have R intervals that include 0 and negative values.
- **k-means baseline.** The lift delta_eta ranges from -0.050 (NHL-6 scfates_ppt) to +0.049 (NHL-7 scfates_ppt) as point estimates, so "at most 0.05"
  is right for them. The intervals are wider: NHL-7 scfates_ppt reaches 0.088 and NHL-6 scfates_ppt -0.061. Only 4 runs have an interval above zero
  (CLL-1 paga_dpt, CLL-2 paga_dpt, NHL-7 paga_dpt, NHL-7 scfates_ppt), and 3 have one that is wholly below (CLL-1 palantir, NHL-6 palantir, NHL-6 scfates_ppt).
- **4 of 12 pass** (p <= 0.01 and delta_eta > 0): CLL-1 paga_dpt, CLL-2 paga_dpt, NHL-7 palantir, NHL-7 scfates_ppt. Their delta_eta is
  positive in 0.96 to 0.99 of replicates. NHL-7 paga_dpt has delta_eta > 0 in 0.98 of replicates but fails on p (N3 0.015).
- Not covered by these intervals: the method run, the k-means partition, and the four patients (declaration, section 3).

## 4. Daniel 2022

Declined by the owner: the paper treats Sheih 2020 as a single case study. Not run. The reasons in the declaration
(section 4) stand as a record.

## What this lets the paper claim

In four patients' CAR-T cells, the clone agreement score against the time-point null is under half of that against the
within-patient null in the point estimates of all 12 runs (R 0.03 to 0.49), but two runs' intervals reach 0.625 and 0.770; synthetic planted-clone data
show that time tied to clones does not by itself produce a gap like this, so the paper reports the time-point-null eta with its
interval as the headline and does not call the score confounded.

## Corrections

**2026-11-23.** In "What this lets the paper claim", the upper end of NHL-7 palantir's R interval was given as
0.62. The value in `benchmarks/results/diagnosis-clonal-2026-11-23.json` is 0.6253, which is 0.625 at three
decimals (as in the table above) and 0.63 at two; 0.62 was a truncation. The sentence now gives 0.625 and 0.770.
Nothing else on this page changed.
