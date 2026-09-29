# Bounded ESM-2 feature compatibility, September 29, 2026

The first three protein IDs were frozen by shortest length in public author `RBPbase.csv` before inference. Only these three known training RBPs were embedded on the user's free Google Colab **CPU** runtime (12.67 GB total RAM), not on the 1.9-GB local host. The stored notebook is private in the user's Drive, at https://drive.google.com/file/d/12sIFhXg1FhlcX0u16fZ-Bq4SkijbUsrX/view?usp=drivesdk&authuser=uditakankana%40gmail.com ; the authoritative Colab page was https://colab.research.google.com/drive/12sIFhXg1FhlcX0u16fZ-Bq4SkijbUsrX . Source notebook template is recorded below, and a local copy is in `code/phage-compat-3refs.ipynb`. Colab's code cell completed in 69.8 seconds from its printed start, within the 30-minute cap. No novel sequence was embedded, generated or scored. No payment was made.

Pinned run: Python 3.13.15, torch 2.11.0+cpu, fair-esm 2.0.0, pandas 2.2.3, author model `esm2_t33_650M_UR50D`, eval mode, layer 33 token mean (excluding special tokens), one sequence per batch, `return_contacts=True`, torch threads 2. Main model weight SHA-256 `ea9d0522b335a8778dea6535a65301f10208dece28cd5865482b0b1fc446168c` (2,604,537,549 bytes); contact-regression file SHA-256 `8ffe6edbd4173dc8d45c2cd5cb27d43aad77ec26b4c768200c58ae1f96693575` (3,687 bytes). Public input RBPbase MD5 `fc235f3acfcd4dcadb71527bdf6704a3`, reference 274 x 1280 embeddings SHA-256 `c282a434f92b6702d54baa821adcdb563070020e9b9fe29a045a1515e53bc990`. Predeclared criterion was max absolute error <= 1e-4 **and** cosine >= 0.999999, for each 1280-dimensional vector.

| Author protein | Length aa | Max absolute error | Cosine | Criterion |
| --- | ---: | ---: | ---: | --- |
| K17alfa62_gp87 | 214 | 4.76837158203125e-07 | 1.000000028696213 | pass |
| K65PH164_gp148 | 215 | 4.76837158203125e-07 | 0.9999999766270342 | pass |
| K50PH164C1_gp20 | 215 | 4.76837158203125e-07 | 0.9999999918310255 | pass |

Cosine slightly above 1 is floating-point roundoff, not a claim of super-identity. This checks a **three-protein feature pipeline**, not generalization to unseen RBPs, a designed phage, the entire reference matrix, capsid function or clinical fitness. The author's inference notebook https://github.com/dimiboeckaerts/PhageHostLearn/blob/main/code/phagehostlearn_inference.ipynb states new-phage predictions were not evaluated in the study. Targets remain unchosen pending accession and locus/resistance source binding; all four exposed NCTC strains are forbidden as fresh validation.
