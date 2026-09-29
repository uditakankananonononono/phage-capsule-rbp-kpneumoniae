#!/usr/bin/env python3
"""Complete-only validation and host-bootstrap paired feature-removal contrasts."""
from pathlib import Path
import json
import numpy as np,pandas as pd
root=Path(__file__).parent
files=sorted((root/'ablation_parts').glob('host_*.csv'))
assert len(files)==131, f'Expected 131 fold outputs; found {len(files)}'
assert [p.stem for p in files]==[f'host_{i:03d}' for i in range(131)]
r=pd.concat((pd.read_csv(p,dtype={'host':str}) for p in files),ignore_index=True)
assert r.host.is_unique and len(r)==131
baseline=pd.read_csv(root/'train_eval_baseline_perhost.csv',dtype={'host':str})
merged=r.merge(baseline,on='host',validate='one_to_one')
assert len(merged)==len(baseline)==131
assert (merged['full_hit5']==merged['hit@5']).all()
assert np.allclose(merged.full_auroc,merged.auroc,atol=1e-12,rtol=0)
assert r['full_hit5'].sum()==103
r.to_csv(root/'ablation_perhost.csv',index=False)
N=10000;seed=20260929;rng=np.random.default_rng(seed);indices=rng.integers(0,len(r),size=(N,len(r)))
out={'scope':'author training-side host-grouped LOO associative feature removal; NOT external validation, mechanism proof or nominated candidate','seed':seed,'bootstrap':'paired host-cluster percentile interval, 10000 resamples, same host indices across arms','hosts':len(r),'full_matches_archived_baseline_perhost':True,'arm':{},'contrast_full_minus':{}}
for arm in ('full','rbp_only','locus_only'):
 out['arm'][arm]={'hit_at_5':float(r[f'{arm}_hit5'].mean()),'hit_hosts':int(r[f'{arm}_hit5'].sum()),'macro_auroc':float(r[f'{arm}_auroc'].mean())}
for arm in ('rbp_only','locus_only'):
 d=np.column_stack((r.full_hit5-r[f'{arm}_hit5'],r.full_auroc-r[f'{arm}_auroc']))
 boot=d[indices].mean(axis=1)
 lo,hi=np.quantile(boot,[.025,.975],axis=0)
 out['contrast_full_minus'][arm]={'hit_at_5_delta':float(d[:,0].mean()),'hit_at_5_ci95':[float(lo[0]),float(hi[0])],'macro_auroc_delta':float(d[:,1].mean()),'macro_auroc_ci95':[float(lo[1]),float(hi[1])]}
(root/'ablation_summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
