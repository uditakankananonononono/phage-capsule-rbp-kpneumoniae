#!/usr/bin/env python3
"""Host-resampled percentile bootstrap for previously frozen training LOO results.
This is an uncertainty interval for training-side diagnostics, not a held-out gate.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
p=Path(__file__).parent
r=pd.read_csv(p/'train_eval_baseline_perhost.csv')
assert len(r)==131 and r.host.is_unique and r['hit@5'].sum()==103 and r.auroc.notna().sum()==131
seed=20260929; n=10000
rng=np.random.default_rng(seed)
ix=rng.integers(0,len(r),size=(n,len(r)))
vals=r[['hit@5','auroc']].to_numpy(dtype=float)
boot=vals[ix].mean(axis=1)
lo,hi=np.quantile(boot,[.025,.975],axis=0)
out={'scope':'author-training host-grouped LOO diagnostic only, no external validation or superiority claim','method':'host-cluster percentile bootstrap, 10000 draws with replacement; every held-out host equally weighted','seed':seed,'hosts':len(r),'hit_at_5':{'successes':int(r['hit@5'].sum()),'point':float(vals[:,0].mean()),'ci95':[float(lo[0]),float(hi[0])]},'macro_auroc':{'hosts':int(r.auroc.notna().sum()),'point':float(vals[:,1].mean()),'ci95':[float(lo[1]),float(hi[1])]}}
(p/'training_side_ci.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
