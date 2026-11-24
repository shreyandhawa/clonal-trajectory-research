# Outreach drafts (for you to send; nothing here has been sent)

Written 2026-11-24. Every name below comes from the author lists in `docs/paper/literature.md` or the Crossref
records in the draft's reference list. No email address or current affiliation was looked up. Before sending, find
each person's current address on their lab or institution page, check who the corresponding author is on the
paper itself, and fill the brackets. Keep each email short, as below. People answer one clear question more often
than a request to read a whole paper.

Timing. Send the expert-reader email (a) before you post, so an answer can still change the draft. Send the
courtesy notes (b) after the preprint is posted, with its link, so they can see exactly what is said about their
work. Ask bioRxiv (c) first of all, since its answer decides how you fill in the affiliation field.

## (a) One question to one expert reader

### Three candidates, and why each fits

| Candidate | Paper (in the literature check) | Why they fit | The question to ask them |
|---|---|---|---|
| Song M (with Tenha L) | Tenha and Song 2022, PLoS Comput Biol, doi:10.1371/journal.pcbi.1009829 [2] | They tested trajectory presence against a no-trajectory null with shuffled-gene negative controls, the closest prior work to the verdict failure | Is a coverage-only verdict failing on blob, loop and sheet controls the expected result, and would their tree-dimension statistic be a fair replacement for C2 on data like this? |
| Horns F or Swift M (with Quake SR) | Swift, Horns and Quake 2023, Life Sci Alliance, doi:10.26508/lsa.202201792 [11] | They used clone-label shuffles restricted to strata (lane, mutation status), the closest precedent for the stratified nulls here | When the root is the earliest sample and clones expand at one time point, does a shuffle within time point remove real lineage signal as well as time structure? |
| Ji Z (with Wang H) | Wang and Ji 2023, bioRxiv, doi:10.1101/2023.11.27.568912 [13] | They showed that cells of one clone share expression, which is the reason behind the k-means baseline | Is k-means on the same principal components a fair no-trajectory baseline for a clone agreement score, or does it set the bar too high? |

My suggestion is the second. The time-point question is the one the paper leaves open, and it is the question
closest to T-cell therapy data, which is where you want to show interest.

### Email (written for the second candidate; change the question line for the others)

Subject: One question about stratified clone shuffles in CAR-T data

Dear Dr. [family name],

I am an independent researcher, and I am writing a short methods paper that tests trust checks for single-cell
trajectory inference against T-cell receptor clones, using the public CAR-T data from Sheih et al. 2020 (four
patients). Your 2023 paper on fate bias in human B cells, with its clone-label shuffles restricted to lane and
mutation status, is the closest precedent I found for what I did.

I have one question. In my data the trajectory is rooted at the infusion product, which is also the earliest
sample, and clones expand at single time points. When I shuffle clone labels within time point instead of within
patient, the clone agreement score falls to under half in every run (point estimates; two runs' intervals reach
above half). On synthetic data, time structure alone did not raise the within-patient score, so I do not think the
drop is simply a time confound. Do you think a shuffle within time point can remove real lineage signal when
lineage and sampling time are this closely tied, and is there a null you would trust more in that case?

A two-line answer would help me a lot. The declared analysis plan and all results are public at
github.com/shreyandhawa/clonal-trajectory-research if you want to look, but I do not expect you to.

Thank you for your time,
Shreyan Dhawa
Independent researcher
[ORCID]

## (b) Courtesy notes to the authors of the methods and the dataset

These are not critiques of their work. Each note says what was done with their method or data, that the finding is
about lumencell's checks and not about their method or paper, and gives them a way to correct anything I got wrong.

### Palantir (Setty M, et al. 2019, Nat Biotechnol, doi:10.1038/s41587-019-0068-4)

Subject: Palantir used in a preprint on trajectory trust checks

Dear Dr. [family name],

I have posted a short preprint, [title], [link], which tests two trust checks in lumencell, an open-source tool I
wrote that runs Palantir alongside PAGA and scFates and puts checks next to each result. I am writing as a courtesy,
because Palantir is one of the three methods in every analysis.

The finding is that these checks did not hold up. lumencell's summary verdict, as it was checked, read only whether
95% of cells got a pseudotime, so it rated synthetic negative controls (a cloud, a ring, a sheet) as supported. It
is not a finding about Palantir. On those controls Palantir ordered the cells much as their generator did, which is
what a pseudotime method is meant to do, and on the two-group controls lumencell 0.5.0 stops Palantir on a
disconnected graph before it runs. In the CAR-T case study, Palantir is one of three methods whose lineages I scored
against T-cell clones, and the paper makes no comparison of the methods, since each is scored on its own cells.

If anything in how I describe or ran Palantir is wrong, I would be glad to correct it in the next version. The code
and settings are at github.com/shreyandhawa/clonal-trajectory-research.

Best regards,
Shreyan Dhawa
Independent researcher

### scFates (Faure L, Soldatov R, Kharchenko PV, Adameyko I. 2023, Bioinformatics, doi:10.1093/bioinformatics/btac746)

Subject: scFates used in a preprint on trajectory trust checks

Dear Dr. [family name],

I have posted a short preprint, [title], [link], which tests two trust checks in lumencell, an open-source tool I
wrote that runs scFates's principal tree alongside PAGA and Palantir. I am writing as a courtesy, because scFates is
one of the three methods in every analysis.

The finding is that these checks did not hold up: lumencell's summary verdict rated synthetic negative controls as
supported because, as checked, it read only whether 95% of cells got a pseudotime. It is not a finding about
scFates. In the CAR-T case study, scFates is one of three methods whose lineages I scored against T-cell clones, and
the paper makes no comparison of the methods. One detail you may want to know: in the recorded verification, three
scFates runs on a two-group control raised an IndexError, and on a rerun with newer libraries they completed. I did
not find which library changed, and I make no claim about scFates from it.

If anything in how I describe or ran scFates is wrong, I would be glad to correct it in the next version. The code
and settings are at github.com/shreyandhawa/clonal-trajectory-research.

Best regards,
Shreyan Dhawa
Independent researcher

### Sheih et al. 2020 (Nat Commun 11:219, doi:10.1038/s41467-019-13880-1)

Subject: Your CAR-T single-cell data used in a methods preprint

Dear Dr. [corresponding author's family name],

I have posted a short methods preprint, [title], [link], that uses the single-cell and TCR data from your 2020
Nature Communications paper (GEO GSE125881) as its one case study. Thank you for making the data public. I am
writing as a courtesy so that you know how they were used.

The preprint tests trust checks in a trajectory tool I wrote, and the finding is that these checks did not hold up.
On your data I scored how well T-cell clones agree with the lineages that three trajectory methods return, with
each patient run alone and the trajectory rooted at the infusion product. Your paper names no trajectory root, so
the preprint says plainly that this root is my assumption. The clone agreement score falls to under half when
clones are shuffled within time point, and a clustering with no trajectory matches most of it. This is a statement
about the checks, not about your findings. Your paper does not rest on these trajectories, and the preprint makes no
biological claim about the patients.

If I have misread anything about the data, for example how the per-sample TCR tables map to cells or which chains
they contain, I would be glad to correct it. The full analysis plan, which was written before the data were scored,
is at github.com/shreyandhawa/clonal-trajectory-research.

Best regards,
Shreyan Dhawa
Independent researcher

## (c) Question to bioRxiv

Send through bioRxiv's contact page or help address (check the current one on biorxiv.org; it was not looked up
here).

Subject: Affiliation for an unaffiliated author, and scope of a methods study on public data

Hello,

I am planning to submit my first preprint to bioRxiv and have two questions before I do.

1. I have no institutional affiliation. The submission page says an affiliation is needed so there is an entity
   providing oversight. What should an unaffiliated author enter in that field? Is "Independent researcher" with a
   city and country acceptable, or is something else needed?

2. The preprint is a methods and calibration study. It tests two checks in an open-source tool for single-cell
   trajectory inference, against synthetic negative controls and against public data, including one public human
   CAR-T dataset from GEO (GSE125881) from a published clinical study. It reports negative results about those
   checks, with full methods, declared analysis plans and code. It makes no clinical claims. Is a paper like this in
   scope for bioRxiv, and would the human data lead screeners to send it to medRxiv instead?

Thank you,
Shreyan Dhawa
