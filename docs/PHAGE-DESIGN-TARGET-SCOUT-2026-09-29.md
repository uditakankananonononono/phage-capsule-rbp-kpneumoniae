# Target and embedding compatibility scout, September 29, 2026

No new locked outcome was opened in this scout. The four publicly listed *K. pneumoniae* reference strains below already occur in the exposed Townsend dataset; **none is a fresh external validation cohort**. Their resistance markers are catalog descriptions, not a verified per-isolate MIC panel or current phenotype. Their capsule types are reported in Townsend Table 1, not independently reconfirmed from assemblies here.

| Public strain | Catalog resistance evidence | Published K-locus type | Candidate status |
| --- | --- | --- | --- |
| NCTC 13439 | VIM-1 metallo-carbapenemase, QnrS1 | KL14 | Public, historically exposed phage outcomes; exploratory target context only |
| NCTC 13440 | VIM-1 metallo-carbapenemase, QnrS1 | KL38 | Public, historically exposed outcomes; host sequence retrieval unresolved |
| NCTC 13442 | OXA-48 carbapenemase | KL110 | Public, historically exposed outcomes; two colony morphotypes in catalog |
| NCTC 13443 | NDM-1 metallo-carbapenemase | KL2 | Public, historically exposed outcomes; host sequence retrieval unresolved; two colony morphotypes |

Primary resistance catalog: https://www.culturecollections.org.uk/products/bacteria-and-mycoplasmas/antimicrobial-resistance-strains/antimicrobial-resistance-reference-strains/ and the individual catalog records (`detail.jsp?collection=nctc&refId=NCTC+13439`, likewise 13440/13442/13443). Published capsule types and host source: https://pmc.ncbi.nlm.nih.gov/articles/PMC8006926/ (Table 1). Existing repository audit `docs/INDEPENDENT-REVIEW-2026-09-29.md` and `docs/FROZEN-GATE-RESULT-2026-09-29.md` contain the exposure limitation. Before locking a design target, resolve public host assembly accession, match isolate/morphotype and resistance evidence to that accession, independently type locus with pinned database, then select by non-outcome criteria. No outcome-based target choice or claim of unseen test is permitted.

## Bounded embedding compatibility preflight

The exact author feature implementation at https://github.com/dimiboeckaerts/PhageHostLearn/blob/main/code/phagehostlearn_features.py specifies `esm.pretrained.esm2_t33_650M_UR50D()`, batch size one, eval mode, layer 33, mean of amino-acid token representations over positions 1..length, `return_contacts=True`, and 1280 dimensions. Public `RBPbase.csv` from https://zenodo.org/records/11061100 (MD5 fc235f3acfcd4dcadb71527bdf6704a3) has 274 protein records, all keyed and order-matched to the deposited 274 x 1280 RBP embedding CSV (SHA-256 c282a434f92b6702d54baa821adcdb563070020e9b9fe29a045a1515e53bc990). All are finite; protein lengths 214..1477 amino acids, no noncanonical amino-acid letters. A bounded selection would use existing short proteins with IDs K17alfa62_gp87 (214 aa), K65PH164_gp148 (215 aa), and K50PH164C1_gp20 (215 aa), predetermined by length not outcome. This preflight verifies **data/schema compatibility only**, not a regenerated embedding.

The exact 650-million-parameter ESM-2 weights alone require roughly 2.6 GB in float32, beyond this 1.9-GiB RAM host, even before activations and Python. PyTorch/ESM are not installed. Running even a single inference here would likely OOM, and swapping in a smaller model would not reproduce 1280-dimensional author vectors. Do not run inference on this host. Need a separate CPU/GPU memory-equipped environment, pinned model weight SHA, package versions, compatible use of token pooling, explicit memory/time/cost ceiling, and a 3-protein maximum for first compatibility test, with predeclared error tolerance against original vectors. This is a heavy-step request to the parent, not an approval to run it.

The author inference notebook itself warns that new-phage predictions were **not evaluated in the study**: https://github.com/dimiboeckaerts/PhageHostLearn/blob/main/code/phagehostlearn_inference.ipynb . Passing vector compatibility would not validate a sequence-designed phage's productive host range or fitness.

## Accession-only follow-up (no sequence values or outcomes opened)

A live ENA assembly **metadata** query, exact strain-field match under *K. pneumoniae* taxon 573 (`https://www.ebi.ac.uk/ena/portal/api/search?result=assembly&query=tax_tree%28573%29%20AND%20%28strain%3D%22NCTC%2013439%22%20OR%20strain%3D%2213439%22%29&fields=accession%2Cstudy_accession%2Cscientific_name%2Cstrain%2Cassembly_name%2Cassembly_type%2Cdescription&format=json&limit=10`, substituting 13440/13442/13443) gave:

- 13439: GCA_020251665 (PRJNA766297; ENA sample SAMN21841528, sample alias P5), plus GCA_054299455 (PRJNA1097786). Two deposits with the same strain label mean the target assembly is not yet unambiguous.
- 13440: no assembly or sample in that exact ENA field query. This is not proof that no genome exists under another alias.
- 13442: GCA_020251505 (PRJNA766297; ENA sample SAMN21841536, alias P13). Catalog warns of two colony morphotypes, with no linkage in these metadata to which morphotype was sequenced.
- 13443: GCA_055659705 (PRJNA1420929; ENA sample SAMN55863828, alias SCL13443, strain field "13443"). Catalog warns of two morphotypes; assembly accession is not enough to bind one phenotype or colony to a design target.

These are **leads, not locked target confirmations**. Genome sequences, Kaptive outputs and resistance alleles/MICs were not read. The catalog's "Link on ENA Database" did not itself yield a parsed accession in the bounded metadata read. Next checks must match specimen alias, catalog lot/morphotype, assembly sequence and Kaptive locus output without looking at historical plaque outcomes. The exposed Townsend matrix cannot validate a design.
