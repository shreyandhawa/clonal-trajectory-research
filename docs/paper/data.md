# Datasets: accessions, licences and data-use terms

Read 2026-11-23. The file URLs and SHA-256 values the code uses are in `src/ctr/datasets.py`, and the licence
lines there were read on 2026-11-19. Where a page blocked automated access (GEO and PMC show a reCAPTCHA, Nature
pages a sign-in), the block was not bypassed: GEO facts come from NCBI's E-utilities API instead, and the item is
marked. **UNCONFIRMED** means it was not read on a primary page.

## Summary

| Dataset | Role in the paper | Original deposit | Files used | Terms of the files used |
|---|---|---|---|---|
| Sheih et al. 2020, human CD19 CAR-T, 4 patients | **Main text** (case study) | GEO **GSE125881** (SRA SRP182902); integration-site reads SRA PRJNA589633 | GEO supplementary files `GSE125881_raw.expMatrix.csv.gz`, `GSE125881_RAW.tar` | NCBI places no restriction on use or redistribution; submitters may still hold rights. Article CC BY 4.0 |
| Bastidas-Ponce et al. 2019, mouse pancreas E15.5 | Supplement (calibration) | GEO **GSE132188** (SRA SRP200419) | `endocrinogenesis_day15.h5ad` from github.com/theislab/scvelo_notebooks | **No licence stated** on that repository. The underlying GEO data fall under NCBI's terms |
| Setty et al. 2019, human CD34+ bone marrow | Supplement | HCA project **091cf39b-01bc-42e5-9437-f419a66c8a45**; BioStudies S-SUBS8; ENA ERP120467 / PRJEB37166 | figshare 14465559, file 27686835 | **CC BY 4.0** (figshare); HCA data use: CC BY 4.0, data-use restriction "NRES" (none) |
| Pijuan-Sala et al. 2019, mouse gastrulation, erythroid | Supplement | ArrayExpress **E-MTAB-6967** | figshare 14465562 (v2), file 27686871 | **CC BY 4.0** (figshare). EMBL-EBI places no additional restriction on the deposit |
| Daniel et al. 2022, mouse LCMV CD8 T cells | Not in the paper (declined); in `real-2026-11-20.json` only | GEO **GSE188666** (SuperSeries GSE188670; SRA SRP345737) | GEO supplementary files (nine, listed in `datasets.py`) | NCBI terms, as for Sheih |

## Per dataset, with sources

### Sheih et al. 2020 (main text)

- Paper: Sheih A, et al. *Nat Commun* 11:219, 2020, doi:10.1038/s41467-019-13880-1. Licence **CC BY 4.0**
  (Europe PMC full text of PMC6954177).
- Accession: GSE125881, human, public 2019-11-22, PMID 31924795, SRA SRP182902 (NCBI E-utilities `esummary`,
  db=gds, id 200125881). The paper's data availability statement puts scRNA-seq in GSE125881 and integration-site
  reads in SRA PRJNA589633, and gives TCR data as a Source Data file (Europe PMC full text).
- Controlled access: **none found.** No dbGaP deposit is named. All 32 SRP182902 experiments are "public" with
  anonymous access (E-utilities, db=sra). Samples are from trial NCT01865617, under Fred Hutchinson IRB approval
  (paper). The paper gives no consent or data-use restriction.
- The TCR tables used are the per-sample clonotype files inside `GSE125881_RAW.tar` on GEO, not the Source Data
  file.
- **UNCONFIRMED:** the GEO accession page and GEO's own disclaimer page (both reCAPTCHA). The NCBI terms quoted
  here are from https://www.ncbi.nlm.nih.gov/home/about/policies/: NCBI "places no restrictions on the use or
  distribution of the data", but submitters may claim other rights, which NCBI cannot grant.
- Use in the paper: cite the paper and the accession. The data are human, and only the processed files GEO
  publishes were used. No raw reads were downloaded.

### Bastidas-Ponce et al. 2019 (supplement)

- Paper: *Development* 146:dev173849, 2019. © The Company of Biologists, published under its user licence
  (biologists.com/user-licence-1-1/). No CC licence is shown, and Europe PMC marks it not open access.
  **UNCONFIRMED:** the wording of that user licence (not read).
- Accession: GSE132188, mouse, public 2019-06-11, PMID 31160421 (E-utilities). The paper's statement names
  GSE132188 and puts processed matrices at github.com/theislab/pancreatic-endocrinogenesis.
- Files used: scvelo's preprocessed `endocrinogenesis_day15.h5ad`, from theislab/scvelo_notebooks. That repository
  has **no licence** (GitHub API: no licence file; last push 2021-11-29). scvelo's own `pancreas()` loader cites
  this paper and downloads the same file. scvelo is BSD-3-Clause, which covers its code, not the data.
- Use in the paper: cite the paper, the accession and scvelo as the source of the processed file. Do not
  redistribute the h5ad; the repo already only downloads it.

### Setty et al. 2019 (supplement)

- Paper: *Nat Biotechnol* 37:451-460, 2019, doi:10.1038/s41587-019-0068-4.
- Files used: figshare 14465559 ("human_cd34_bone_marrow.h5ad", one file, 27686835), **CC BY 4.0**, published
  2021-04-22, citing the paper (figshare API, checked again 2026-11-23).
- Original deposit: the paper's statement names HCA project `29f53b7e-071b-44b5-998a-0ae70d0229a4`, which **no
  longer resolves** in the HCA index. The project now listed under the same DOI is
  `091cf39b-01bc-42e5-9437-f419a66c8a45` (BioStudies S-SUBS8, ENA ERP120467 / PRJEB37166, public 2020-03-12), with
  data-use restriction "NRES" and open access (HCA Azul API; ENA portal API). HCA's data-use agreement page says
  its datasets are under CC BY 4.0 (data.humancellatlas.org/about/data-use-agreement).
- Use in the paper: cite the paper and the current HCA project, and note that the paper's project link is dead.

### Pijuan-Sala et al. 2019 (supplement)

- Paper: *Nature* 566:490-495, 2019, doi:10.1038/s41586-019-0933-9.
- Accession: E-MTAB-6967, released 2018-12-05, linked to that DOI (BioStudies API). The record has no licence
  field. EMBL-EBI's terms of use place no additional restriction on use or redistribution, but submitters may
  hold rights (ebi.ac.uk/about/terms-of-use).
- Files used: figshare 14465562 (v2, "erythroid_lineage.h5ad", file 27686871), **CC BY 4.0**. **Caveat:** the
  figshare record cites bioRxiv doi:10.1101/2020.12.21.423773 ("Perspectives in RNA velocity"), not Pijuan-Sala:
  the file holds spliced and unspliced counts reprocessed by that later work. scvelo's `gastrulation_erythroid()`
  cites Pijuan-Sala.
- **UNCONFIRMED:** whether the file was made from E-MTAB-6967 or from a separate deposit by the bioRxiv authors
  (the figshare record does not say); the bioRxiv paper's authors and any published version (not opened); the
  Pijuan-Sala data availability statement (Nature sign-in; PMC CAPTCHA).
- Use in the paper: cite both Pijuan-Sala 2019 (the data) and the bioRxiv work (the processed file). The bioRxiv
  entry must be checked before it goes in the reference list.

### Daniel et al. 2022 (not in the paper)

- Paper: *Nat Immunol* 23:1614-1627, 2022, doi:10.1038/s41590-022-01337-5.
- Accessions: GSE188666 (mouse scRNA-seq, public 2022-07-25, SRA SRP345737, PMID 36289450) and SuperSeries
  GSE188670 (E-utilities).
- **UNCONFIRMED:** the paper's data availability statement and the article licence (Nature sign-in; PMC CAPTCHA);
  GSE188666's SRA access level (not checked).
- The paper does not use these data (declined as a second dataset). If the supplement shows the `real-2026-11-20`
  Daniel rows, cite the paper and the accession.

## What this means for the paper

- Every file used is public, and none is under controlled access as far as these records show. Three are CC BY 4.0
  (bone marrow, gastrulation, Sheih's article). GEO and EMBL-EBI deposits carry no added restriction. The
  pancreas h5ad has no licence on its host.
- No data are redistributed by this repository: `ctr fetch` downloads each file from its host and checks its
  SHA-256.
- The data statement in the draft should list the five accessions above, the two figshare records, the scvelo
  source, and the current HCA project.
- Two references need your check before they are cited: the bioRxiv source of the erythroid file
  (doi:10.1101/2020.12.21.423773), and the replacement HCA project for Setty 2019.
