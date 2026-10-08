# Phase 2: author-baseline attempt, training-side uncertainty and safety status

## Boundaries
No new independent outcome cohort was opened. The program-wide `science-program-ledger/EXPOSURE-LEDGER.md` was read before this work: Townsend outcomes are exposed; Ghatbale remains excluded by the frozen RBP rule. The 131-host results are author-training leave-one-host-out diagnostics, **not external validation**, an efficacy finding, or a comparison showing superiority over the published baseline. No phage nominated.

## Published PhageHostLearn reproduction: complete archived outputs

The historical 2/133 checkpoint has been superseded by complete 133-group prediction artifacts. See `PHASE3-BASELINE-2026-09-29.md` and `RETROSPECTIVE-AUDIT-2026-10-08.md`. The latter independently recomputes archived metrics and validates every label/group against newly downloaded author bytes; it does not rerun fitted models. On 131 descriptively eligible author-training hosts, hit@5 is 95/131 and macro host AUROC 0.7153; pooled pair AUROC across 200 hosts is 0.7513. This is an author-parameter reimplementation, not an exact original-runtime replication or external validation. Its locus-group split differs from the prototype's host-wise split; no fair paired superiority finding follows.

## Frozen training diagnostic: host-bootstrap uncertainty
On `code/train_eval_baseline_perhost.csv`, `code/training_side_ci.py` draws 10,000 host clusters with replacement using seed 20260929; percentile 2.5%/97.5%, equal host weights. The 131-host verified prototype has 103 hits, hit@5 = 0.78626 (95% bootstrap CI 0.70992 to 0.85496), macro AUROC = 0.81132 (95% CI 0.76454 to 0.85520). All 131 hosts had defined AUROC. The CI covers resampling variability in this **author training-side LOO sample**, not data-source shift, phage-cluster leakage, or external superiority. This is not a paired improvement CI under the frozen external gate.

## Safety screen status
`code/safety_inventory.py` verifies the deposited phage-genome archive MD5 f43159fd3473e2d22a56fec27e8d443c and inventories genome availability for the 105 author-training phages with RBP embeddings (105/105 present, 0 multi-record FASTAs, two FASTAs with ambiguous letters). This is **not a curated safety screen**: one FASTA record does not prove a complete genome or verified ends, and no complete safety clearance is supported. A later protein-only cargo summary reports 105 searches/zero hits, but raw reports/logs/ORFs are absent from the repository and execution is not independently certified in the October 8 audit. No validated lifecycle or beneficial-commensal off-target result is archived. All 105 records are unverified and fail nomination readiness. Neither no-hit nor predicted narrow range would prove safety. No candidate names, therapy suggestion, sequence designs, or laboratory actions follow from this inventory.

## Mechanism feature removal: completed on author-training LOO only
`code/mechanism_ablation.py` retrains all 131 held-out-host folds using the prototype hyperparameters on full `[mean RBP | locus]`, RBP-only, and locus-only inputs. `code/summarize_ablation.py` verifies exact full-arm **per-host** hit@5 and AUROC equality to `code/train_eval_baseline_perhost.csv` for every host, requires all 131 fold files, and writes reproducible results to `code/ablation_perhost.csv` and `code/ablation_summary.json`. Pair-level labels and folds are unchanged, and all uncertainty intervals resample the *same* 131 hosts in 10,000 paired percentile-bootstrap draws (seed 20260929).

| Training-side arm | Host hit@5 | Macro host AUROC |
|---|---:|---:|
| Full prototype | 103/131 = 0.7863 | 0.8113 |
| RBP-only | 86/131 = 0.6565 | 0.6941 |
| Locus-only | 16/131 = 0.1221 | 0.5000 |

Full minus RBP-only paired host hit@5 difference 0.1298 (95% bootstrap CI 0.0458-0.2137); macro AUROC difference 0.1172 (0.0825-0.1539). Full minus locus-only hit difference 0.6641 (0.5725-0.7557); AUROC difference 0.3113 (0.2645-0.3552). **Interpretation guard:** for a single held-out host, locus-only features are identical across all candidate phages. Its AUROC 0.5 follows structurally, and its hit@5 reflects an arbitrary input-order tie break. Do not infer a biological receptor mechanism from this trivial no-phage arm. The full-vs-RBP-only difference suggests host-locus features aid this author-training diagnostic, but does not establish physical capsule binding, cross-cohort transport, a comparable published-baseline improvement, or clinical use.

