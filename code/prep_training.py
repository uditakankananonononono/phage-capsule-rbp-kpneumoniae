#!/usr/bin/env python3
"""Training-data prep for capsule-aware RBP/K-locus ranking (prereg v0.1.1).
Author training data ONLY (Zenodo 11061100). NaN = untested pair, excluded.
Outputs: code/prep_report.json + interacts parquet-free CSV summaries."""
import pandas as pd, numpy as np, json, os, hashlib
R = '/tmp/deep-research/phage-kp/raw'
M = pd.read_csv(f'{R}/phage_host_interactions.csv', index_col=0)
loci = pd.read_csv(f'{R}/esm2_embeddings_loci.csv', index_col=0)
rbp = pd.read_csv(f'{R}/esm2_embeddings_rbp.csv')
rep = {}
rep['matrix_hosts'], rep['matrix_phages'] = M.shape
rep['cells_tested'] = int((~M.isna()).sum().sum())
rep['cells_positive'] = int((M == 1).sum().sum())
rep['cells_negative'] = int((M == 0).sum().sum())
rep['loci_embed_hosts'] = int(loci.shape[0]); rep['loci_embed_dim'] = int(loci.shape[1])
rep['rbp_rows'] = int(rbp.shape[0])
ph_with_rbp = set(rbp['phage_ID'])
mh, mp = set(M.index), set(M.columns)
rep['hosts_with_loci_embed'] = len(mh & set(loci.index))
rep['hosts_missing_loci_embed'] = sorted(mh - set(loci.index))[:10]
rep['phages_with_rbp_embed'] = len(mp & ph_with_rbp)
rep['phages_missing_rbp_embed'] = sorted(mp - ph_with_rbp)
rep['rbps_per_phage'] = rbp.groupby('phage_ID').size().describe().round(2).to_dict()
# eligible pairs: tested AND both sides have embeddings
ok_h = [h for h in M.index if h in loci.index]
ok_p = [p for p in M.columns if p in ph_with_rbp]
sub = M.loc[ok_h, ok_p]
rep['eligible_pairs'] = int((~sub.isna()).sum().sum())
rep['eligible_hosts'] = len(ok_h); rep['eligible_phages'] = len(ok_p)
rep['eligible_pos'] = int((sub == 1).sum().sum())
# per-host tested-phage counts (hit-rate@5 feasibility, training side)
cnt = (~sub.isna()).sum(axis=1)
pos = (sub == 1).sum(axis=1)
rep['hosts_ge5_tested_ge1_pos'] = int(((cnt >= 5) & (pos >= 1)).sum())
json.dump(rep, open(os.path.join(os.path.dirname(__file__), 'prep_report.json'), 'w'), indent=2)
print(json.dumps(rep, indent=2)[:1500])
