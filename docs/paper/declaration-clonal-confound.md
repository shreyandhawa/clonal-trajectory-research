# Declaration: is the clonal agreement score confounded by time?

Declared 2026-11-23, in a PR that is merged before any check below is run. Nothing here changes a
rule, threshold, seed, definition or null. The checks are code in `src/ctr/diagnosis_clonal.py`
(tested on toy data only). Results go in a later PR as `benchmarks/results/diagnosis-clonal-<date>.json`
and `docs/paper/diagnosis-clonal.md`.

**The observation.** In Sheih 2020 (`benchmarks/case_studies/results/sheih2020-2026-11-20.json`, 12
per-patient runs), the score against the time-point null (N3) is below half of the score against the
within-patient null (N1) in all 12 runs (the ratios, which I read from that file before writing this, run from 0.03
to 0.49; NHL-7 scfates_ppt is the closest at 0.49). The p against N1 is 0.000999 in all 12. The rest
of this document asks what that pattern means.

## 1. Does the existing calibration already answer it? Partly. The part it answers, and the part it does not.

Read from `clonal-calibration-2026-11-13.json` (phase 1), `clonal-calibration-n2-amended-2026-11-17.json`
(N2a) and `src/ctr/calibration.py`, no run:

**Answered.** The calibration plants clones that carry no lineage information and counts rejections
(p <= 0.05, bound 18 of 200). Two of its controls are a depth confound and a donor confound.
- `depth_only` (clones are consecutive in true pseudotime, so a clone is a stretch of the trajectory and
  nothing else): **N1 rejects 200 of 200** with no lineage signal. So N1 is not a valid null when clones
  are tied to depth, and a p of 0.001 against N1 carries no information in that case. The recorded
  headline p is the **largest** p over the nulls, so it is not N1's p alone.
- The decile N2 failed on that control (57 of 200, recorded as failed). The amended N2 (N2a, seeds
  300-499) passes it: 8 of 200. Donor confound: N1 calibrated (7 of 200, then 15 of 200); ignoring donors
  rejects 200 of 200.

So **"N1 alone is confounded by depth, and a significant N1 p is uninformative then"** is already shown, for
pseudotime depth, by a recorded file.

**Not answered, and the reason it matters here.**
1. The calibration records **p-values only** (`RejectionCount.p_values`); no eta was stored. It says
   nothing about how large eta against N1 is when the only structure is depth or time.
2. **N3 (strata = time point) was never calibrated.** The synthetic generator has no time-point variable
   and `calibration.py` never passes strata, so N3 does not exist in any recorded calibration. The 12
   Sheih numbers lean on N3.
3. **Time point is not pseudotime.** In Sheih, clones expand at a time point; that is clone structure by
   sample, which is not a stretch of pseudotime.
4. Nothing recorded separates two readings of "eta(N3) < half of eta(N1)": (i) time structure inflates
   eta(N1), so the drop is the confound removed; (ii) N3 over-corrects, because lineage and time point
   are collinear, so the drop would happen under real lineage signal too. They predict different things
   on synthetic data, so I test them there (section 2).

## 2. Synthetic check: planted clones, a time point variable, known signal

**Data.** Seeds 600-639 (40 seeds; clear of 0-5, 100-499, and of 500-519 and 900-904, which the HANDOFF
reserved for a verdict redesign); seed s uses `topologies[(s - 600) % 3]` with
`["bifurcation", "trifurcation", "binary2"]`, the `[synthetic]` preset, 3000 cells, 2000 genes, via
`lumencell.bench.synth.generate`. One donor (a patient run alone, as in the case study).

**Time points.** K = 4 (the infusion product and three later samples, as in Sheih). A cell's time point
is the quartile of `u = rank(true_pseudotime) / n + Normal(0, sigma)`, drawn from
`default_rng([seed, 7100601])`. Two settings, **sigma = 0.1 (time tracks position closely) and sigma = 0.4
(loosely)**.

**Clones.** `label_rate` 0.85, `draw_clone_size` of `lumencell.bench.synth_clones` (singleton share 0.5,
Zipf 2.2), drawn from `default_rng([seed, 7100602])`. As in `add_clones`, with `fate_bias` f a labelled
cell joins its leaf's pool with probability f, otherwise the trunk pool; each pool is permuted and cut
into consecutive clones. The planting is `plant_clones` in the module. Four arms:

| Arm | fate_bias | Clones confined to one time point | What it is |
|---|---|---|---|
| T0 | 0 | no | no structure at all (calibration check) |
| T1 | 0 | **yes** | time only: clones are time-point specific, no lineage signal |
| T2 | 0.7 | no | lineage only: real signal, clones span time points |
| T3 | 0.7 | **yes** | both: the closest to Sheih |

Pools are built inside each time point when "confined". The label and leaf-join draws are the same in every arm of a seed (same labelled cells); the arms differ
in how those cells are pooled into clones.

**Scoring.** `score_clonal` with the **runtime** definitions (N1, N2 with the lineage-onset split, N3 with
strata = time point; B = 1000, seed 0, m = 2), in two modes: **oracle** (true lineages, true
order, single-lineage cells, constant baseline, as in `calibration._oracle`) as the primary result; and
**own-cells with `paga_dpt`** (prep and one method run per seed, rooted at the true root label, k-means
baseline as in `score_with_baseline`) as a check that the method's errors do not change the reading.
Not run: palantir and scfates_ppt (the method run does not depend on the arm, so each seed's run is
reused across all 8 conditions).

**Reported per arm, sigma and mode.** Median and interquartile range of eta against N1, N2 and N3; the ratio
`R = eta(N3) / eta(N1)` for seeds with `eta(N1) >= 0.05` (the repo's own `oracle_eta_min`; seeds below it
are counted and left out of R); rejections (p <= 0.05) for each null against the binomial bound
(`rejection_bound(40, 0.05, 0.99)` = 6); the share of seeds with R < 0.5. Intervals: a 95% percentile
bootstrap over seeds (2000 resamples, seed 0) for each median.

**Decisions, fixed now (both sigma must agree; if they do not, the reading is "depends on sigma").**
- **D0, validity.** T0: N1, N2 and N3 each reject at most 6 of 40. If any does, the harness is broken and
  nothing else is read.
- **D1, "N1 is confounded by time".** T1: median eta(N1) >= 0.05, N1 rejects more than 6 of 40, N3
  rejects at most 6 of 40, and |median eta(N3)| < 0.02.
- **D2, "N3 keeps real signal when lineage and time are separable".** T2: median eta(N3) >= 0.5 x median
  eta(N1), and N3 rejects more than 6 of 40.
- **D3, "the halving is a confound signature".** T3: median R >= 0.5 (real signal survives N3 even with
  clones tied to time).
- **Outcomes.**
  - D1, D2 and D3 hold: **the Sheih pattern (R < 0.5 in 12 of 12) is what time structure alone produces
    and not what a real signal produces. eta(N1) is overstated by time; eta(N3) is the number to report.**
  - D1 holds, D3 fails (T3 median R < 0.5): **N1 is confounded, but the halving is also what a real signal
    does when clones are tied to time. The ratio is not evidence of a confound.** Report eta(N3) as the
    conservative figure and say the ratio cannot separate the readings.
  - D1 fails: **time structure of this kind does not inflate eta(N1) in the synthetic data, so the Sheih
    pattern is not explained by it.** The paper must not call the score confounded on this evidence.
  - D2 fails (T2 median R < 0.5): **N3 over-corrects even when time and lineage are separable;** the
    halving is then an artefact of the null.
- **Sheih comparison.** For each outcome the results also say, per arm, what share of seeds have R below
  the median Sheih ratio (0.17, read above from the 12 recorded ratios, which are re-read from the file
  in the results) and below its largest (0.49).

## 3. Bootstrap intervals for the Sheih numbers

**Unit.** The clone, not the cell. The scored cells of a clone are not independent draws (they share a
receptor and, by design, a state), so a cell bootstrap would give intervals that are too narrow. A
**clone bootstrap**: for each of the 12 runs, draw K scored clones with replacement (K = the run's number
of scored clones at m = 2), `default_rng(0)`, 500 replicates. Each draw keeps all that clone's scored
cells, with a new clone id per draw (a clone drawn twice is two clones). Each replicate is re-scored with
`score_clonal`, 100 permutations per null (the null mean's sampling error at B = 100 is far smaller than
a clone-level interval; this is a stated approximation, chosen to make 6000 scores affordable),
with the run's own lineage membership, pseudotime, strata and k-means partition held fixed, m = 2, seed
`b` for replicate `b`.

**What gets an interval** (95% percentile, 2.5 and 97.5): eta(N1), eta(N2), eta(N3), R = eta(N3)/eta(N1),
delta_eta (the lift over k-means), and the share of replicates with delta_eta > 0 and with R < 0.5
(R is undefined in a replicate whose eta(N1) is below 0.05; those are counted and left out of the share).
p-values are not bootstrapped: they are reported as recorded, with the pass rule (p <= 0.01 and delta_eta
> 0) applied to the point estimate.

**Point estimates.** The three methods are rerun per patient on the cached derived file with the declared
case-study settings (`[case_study.sheih2020]`), under the pinned lumencell (0.5.0), and re-scored with the
runtime definitions at B = 1000. The recorded values (commit 5b4f83f, `lumencell 0.1.0.dev0`) are
reported next to them. **If any run's eta(N1) moves by more than 0.02 from the recorded value, that run is
flagged "drift" and both numbers are shown; the interval is then around the fresh run.** Nothing is edited
in the recorded file.

**What the intervals leave out, said now.** Uncertainty in the method's own lineages and pseudotime (one run
per method), in the k-means partition (fixed), and in which patients were sampled (four).
Four patients cannot give a patient-level interval; none is claimed.

**Reported per run, not only "4 of 12":** patient, method, scored cells and clones, lineages, eta against
N1, N2, N3 with intervals, R with interval, p against N1, N2, N3 (the largest is the headline), eta_base, delta_eta with
interval, and whether the run passes C5. The k-means result "the lineages add at most 0.05 over expression
clustering" is checked as the range of delta_eta over the 12 runs and each one's interval; the recorded
point values are +0.049 (largest) to -0.050.

## 4. Daniel 2022 as a second clonal dataset: reasons, not run

Reading only (`thresholds.toml` `[real.daniel2022.*]`, the HANDOFF Phase 3 Task 6 and 8 notes,
`real-2026-11-20.json`). **Not usable as a confirmation of the Sheih result or of any trajectory claim;
usable at most as an exploratory second look at the null behaviour, and only after its own
declaration and your decision.**
- *Why it was "not assessable".* Declared 2026-11-20 with no gated lineage: the two CX3CR1+ labels
  (`TEx_int`, `TEx_KLR`) are one stage in the papers but two labels in the data, so a lineage truth
  cannot be written without inventing an order. A lineage truth is what the oracle scoring and the lineage
  gates need. Own-cells scoring does not need it, but the result file shows `clonal_status not_assessable`
  for all three methods, as declared.
- *Namespace is an assumption.* The records name no mouse, so clones are keyed by capture (rule b), on the
  stated assumption of one mouse per capture. If a capture pools mice, or a mouse spans captures, clone
  sharing across captures is misread. Sheih has patient as a real namespace.
- *Time structure is weak.* Two days (8 and 21) after dropping the state-gated sorts, spleen only,
  eight captures. Sheih has four time points per patient. A time-point null with two strata cannot
  show the same pattern as one with four.
- *The root is not credible.* `TEx_prog` sits late in every method's pseudotime (median root pseudotime
  0.70, 0.80, 0.984, against 0.07-0.58 on the other datasets), and day-versus-pseudotime Spearman is 0.13
  to 0.34. The direction is not trusted there.
- *Different species and biology.* Mouse chronic LCMV exhaustion, not human CAR-T. Agreement there does
  not bear on Sheih.
- *Not blind.* The Daniel clone numbers (recurrence 0.0612, labelled share 0.898) are already recorded, and
  the file has been scored once; any new analysis is a second look at seen data and must say so.
- **What it could add.** If you decide to, a separate declaration would fix own-cells scoring, strata =
  day, namespace = capture, and the same pass rule, and would call the result exploratory. I recommend
  declining it for the paper: it cannot be a second confirmation, and the paper's honest scope is one
  dataset.

## 5. What can be said at the end (the sentence is fixed by the outcome of section 2)

The results document ends with one sentence chosen from the four outcomes above. It will not say the score
is "confounded" unless D1 holds, and it will not say a drop in eta is "a confound signature" unless D1, D2 and
D3 all hold. In every case the paper reports eta(N3) as the headline and the clone-bootstrap intervals
beside it.

## Limits, stated now

One synthetic family (the lumencell trees); one clone model (fate bias on a leaf pool or the trunk pool); a
time-point model I chose (quartiles of noisy rank). Oracle and one method only. Percentile bootstrap at 500
replicates and 100 permutations. These bound what the synthetic check can show; they are not tuned.
