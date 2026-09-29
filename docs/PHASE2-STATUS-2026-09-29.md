# Phase 2: author-baseline attempt, training-side uncertainty and safety status

## Boundaries
No new independent outcome cohort was opened. The program-wide `science-program-ledger/EXPOSURE-LEDGER.md` was read before this work: Townsend outcomes are exposed; Ghatbale remains excluded by the frozen RBP rule. The 131-host results are author-training leave-one-host-out diagnostics, **not external validation**, an efficacy finding, or a comparison showing superiority over the published baseline. No phage nominated.

## Published PhageHostLearn reproduction: attempted, not finished
Public author source: https://github.com/dimiboeckaerts/PhageHostLearn (`code/phagehostlearn_training.ipynb`, cells 23, 30, 31, and `code/phagehostlearn_features.py`); author inputs: https://zenodo.org/records/11061100 . The source specifies 0.995 locus-score clustering, leave-one-group-out, averaged RBP embeddings concatenated **after** locus embeddings, and XGBoost with per-fold positive-weight correction, learning rate .3, 250 estimators and depth 7. All needed processed inputs are public. This is not an unavailable-public-artifact case.

`code/phagehostlearn_repro.py` attempts these operations with SHA-256 input provenance, a deterministic sorted-phage order, a fixed seed and explicit installed versions. It is not bit-identical to the author run: the original uses unordered Python `set` enumeration of phages, unspecified XGBoost random state, and XGBoost 1.5.0/Scikit-learn 0.24.2 on Python 3.9.7; this environment has XGBoost 3.2.0/Scikit-learn 1.7.2/Python 3.11. It thus is an author-parameter reimplementation rather than an exact original-environment replication. Local 2-CPU, 1.9-GiB run completed just two of 133 clusters in ~105 sec before the 120-second call limit. Partial predictions are not a baseline estimate. A complete 133-cluster author baseline (especially on **matched external candidates**) remains missing, and external comparison is unevaluable because both existing cohorts are closed. Do not compare two training-side scores as if paired external validation.

## Frozen training diagnostic: host-bootstrap uncertainty
On `code/train_eval_baseline_perhost.csv`, `code/training_side_ci.py` draws 10,000 host clusters with replacement using seed 20260929; percentile 2.5%/97.5%, equal host weights. The 131-host verified prototype has 103 hits, hit@5 = 0.78626 (95% bootstrap CI 0.70992 to 0.85496), macro AUROC = 0.81132 (95% CI 0.76454 to 0.85520). All 131 hosts had defined AUROC. The CI covers resampling variability in this **author training-side LOO sample**, not data-source shift, phage-cluster leakage, or external superiority. This is not a paired improvement CI under the frozen external gate.

## Safety screen status
`code/safety_inventory.py` verifies the deposited phage-genome archive MD5 f43159fd3473e2d22a56fec27e8d443c and inventories genome availability for the 105 author-training phages with RBP embeddings (105/105 present, 0 multi-record FASTAs, two FASTAs with ambiguous letters). This is **not a curated safety screen**: one FASTA record does not prove a complete genome or verified ends, and no curated lysogeny, AMR, toxin, virulence, or beneficial-commensal off-target search was executed. All 105 records are unverified and fail nomination readiness. Neither no-hit nor predicted narrow range would prove safety. No candidate names, therapy suggestion, sequence designs, or laboratory actions follow from this inventory.

## Mechanism feature removal: completed on author-training LOO only
`code/mechanism_ablation.py` retrains all 131 held-out-host folds using the prototype hyperparameters on full `[mean RBP | locus]`, RBP-only, and locus-only inputs. `code/summarize_ablation.py` verifies exact full-arm **per-host** hit@5 and AUROC equality to `code/train_eval_baseline_perhost.csv` for every host, requires all 131 fold files, and writes reproducible results to `code/ablation_perhost.csv` and `code/ablation_summary.json`. Pair-level labels and folds are unchanged, and all uncertainty intervals resample the *same* 131 hosts in 10,000 paired percentile-bootstrap draws (seed 20260929).

| Training-side arm | Host hit@5 | Macro host AUROC |
|---|---:|---:|
| Full prototype | 103/131 = 0.7863 | 0.8113 |
| RBP-only | 86/131 = 0.6565 | 0.6941 |
| Locus-only | 16/131 = 0.1221 | 0.5000 |

Full minus RBP-only paired host hit@5 difference 0.1298 (95% bootstrap CI 0.0458-0.2137); macro AUROC difference 0.1172 (0.0825-0.1539). Full minus locus-only hit difference 0.6641 (0.5725-0.7557); AUROC difference 0.3113 (0.2645-0.3552). **Interpretation guard:** for a single held-out host, locus-only features are identical across all candidate phages. Its AUROC 0.5 follows structurally, and its hit@5 reflects an arbitrary input-order tie break. Do not infer a biological receptor mechanism from this trivial no-phage arm. The full-vs-RBP-only difference suggests host-locus features aid this author-training diagnostic, but does not establish physical capsule binding, cross-cohort transport, a comparable published-baseline improvement, or clinical use.

