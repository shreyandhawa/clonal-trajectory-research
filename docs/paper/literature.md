# Literature check for the planned short paper

Researched 2026-11-23. Research only; no code was run. Every paper in the main tables was opened
(abstract at least) at a primary or indexing page, and the DOI was matched to the cited title. How I
checked, and its limits:

- Title and DOI were matched on the Crossref API (`api.crossref.org/works/<doi>`) or on the Europe PMC
  REST record for that DOI (`ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:<doi>`). Crossref
  returned HTTP 429 for two DOIs, so Europe PMC was used for those.
- Publisher pages at nature.com and pmc.ncbi.nlm.nih.gov refused automated access (login redirect,
  browser check). I did not try to get around that. Abstract-level facts therefore come from Europe PMC;
  deeper facts (nulls, controls) come only where I read open full text, and each such row says so.
- The fetch tool summarises pages with a small model, so wording below is my paraphrase, not a quote.
- "Overlap" labels are against the working claim (section "Working claim"): same claim, partial, none.

## Working claim, and how it differs from the repo

> "TCR clonal concordance and tree-likeness verdicts overstate trajectory validity: in a
> pre-registered evaluation, a tree-support rule rated 28 of 31 negative controls as supported, and
> clone agreement in CAR-T data (Sheih et al. 2020) mostly vanished under time- and depth-matched nulls."

Mismatches with `docs/results.md` and `docs/case-studies/sheih-2020.md` (read first):

1. **"tree-support rule" / "tree-likeness".** The 28 of 31 figure is for the overall verdict rule. The
   case study says tree-likeness (C2) and both stability checks (C3, C4) are left out for lack of a
   calibrated threshold, so the verdict "reads coverage (C1) and clonal support (C5) only", and
   "supported" means "connected", not "a tree". The failed rule is therefore not a tree-likeness rule.
2. **"pre-registered".** The repo shows a dated declaration (`[case_study.sheih2020]` in
   `benchmarks/thresholds.toml`, PR #51, commit 5ef3151) written before the case-study data were scored.
   That covers the Sheih analysis plan. The pages I read do not say the 31-negative-control check had its
   own registered plan, and neither is a public registry entry. "Declared in advance in a dated commit"
   is what the repo supports.
3. **"mostly vanished".** Against the within-patient shuffle (N1) every run has p = 0.000999, so the
   concordance does not vanish. What happens: eta against the time-point null (N3) is below half of eta
   against N1 in all 12 per-patient runs (I re-checked the 12 rows of the generated table; the closest are
   NHL-7 palantir 0.064 to 0.028 and NHL-7 scfates_ppt 0.070 to 0.034). Seven of 12 runs still have a
   headline p of at most 0.01; four of them also beat the k-means baseline.
4. **"time- and depth-matched".** In the repo "depth" is pseudotime-decile stratification (N2), not
   sequencing depth. N2 is not below half of N1 in every run (for example CLL-1 paga_dpt 0.695 to 0.363,
   CLL-2 scfates_ppt 0.143 to 0.124, NHL-7 palantir 0.064 to 0.049). The "under half in every run" result
   holds for N3, the time-point null, and the results page words it as "N2 or N3".
5. **The k-means finding is missing from the claim.** Delta-eta is at most 0.050 in absolute value in
   every per-patient run and at or below 0 in 6 of 12, so expression clustering matches most of the
   clone score. This is arguably the stronger result.
6. **Scope.** Four patients (2 CLL, 2 NHL), 3 methods, blood only, root assumed to be the infusion
   product. The claim should not read as general.

## (a) Clonotypes or lineage barcodes used to validate or build trajectories

| Citation | What it shows | Overlap |
|---|---|---|
| Zhang L, et al. Lineage tracking reveals dynamic relationships of T cells in colorectal cancer. *Nature* 564(7735), 2018. doi:10.1038/s41586-018-0694-x | Introduces STARTRAC: TCR sharing among about 11,000 T cells from 12 colorectal cancer patients used to infer relationships between T-cell states. Abstract only (paper is not open access). | partial (clone sharing as lineage evidence; no matched nulls seen) |
| Xie J, et al. LRT: Integrative analysis of scRNA-seq and scTCR-seq data to investigate clonal differentiation heterogeneity. *PLoS Comput Biol* 19(7), 2023. doi:10.1371/journal.pcbi.1011300 | Builds trajectories from RNA, then clusters clonotypes by TCR and phenotype to find clusters biased along the trajectory. Open full text read: a permutation test shuffles cluster membership across cells (cluster sizes fixed) against the global cell distribution; no stated control for time point, clone size or sampling depth; no ground-truth validation (only agreement with earlier biology); mouse LCMV data only. | partial (uses clones plus a permutation; no stratified or matched null) |
| Fu Y, et al. Deciphering Cell Fate and Clonal Dynamics via Integrative Single-Cell Lineage Modeling (Clonotrace). bioRxiv 2025. doi:10.1101/2025.09.01.673503 (same authors also posted a Research Square version, doi:10.21203/rs.3.rs-7510946/v1) | Joint model of expression and TCR clonotype to infer state transitions and fate bias; tested on T cells, hematopoiesis and therapy resistance. Abstract only; I did not see its controls. | partial (builds clone-aware trajectories; null controls not checked) |
| Guryleva M, et al. Inferring differentiation trajectories from T cell clonotype distributions (PhyloTrajectory). bioRxiv, posted 2026-07-02. doi:10.64898/2026.06.29.735205 | Models clonotype-frequency change as a stochastic process to reconstruct differentiation trees; checked on simulated trees and mouse CD4 T-cell data. The bioRxiv landing page shows no null models or negative controls on real data (abstract only; full text not read). | partial |
| Wilson TL, et al. Common Trajectories of Highly Effective CD19-Specific CAR T Cells Identified by Endogenous T-cell Receptor Lineages. *Cancer Discov* 12(9):2098-2119, 2022. doi:10.1158/2159-8290.CD-21-1508 | Pediatric CD19 CAR T cells: post-infusion cytotoxic cells share receptors with a subset of pre-infusion cells, read as effector precursors. TCR lineages used to infer trajectories in CAR-T data. Abstract only. | partial (same data type, no null critique seen) |
| Sheih A, et al. Clonal kinetics and single-cell transcriptional profiling of CAR-T cells in patients undergoing CD19 CAR-T immunotherapy. *Nat Commun* 11:219, 2020. doi:10.1038/s41467-019-13880-1 | The dataset paper: clones that expand after infusion mostly come from infusion-product clusters with higher cytotoxicity and proliferation genes. Not a validation of trajectories. Searches for a reanalysis of GSE125881 for trajectories or benchmarks found none (absence in search results, not proof). | none |
| Weinreb C, et al. Lineage tracing on transcriptional landscapes links state to fate during differentiation. *Science* 367(6479), 2020. doi:10.1126/science.aaw3381 | Expressed barcodes (LARRY) in hematopoiesis; benchmarks dynamics-inference methods against clonal data and finds fate choice earlier than leading algorithms detect. Abstract-level (Europe PMC and the bioRxiv preprint abstract); metric and controls not read. | partial (lineage tracing used to test trajectory methods; not TCR, not a null critique) |
| Wang SW, et al. CoSpar identifies early cell fate biases from single-cell transcriptomic and lineage information. *Nat Biotechnol* 40(7):1066-1074, 2022. doi:10.1038/s41587-022-01209-1 | Method that infers dynamics from state plus sparse lineage data; applied to hematopoiesis, reprogramming and directed differentiation. Abstract only. | none (method, not validation of other methods) |
| Forrow A, Schiebinger G. LineageOT is a unified framework for lineage tracing and trajectory inference. *Nat Commun* 12:4940, 2021. doi:10.1038/s41467-021-25133-1 | Optimal-transport method using lineage data to improve trajectory reconstruction; claims fewer time points needed. Abstract only. | none |
| Pan X, Li H, Zhang X. TedSim: temporal dynamics simulation of single-cell RNA sequencing data and cell division history. *Nucleic Acids Res* 50(8):4272-4288, 2022. doi:10.1093/nar/gkac235 | Simulator producing expression plus lineage barcodes; tests show trajectory methods recover state transitions in simulation. Abstract only. | partial (simulated ground truth, not real data) |
| Wagner DE, Klein AM. Lineage tracing meets single-cell omics: opportunities and challenges. *Nat Rev Genet* 21(7):410-427, 2020. doi:10.1038/s41576-020-0223-2 | Review of pairing lineage tracing with single-cell atlases. Abstract only. | none (background) |

## (b) Null models for clonal concordance or clone-state coupling

| Citation | What it shows | Overlap |
|---|---|---|
| Swift M, Horns F, Quake SR. Lineage tracing reveals fate bias and transcriptional memory in human B cells. *Life Sci Alliance* 6(3):e202201792, 2023. doi:10.26508/lsa.202201792 | Open full text read. Clone-label permutation tests: fate-bias test restricted to 10X lane and mutation status; per-gene coherence test shuffled within lane (10,000 permutations). Time is not a stratum and clone size is not controlled. Closest precedent for stratified clone-label shuffles; antibody, not TCR, and no trajectory evaluation. | partial (stratified clone-label shuffle exists; not time-matched, no trajectory) |
| Zheng L, Qin S, Hu X, Zhang Z. Indexes characterizing meta-clusters and STARTRAC analysis. Bio-protocol Preprint 1562, 2022. doi:10.21769/p1562 | Protocol linked to a 2021 *Science* pan-cancer T-cell paper. The page describes a permutation test for the STARTRAC expansion index only: clonotype IDs shuffled within each patient, 1000 repeats. It describes no permutation for the migration or transition indices. | partial (within-patient shuffle precedent; the shuffle is not stratified by time, and covers expansion only) |
| Schattgen SA, et al. Integrating T cell receptor sequences and transcriptional profiles by clonotype neighbor graph analysis (CoNGA). *Nat Biotechnol* 40(1):54-63, 2022. doi:10.1038/s41587-021-00989-2 | Compares TCR-similarity and expression-similarity graphs statistically. Abstract only; the exact null was not checked. | none (TCR-phenotype association, not trajectory validation) |
| Wang H, Ji Z. T cell transcriptional landscapes are shaped by TCR sequence similarity. bioRxiv 2023 (preprint, no journal version in Europe PMC). doi:10.1101/2023.11.27.568912 | Cells sharing a clonotype often share cell type, and similar expression tracks similar TCRs. Abstract via Europe PMC. This supports the expectation behind the repo's k-means baseline: clones are expression-similar, so clustering alone can score high. | partial (supports the baseline logic; does not test trajectories) |
| Cottrell T, et al. Evaluating T-cell cross-reactivity between tumors and immune-related adverse events with TCR sequencing: pitfalls in interpretations of functional relevance. *J Immunother Cancer* 9(7), 2021. doi:10.1136/jitc-2021-002642 | In one patient, sample size, tissue type and collection batch or timing distort apparent clone overlap; recommends mitigation. Bulk TCR sequencing, abstract only. | partial (same warning that timing and depth confound clone sharing; bulk, different question) |

I found no paper that applies a time-point-stratified or pseudotime-stratified clone-label shuffle plus a
k-means baseline to score trajectory lineages against TCR clones. That is a search result, not a proof.

## (c) Calibration, negative controls, or confidence for trajectory presence, stability or topology

| Citation | What it shows | Overlap |
|---|---|---|
| Tenha L, Song M. Inference of trajectory presence by tree dimension and subset specificity by subtree cover. *PLoS Comput Biol* 18(2):e1009829, 2022. doi:10.1371/journal.pcbi.1009829 | Opened at the PLOS page. States that existing methods mostly assume a trajectory and infer one even if not significant. Tests trajectory presence via a minimum-spanning-tree dimension statistic against an isotropic-Gaussian no-trajectory null; uses 110 dynverse real datasets, and shuffled-gene versions as 110 negative controls. No lineage-tracing or clonal validation. | partial (negative controls for a trajectory-presence statistic; not a verdict rule, not clones) |
| Tenha L, Song M. Statistical evidence for the presence of trajectory in single-cell data. *BMC Bioinformatics* 23(Suppl 8), 2022. doi:10.1186/s12859-022-04875-9 | Three graph-based statistics with a permutation null for "no trajectory". Abstract only. | partial |
| Hou W, et al. A statistical framework for differential pseudotime analysis with multiple single-cell RNA-seq samples (Lamian). *Nat Commun* 14:7286, 2023. doi:10.1038/s41467-023-42841-y | Statistical framework across samples; abstract notes it detects changes in trajectory topology and accounts for sample variability. The bootstrap branch detection-rate detail came from search-result text and was not read on a primary page. | partial (uncertainty for topology; no clones) |
| Roux de Bezieux H, Van den Berge K, Street K, Dudoit S. Trajectory inference across multiple conditions with condiments. *Nat Commun* 15:833, 2024. doi:10.1038/s41467-024-44823-0 | Tests for differences in trajectories between conditions. Abstract only. | none |
| Wolf FA, et al. PAGA: graph abstraction reconciles clustering with trajectory inference through a topology preserving map of single cells. *Genome Biol* 20:59, 2019. doi:10.1186/s13059-019-1663-x | Graph of partition connectivity. Abstract describes a connectivity estimate; I did not verify any calibration or significance claim against null data. | none |
| Setty M, et al. Characterization of cell fate probabilities in single-cell data with Palantir. *Nat Biotechnol* 37(4):451-460, 2019. doi:10.1038/s41587-019-0068-4 | Pseudotime plus fate probabilities. Abstract reports validation by comparison with other methods on hematopoiesis; no lineage barcodes mentioned in the abstract. | none |
| Cannoodt R, Saelens W, Saeys Y. Computational methods for trajectory inference from single-cell transcriptomics. *Eur J Immunol*, 2016. doi:10.1002/eji.201646347 | Review of method classes. Abstract only (the Wiley full text returned HTTP 403). | none |

## (d) Benchmarks reporting failures on real data

| Citation | What it shows | Overlap |
|---|---|---|
| Saelens W, Cannoodt R, Todorov H, Saeys Y. A comparison of single-cell trajectory inference methods. *Nat Biotechnol* 37(5):547-554, 2019. doi:10.1038/s41587-019-0071-9 | 45 methods, 110 real and 229 synthetic datasets; best method depends on dataset size and topology. I read the bioRxiv v1 full text (10.1101/276907), not the journal text: real-data gold standards come from sampling origin or FACS-type information, not lineage tracing; stability tests and tests on data with no trajectory are listed there as future work. The published version may differ. | none (benchmarks real data with proxy labels; no clone check, no verdict calibration) |
| Huang K, et al. Benchmarking algorithms for RNA velocity inference. bioRxiv, 2026-01-03. doi:10.64898/2026.01.03.697314 | 29 velocity methods on 114 simulated and 62 real datasets; no method best on all criteria; includes a stability criterion. Abstract only. | none (velocity, not pseudotime or clones) |
| Weinreb et al. 2020 (above) | Barcode-based benchmark of dynamics-inference methods on one system. | partial |

## Verdict

**Partly known.**

Known (do not present as new):
- Using TCR clones or lineage barcodes to check or build trajectories: STARTRAC (2018), LRT (2023), Clonotrace (2025), PhyloTrajectory (2026), Wilson 2022 for CAR-T, Weinreb 2020.
- Shuffling clone labels as a null, including inside strata: STARTRAC-style within-patient shuffle; Swift 2023 within lane and mutation status; LRT cluster shuffle.
- Warning that trajectory methods return a trajectory whether or not one exists, with a no-trajectory null and shuffled-gene negative controls: Tenha and Song 2022.
- Warning that timing and sample size distort clone overlap: Cottrell 2021 (bulk).
- Clones are expression-similar, so clustering is a fair baseline: Wang and Ji 2023 (preprint).
- Trajectory benchmarks rely on proxy labels, not lineage tracing: Saelens 2019 (preprint v1 text).

What I could not find, so what is plausibly new (subject to the search limits below):
1. A clone-concordance score for trajectory lineages checked against three nulls at once (within-patient, pseudotime-stratified, time-point-stratified) plus a no-trajectory k-means baseline, applied to public human CAR-T TCR data across several methods and patients. The finding is that the score is large against the usual within-patient shuffle but falls under half against the time-point shuffle in all 12 runs, and that clustering matches most of it.
2. A reported negative-control calibration failure of a trajectory verdict rule (28 of 31 rated supported), and the decision to cap the verdict instead of retuning it. Tenha and Song ran negative controls on a presence statistic, not on a composite verdict.

Limits of this check: searches used Europe PMC, Crossref, and web search; only abstracts were read for most papers; Clonotrace and PhyloTrajectory controls were not read in full; STARTRAC and CoSpar full texts were not accessible. A reviewer may know a paper I missed. Re-run a search on "clone", "time-matched", "permutation" and "trajectory" in Google Scholar before submission.

## Suggested claim wording

Replace the working sentence with something the repo's numbers support:

> "In four patients' CD8 CAR-T cells (Sheih et al. 2020; 12 per-patient runs of three trajectory methods), the
> agreement between T-cell-receptor clones and the returned lineages is significant against a within-patient
> label shuffle in every run, but the normalised score falls to under half of that value against a
> time-point-stratified shuffle in all 12 runs, and a k-means partition that uses no trajectory matches most
> of it (the lift over k-means is at most 0.05 in absolute value). Separately, a verdict rule that reads only
> coverage and clonal support rated 28 of 31 negative-control runs as supported; we therefore never report
> a supported verdict."

Keep as separate sentences: the Sheih result, and the verdict-rule failure. Do not write "tree-likeness
verdict", "pre-registered" (unless the 31-run check has its own dated declaration; the declaration that
exists covers the Sheih plan), "vanished" or "depth-matched" (say "pseudotime-stratified"). Say "four
patients, one dataset" in the abstract.

## bioRxiv rules for a first submission by an unaffiliated author

Read 2026-11-23. Pages were fetched through a summarising tool, so quotes are fragments (under 15
words). Where the page I fetched did not say something, the line says "not stated", not that the
rule does not exist.

| Rule | What the page says | Page |
|---|---|---|
| Affiliation | Submitters register and "supply an affiliation so there is an entity providing oversight" that bioRxiv can contact. No route is described for someone with no institution, and nothing says whether a non-institutional affiliation (for example a home address or "Independent researcher") is accepted. **Cannot confirm; ask bioRxiv before submitting.** | https://www.biorxiv.org/submit-a-manuscript |
| Who may submit | FAQ: you create an account in the submission system and confirm approval from all co-authors. Eligibility by institution or career stage: not stated. | https://www.biorxiv.org/about/FAQ (item "How do I submit to bioRxiv?") |
| Account / ORCID | The sign-in portal offers "Log in with ORCiD" and also email-and-password login. Whether an ORCID is required: not stated on the pages I could open (the portal is a login wall). | https://submit.biorxiv.org/ |
| Scope | Life sciences; other fields only with "direct relevance to the life sciences". | https://www.biorxiv.org/about-biorxiv |
| Article types | Complete, unpublished manuscripts with New, Confirmatory or Contradictory Results. Reviews, viewpoints and essays that summarise existing work are not appropriate. Tool announcements or protocols alone are not sufficient; a full article with Introduction, Results and Discussion is expected. | https://www.biorxiv.org/about/FAQ (items on content types, reviews, methods) |
| Computational and public-data papers | "bioRxiv welcomes computational papers" if they are full research papers with methods and results. The fetch summary said simple analyses of public data and software announcements without detailed methods generally do not qualify. I did not capture that sentence verbatim, so re-read it. This matters here: the paper reanalyses public data, so it needs to be framed as a methods and calibration study with full methods and the negative-control results. | https://www.biorxiv.org/about/FAQ (item on bioinformatics and computational papers) |
| Clinical content | "Clinical papers should now be submitted to medRxiv". The Sheih data are patient samples, but the study is computational. Whether screeners would redirect it: not stated. | https://www.biorxiv.org/about/FAQ (item on clinical papers) |
| Length | No word, page or file-size limit stated. | https://www.biorxiv.org/submit-a-manuscript |
| Format | One PDF preferred; Word plus figure files accepted; TeX or LaTeX must be converted to PDF first. | https://www.biorxiv.org/submit-a-manuscript and https://www.biorxiv.org/about/FAQ |
| Licence | Author keeps copyright and picks one of CC BY, CC BY-NC, CC BY-ND, CC BY-NC-ND, CC0, or no reuse. Posting means consent to text mining. | https://www.biorxiv.org/submit-a-manuscript |
| Fees | "There is no charge for registration or article deposition" and "no fee to submit". | https://www.biorxiv.org/submit-a-manuscript and https://www.biorxiv.org/about/FAQ |
| Endorsement or sponsorship | Not stated on any page I read; no endorsement requirement appears. Preprints are not peer-reviewed or endorsed by bioRxiv. | https://www.biorxiv.org/about/FAQ |
| Screening | Basic screening for plagiarism, non-scientific content, inappropriate article types, and health or biosecurity risk; volunteer Affiliates help screen. | https://www.biorxiv.org/about-biorxiv and https://www.biorxiv.org/about/FAQ |
| Generative AI | Authors are accountable for all content; describe AI use in the manuscript; AI tools may not be listed as authors. | https://www.biorxiv.org/about/FAQ (item on generative AI) |
| Funding, data, ethics | Funding information is requested in the submission steps; large datasets go to community databases; work not done to ethical standards may be removed. A competing-interest statement, a formal submission checklist, subject-area selection and a corresponding-author field: not stated on the pages I could open. | https://www.biorxiv.org/about/FAQ and https://www.biorxiv.org/submit-a-manuscript |
| After posting | A posted article is citable and cannot be removed (it can be withdrawn with a statement); revisions keep the same DOI. | https://www.biorxiv.org/about/FAQ |

Not found at all (so do not rely on either answer): an ORCID requirement, an "independent researcher"
policy, a submission checklist document, any endorsement requirement. The portal also links a Submission
Guide and Help page that I could not open; check them with an account before submitting.

## Unverified (not opened on a primary page; do not cite from this file)

- TraceSim (NeurIPS 2026 poster page, "A Generative Simulator and Benchmark for Joint scRNA-seq and Lineage Tracing"): only a search snippet.
- Pyro-Velocity (bioRxiv 2022, 10.1101/2022.09.12.507691): snippet only; reported modest agreement with LARRY clonal fates. Not opened.
- Deep Lineage (Cell Systems 2026, S2405-4712(26)00241-3) and "Predictive Multiplicity in Cell-Fate Assignment" (arXiv 2610.11185): snippets only.
- Ventre E, J Math Biol 2026, doi:10.1007/s00285-026-02375-5, "Trajectory inference for a branching SDE model of cell differentiation via lineage tracing": title and DOI appeared in a Europe PMC listing only; abstract not read.
- Schalck A, Cancer Discov 2022, doi:10.1158/2159-8290.cd-21-1248, TIL trajectory in pancreatic cancer: listing only.
- The STARTRAC paper's own Methods wording on its permutation null: the only description I read is the Bio-protocol preprint above, a secondary page by some of the same group; Nature's page was not accessible.
- CoSpar's and Weinreb 2020's full-text controls and metrics: only abstracts read (the Weinreb PMC text request returned HTTP 500).
- Cannoodt 2016 sentence that every method "will always return a trajectory": seen in a search result, not on the Wiley page (HTTP 403). The same point is verified in Tenha and Song 2022.
- Lamian's bootstrap branch detection rate: seen in a search result and in the abstract-level summary only.
- Absence claims: "no reanalysis of GSE125881" and "no stratified clone-null on trajectory lineages" are search findings only.
