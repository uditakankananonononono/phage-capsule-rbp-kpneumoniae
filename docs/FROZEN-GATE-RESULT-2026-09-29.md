# Frozen-gate result: CRKP-specific external endpoint (2026-09-29)

Status: **UNEVALUABLE - underpowered before homology exclusions.** This is the locked v0.1/v0.1.2 gate outcome. It is not a win, not a loss for the model, and not evidence about PhageHostLearn. The benchmark comparison was never run and per the frozen protocol must not be substituted with a convenient split.

## Feasibility arithmetic (from the independently transcribed Townsend matrix)

Independent transcription (CSV SHA256 bb1c5c339b1578ed045c48e2ba8c496c778e0bdf7fbc962423731e539f114e2f, 720 cells, no unresolved cells; second pass by same analyst, no third checker). Temperate phages excluded per prereg (Eggy, Pokey, Raw, Ant), leaving 26 lytic phages tested against each host. Carbapenemase-bearing K. pneumoniae hosts matched by exact NCTC number to the Culture Collections AMR reference listing (VIM-1, OXA-48, NDM-1 mechanisms); MIC-level susceptibility remains unverified.

| Host (NCTC) | KL type | Lytic phages tested | Plaque positives | Meets >=1 positive denominator? |
|---|---|---|---|---|
| 13439 | KL14 | 26 | 3 (vB_KoM-Liquor, vB_KpM-KalD, vB_KpM-Mild) | yes |
| 13440 | KL38 | 26 | 1 (vB_KpM-SoFaint) | yes |
| 13442 | KL110 | 26 | 0 | no |
| 13443 | KL2 | 26 | 0 | no |

Clearance (red) and turbid (dark red) cells are NOT plaques per the figure legend and were never counted as positives.

## Why the gate cannot be evaluated

1. The locked primary endpoint scores per-host hit-rate@5 only for hosts with >=5 experimentally tested eligible lytic phages AND >=1 plaque positive, then compares paired mean improvement with a 95% host-cluster bootstrap CI (10,000 resamples, seed 20260929). At most TWO hosts (13439, 13440) meet the positive-denominator rule BEFORE any phage/host homology or safety exclusions. Homology exclusions can only remove candidates, never add hosts.
2. A paired two-host bootstrap cannot support a credible superiority CI. The prereg required recording eligible N and effective power; N=2 is below any defensible threshold, so the gate is declared underpowered/unevaluable rather than evaluated.
3. The frozen host K-locus rule is additionally non-executable for half the CRKP panel: NCBI Assembly searches (2026-09-29) found genomes for NCTC 13439 (GCF_054299455.1, GCF_020251665.1) and NCTC 13442 (GCF_020251505.1), but NONE for NCTC 13440 or NCTC 13443. Per protocol these hosts are marked unresolvable, not silently skipped. Locibase.json contains translated locus proteins only, so the 95%/80% nucleotide rule needs the raw genomes.
4. The RBP-family homology screen requires BLASTP, which is not available in this environment; per the frozen rule, unscoreable sequences are quarantined, not assumed independent. This further blocks any claim of a clean eligible set.

## What this result is and is not

- It IS a legitimate frozen-gate outcome: the only leakage-safe external CRKP candidate cohort found in public data cannot support the locked endpoint.
- It is NOT evidence that capsule-aware ranking fails, that PhageHostLearn wins, or that the four NCTC strains are resistant/susceptible at MIC level.
- Any further Townsend analysis (genus-level arm, same-KL exclusions) is a separately dated EXPLORATORY pivot relative to the opened matrix and cannot be reported as held-out validation.
- Ghatbale et al. 2025 (https://www.nature.com/articles/s41467-025-66062-7) remains a candidate for a properly frozen second validation (11 phages incl. evolved descendants x 59 clinical isolates, spot-lysis endpoint, CRE starred; Table S3 resistance profiles). Provenance/overlap vetting is incomplete; no outcome data from it has been used. It needs its own frozen amendment before any inspection of its matrix cells.
