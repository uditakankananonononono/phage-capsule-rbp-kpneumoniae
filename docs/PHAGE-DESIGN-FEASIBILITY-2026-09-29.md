# Design feasibility memo, September 29, 2026

**Requested change:** investigate computational creation of phage candidates aimed at resistant *K. pneumoniae*. This memo is a decision point before generation, compute or any candidate release. It contains no designed sequence or candidate nomination. Existing benchmark gates and safety limitations still apply.

## What the existing model can and cannot do

PhageHostLearn uses host K-locus embeddings concatenated with mean receptor-binding-protein (RBP) embeddings. Our complete 133-group, 10,006-pair training-side reimplementation is documented in `docs/PHASE3-BASELINE-2026-09-29.md`. It consumes author-supplied ESM-2 embeddings of **existing** protein sequences, not an RBP or whole-genome sequence directly. A novel sequence would require a defined protein annotation/segmentation and the identical ESM-2 model/tokenization/pooling and feature orientation before inference, plus checks for embedding distribution shift. The current 95/131 hit@5 and 0.7153 macro AUROC are training-side diagnostics; they cannot be used as predicted fitness of a designed phage. Host-range prediction is not capsid assembly, growth, burst size, bactericidal activity, therapeutic fitness or absence of transduction.

## Candidate research tracks (not execution instructions)

| Track | Research question | Main uncertainty and gate |
| --- | --- | --- |
| RBP/tail-fiber conceptual design | Can a sequence-level hypothesis yield an RBP that changes capsule recognition while remaining compatible with a natural phage background? | Separate binding from productive infection. Both genotype-to-phenotype link and compatible phage context require experimental validation; no reference background is currently safety-cleared. |
| Capsid conceptual design | Is there a reason to change a capsid instead of an RBP for the stated host-range goal? | Capsid alterations are not directly represented in this baseline and cannot receive a validated host-range/fitness score from it. Do not infer function from structural plausibility alone. |
| Non-generative comparator | How do naturally observed, annotated RBPs rank for a specified host under a strictly training-only model? | Comparator is not a new phage and has no safety clearance; can measure pipeline behavior without claiming design efficacy. |

The evidence supports researching the RBP path first, because capsule specificity has published mechanistic and empirical support, but not a direct path from sequence to therapeutic phage. Primary sources: PhageHostLearn https://www.nature.com/articles/s41467-024-48675-6 and author code https://github.com/dimiboeckaerts/PhageHostLearn ; modular RBP work https://journals.asm.org/doi/10.1128/mbio.00455-21 ; depolymerase capsule-specificity dataset and limitations https://www.nature.com/articles/s41467-025-63861-w ; diversity and cross-reactivity limits https://pmc.ncbi.nlm.nih.gov/articles/PMC11652154/ .

## Research design before a compute run

1. Define intended clinical isolate context without claiming a strain or capsule type not supplied by the user. Freeze host accession, resistance phenotype provenance and receptor/K-locus characterization before any scoring. If no suitable isolate, restrict work to an explicit public training-side *method demonstration*, not a resistant-*K. pneumoniae* therapy claim.
2. Freeze an evaluation spec before model or candidate selection: sources and hashes; training/phage-family/host-locus partitions; forbidden overlap thresholds; design inputs; candidate counts; metrics and baselines; uncertainty and out-of-distribution checks; negative-control logic; and stopping conditions. Compare on a newly qualified, genuinely unseen external assay only if the parent confirms cohort-wide exposure and the locked protocol is preregistered *before* its outcomes are opened. Townsend remains outcome-exposed/underpowered; Ghatbale is homology-excluded. No post-hoc threshold change or reuse as a fresh test.
3. Prototype a **read-only** feature/embedding compatibility test against known RBPs, comparing regenerated embeddings bitwise or within a predeclared tolerance to author CSVs. If this fails, do not score designed sequences. Fit a final baseline model only on authorized training data and report why LOGOCV fold predictions do not constitute an inference model. Reject missing structural metadata, ambiguous sequence boundaries and out-of-distribution inputs rather than extrapolating silently.
4. Keep generation separate from scoring and safety review. Any ranked computational hypotheses must show uncertainty, model applicability, comparator provenance, and explicit "unvalidated in silico" labels, with no claims of productive infection, fitness, efficacy or safety. The heavy generation and embedding run require a separate plan and parent's green-light first.
5. Before any nomination, confirm complete genome/end provenance for a proposed phage context; curated AMR/toxin/virulence and lifecycle review; defined beneficial-commensal panel; and external biological testing by qualified collaborators. Current limited protein-only cargo screen on 105 references (`docs/PHASE3-SAFETY-LIMITS-2026-09-29.md`) returned no database reports but is not a clearance. Source for AMR database method: https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/ .

## Compute authorization boundary

No heavy compute starts from this memo. A proposed small read-only compatibility check would cover a handful of existing author RBPs with pinned ESM-2 model revision, exact preprocessing, input hashes, expected numeric tolerance, wall-clock/memory estimate and abort-on-mismatch; on this 2-CPU, 1.9-GiB local host, ESM-2 and especially generative models may require a separately approved larger environment. Before generation, return an explicit model/license/source, candidate-count cap, infrastructure, estimated time/cost, privacy, and failure/stop conditions to the parent for approval. Never substitute unsupported embedding values or use the completed LOGOCV output as a novel-sequence score.

## Current decision

**Feasible as a staged research program, not yet executable as ranked therapeutic phage designs.** Missing: specified target host/resistance profile, validated sequence-to-embedding path, qualified/safety-reviewed phage context, prospective assay and adequate compute. We should not invent sequences, rank candidates as fit, or nominate any phage from the current evidence.
