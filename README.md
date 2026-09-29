# CRKP phage host-range triage - evidence status (2026-09-29)

Computational benchmark and contamination audit of existing naturally occurring phages, not a clinical recommendation or an engineered-phage design. **No independently eligible external test remains; no efficacy, safety, or CRKP prediction superiority has been shown.**

## Verified
- Preregistered protocol v0.1, clarifications v0.1.1/v0.1.2 and separately frozen Ghatbale amendment v0.2.0 are archived. Townsend's four carbapenemase-reference hosts yielded plaque-positive counts 3/1/0/0 against 26 lytic phages, so the primary gate is underpowered and unevaluable (`docs/FROZEN-GATE-RESULT-2026-09-29.md`).
- Ghatbale's candidate cohort is excluded under the frozen RBP homology screen, independently corroborated with BLAST+ 2.17.0 (19 qualifying RBP pairs). Its spot-lysis matrix is outcome-exposed; feasibility before homology exclusion is not predictive validation. See `docs/AUDIT-NOTES-2026-09-29.md` and `audit/ghatbale-blast-validation-note-a5464c40.txt`.
- Author training material from Zenodo 11061100 provides 10,006 tested embedding-eligible pairs among 200 hosts and 105 phages, with 333 positive pairs. Of these, 131 hosts have >=5 tested eligible phages and >=1 positive. These counts are descriptive training-side facts, not held-out performance.

## Thin / incomplete
- `code/train_eval.py` is a training-side leave-one-host-out XGBoost prototype, **not the published PhageHostLearn baseline**; it uses a mean RBP embedding plus K-locus embedding. This is a training-side diagnostic, not an independent external validation or superiority test. The executed parameter note was corrected to depth 4, 60 trees (seed 20260929). The earlier reported configuration and original output note said depth 5 / 100 trees; the original docstring did not specify these values. Actual classifier construction used depth 4 / 60; PHAGE_RAW_DIR can point to downloaded Zenodo embeddings. Verified training-side diagnostic: 103/131 hit@5 = 0.7863, mean AUROC 0.8113 across 131 eligible hosts. Its per-host and aggregate artifacts are committed only when pushed; the Drive checkpoint is a backup. These figures do not establish external performance.
- Contamination analysis is a bounded audit with conservative exclusion, not a comprehensive homolog search across every public phage, host and KL locus. Some engine/environment substitutions and incomplete strain/phenotype metadata are disclosed in audit notes.

## Missing / blocked
- A working, independently tested, capsule-aware ranking application, published PhageHostLearn model reproduction on matched candidates, calibrated predictions, mechanism ablation, paired confidence interval and frozen test prediction file.
- Comprehensive curated safety screens (temperate markers, AMR, toxins, virulence and commensal off-target panel) and any justified candidate nomination. **No phage is nominated.** In-silico no-hit would not prove safety.
- Any new independent locked cohort. Check the program-wide EXPOSURE-LEDGER and ask the parent for cross-agent accession exposure review before opening its outcomes. Do not relax the frozen overlap thresholds after seeing these results.

## Reproduction
Input provenance is `source-manifest.tsv` and Zenodo https://zenodo.org/records/11061100 . Download the three specified author embedding/interaction CSVs into a directory and set `PHAGE_RAW_DIR` to it. `data/work_pairs.csv` is in the repo. Run `python3 code/train_eval.py` from repo root with pandas, numpy, xgboost and scikit-learn; the original chunked rerun used the same classifier with seven host-index slices (0:20 ... 120:131), and assembled results in sorted host order. Training diagnostic details and a parameter correction are in `code/train_eval.py`. External matrices are not used to fit or tune a model. This repository is private; it contains public-source sequence material and audit records.
