# Results so far

This page says what the first real-data case study found, and what it does not show.
The case study is on Sheih et al. 2020, a study of CAR-T cells in four patients.

## What was declared before the data

The analysis plan was written down before any real data were scored. It was merged in
[PR #51](https://github.com/shreyandhawa/lumenCell_V2/pull/51), at commit 5ef3151.
The plan was written from the paper and the file headers only.

- A clone is a set of cells that share the same paired T-cell receptor chains.
- Clones are counted within one patient. The same receptor in two patients is two clones.
- The clone null shuffles labels within each time point, so clones that grow at one time point do not count as lineage agreement.
- The trajectory starts from the infusion product cells. This start is an assumption.
- Each patient is run alone, with each of three methods. That is 12 runs.
- A run with all four patients pooled is a diagnostic only, never the headline.
- Clone size 2 is the main test. Clone size 3 is a sensitivity check. There are 1000 shuffles, with seed 0.

## What failed

The verdict rule failed its check on fresh seeds, on 2026-11-17. Its verification ran on
31 negative-control runs. 28 of 31 were rated supported. The rule was not changed to fix this.

Because of that failure:

- No run is shown as supported.
- A supported verdict is capped at provisional ("Not shown to be a tree").
- A failed check is shown as weak ("Clones do not back these lineages") or not_supported ("Not supported: cells left without a pseudotime").

## What was found

Sheih 2020, per patient. There are 12 method runs: 4 patients, 3 methods.

- 8 of 12 are weak ("Clones do not back these lineages").
- 4 of 12 are provisional ("Not shown to be a tree").
- None is supported. None is not_supported.

| Patient | paga_dpt | palantir | scfates_ppt |
|---|---|---|---|
| CLL-1 | provisional | weak | weak |
| CLL-2 | provisional | weak | weak |
| NHL-6 | weak | weak | weak |
| NHL-7 | weak | provisional | provisional |

A run passes the clone check when its headline p is at most 0.01 and its lift over a
k-means clustering baseline (Δη) is above 0. Four of the 12 runs pass it.

## What it does not show

- **It does not show a tree.** Provisional means "not shown to be a tree". It is never support.
- **The verdict is not evidence of a tree.** Its rule cannot tell a tree from these controls. Supported means "connected", not "a tree".
- **Clones give no direction.** Shared clones say two states are related. They never say which came first.
- **The direction comes from an assumed root.** The paper's main text and Methods name no trajectory root (the supplementary figures were not read).
- **It is four patients.** Two have CLL and two have NHL. Nothing here applies beyond them.
- **There is no batch correction.** Pooled runs may mix patient structure into the lineages, so the pooled run is a diagnostic only.
- **Clone scores fall under the time-point null.** In every per-patient run, the point estimate of the clone score against the time-point null is below half its value against the within-patient null (ratio 0.03 to 0.49). Two intervals reach above half: NHL-7 palantir 0.439 [0.179, 0.625] and NHL-7 scfates_ppt 0.491 [0.245, 0.770]. Against the pseudotime-depth null the score is not below half in every run (CLL-1 paga_dpt: 0.695 to 0.363).
- **The lineages add little.** Expression clustering matches most of the clone score. Δη is at most 0.050 in absolute value as a point estimate (−0.050 to +0.049). Its clone-bootstrap intervals are wider (up to [0.008, 0.088] and [−0.061, −0.037]): 4 runs have an interval wholly above zero and 3 wholly below.
- **Each method scores its own cells.** So the three methods are not compared like for like.
- **Blood only.** The infusion product is a cultured, stimulated cell population.

Full details: [the case study](case-studies/sheih-2020.md) and [the handoff](superpowers/HANDOFF.md).

## Corrections

**2026-11-23.** Two lines under "What it does not show" were corrected.
- *Clone scores.* The old line said the score was below half "against the time-point null or the pseudotime-depth null" in every run. That held only because of the "or": against the pseudotime-depth null alone it is false (CLL-1 paga_dpt 0.695 to 0.363, a ratio of 0.52). The line now names the time-point null, and gives the two runs whose intervals reach above half.
- *k-means baseline.* The old line gave "at most 0.050" with no uncertainty. The line now adds the clone-bootstrap intervals.

Both come from `benchmarks/results/diagnosis-clonal-2026-11-23.json` (clone bootstrap, 500 replicates, 95% percentile; [diagnosis page](paper/diagnosis-clonal.md)) and the case-study table. No other finding on this page changed, and no rule, threshold or null changed.
