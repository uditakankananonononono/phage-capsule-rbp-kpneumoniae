# Preregistration amendment v0.2.0 - frozen SECOND external validation (Ghatbale 2025 cohort)
Dated 2026-09-29. Frozen BEFORE any inspection of the outcome matrix (Figure S2 cells). Figure S2 cell values have never been viewed by the analyst; only paper prose (aggregate percentages for evolved-vs-ancestral comparisons, phage activity groupings) and provenance metadata have been read.

## Status of this amendment
This is a SEPARATE frozen test, independent of the v0.1/v0.1.2 Townsend protocol. The Townsend CRKP gate is already declared underpowered/unevaluable (FROZEN-GATE-RESULT-2026-09-29.md) and is unaffected. This amendment does not reopen, replace, or retrospectively patch that outcome.

## Cohort (provenance vetted, audit files committed)
Source: Ghatbale et al. 2025, Nat Commun (https://www.nature.com/articles/s41467-025-66062-7). 11 phages x 59 clinical K. pneumoniae isolates, spot-lysis matrix (Fig S2), isolates Kaptive-typed by authors; 5 CRE isolates (4 of 39 ESBL + 1 of 20 other; starred in Fig S2).

Phage-side vet (audit/ghatbale-genome-audit.json, ghatbale-relatedness-audit.json):
- All 11 deposited genomes fetched from GenBank (PQ621121-PQ621133 range + PQ529758); SHA256 recorded; ZERO exact matches to the 105 PhageHostLearn training genomes or the 30 Townsend genomes; zero name overlap.
- MinHash k=21/sketch=2000 screen vs training genomes, Mash-distance ANI estimate, VIRIDIC 95% species standard (fixed in v0.1.2):
  - LK2 ~97.2% vs K8PH128 -> EXCLUDED (same species as training phage)
  - QTY ~96.9% vs K65PH164 -> EXCLUDED
  - LK3 ~95.8% vs K52PH129C1 -> EXCLUDED
  - Chai ~94.6% vs K48PH164C1 -> QUARANTINED: included ONLY IF a full-alignment confirmation (MMseqs2 nucleotide search, frozen command recorded at execution) shows <95% ANI-equivalent identity to all training genomes; otherwise excluded. This decision procedure is frozen here; the confirmation runs before model scoring, not after outcomes.
  - CLEAN (<=64% estimated ANI vs all training genomes): APV, ACE, LK1, Beam, KL35, Rec, Turmeric (7 phages).
- Only natural ancestral phages are eligible. The 11 deposits are the ancestral panel (paper: evolved/trained isolates of Ace and APV were derived in-study and are NOT among the deposits); evolved descendants are excluded by construction.

Host-side vet (audit/ghatbale-host-nuccore.json):
- 58 WGS isolate genomes under PRJNA1189177 (KP96-KP361 naming series); ZERO strain-name overlap (normalized exact match) with the 200 PhageHostLearn training hosts. Distinct clinical collection.
- Frozen host screen: normalized strain-name identity (done: 0 overlap) + KL-type labels recorded descriptively. If training-host genomes become retrievable, the v0.1.2 K-locus rule (95% identity / 80% length) applies; any host failing it is quarantined, not skipped.

## Endpoint and analysis (all frozen here)
- Positive = COMPLETE lysis only (dark blue in Fig S2). Partial lysis (medium/light blue) and no lysis = negative. Conservative, consistent with the Townsend plaque-only convention.
- Transcription: Fig S2 is image-based (MOESM1 PDF). An independent transcription pass (same protocol as Townsend: analyst transcribes to CSV, SHA256 archived, audit note, single-analyst caveat) runs ONLY AFTER this amendment is committed. Matrix cells are otherwise never inspected.
- Primary arm: the 5 CRE-starred isolates. Per-host hit-rate@5 (top-5 ranked of the eligible clean phages; requires >=5 tested eligible phages AND >=1 complete-lysis positive per host). MINIMUM ELIGIBLE HOSTS = 3; if fewer, the arm is declared underpowered and reported as feasibility-only (no baseline comparison).
- Secondary arm (labeled secondary): full panel of 59 isolates, same rules.
- Comparison: capsule-aware RBP/K-locus ranking model vs PhageHostLearn baseline, both trained on PhageHostLearn author training data ONLY. Paired host-cluster bootstrap, 10,000 resamples, seed 20260929, 95% CI; superiority claimed only if the CI lower bound exceeds 0. Honest negative if not.
- RBP homology independence screen: MMseqs2 (static binary now available in-environment; PhaMMseqs is MMseqs-based, so this is the faithful implementation of the v0.1.2 screen). Frozen thresholds as in v0.1.2 (E<=0.001, >=60% coverage, >=60% length); any unscoreable phage is quarantined, never assumed independent.
- Safety screen (frozen): before nomination, each candidate phage genome is screened for temperate markers (integrase/excisionase/repressor), toxin, AMR, and virulence cargo via annotation search; any hit excludes the phage from nomination and is recorded. Lytic-only candidates advance.
- No wet-lab, clinical, or deployment claims; computational ranking evaluation only.

## What this amendment cannot do
It cannot resurrect the Townsend gate, cannot use Fig S2 knowledge beyond what is stated above, and cannot count partial lysis as success. Any change to cohort, endpoint, or thresholds after matrix transcription ships as a new dated amendment.
