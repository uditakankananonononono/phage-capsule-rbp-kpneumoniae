#!/usr/bin/env python3
"""Verify every published-style LOGOCV prediction against author inputs; summarize training-side only."""
import gzip, hashlib, io, json, os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parents[1]
raw=Path(os.environ.get('PHAGE_RAW_DIR','raw'))
part=ROOT/'code'/'published_repro_parts'
meta=json.loads((part/'metadata.json').read_text())
assert meta['groups']==133 and meta['tested_pairs']==10006 and meta['positive_pairs']==333 and meta['threshold']==.995
for n,sha in meta['sha256'].items():assert hashlib.sha256((raw/n).read_bytes()).hexdigest()==sha,n
files=sorted(part.glob('group_*.csv'))
assert [p.name for p in files]==[f'group_{i:03d}.csv' for i in range(133)]
frames=[]
for g,p in enumerate(files):
 d=pd.read_csv(p,dtype={'host':str,'phage':str});assert list(d.columns)==['host','phage','y','score','group']
 assert len(d)>0 and d.group.eq(g).all() and d.score.between(0,1).all() and d[['host','phage']].duplicated().sum()==0
 frames.append(d)
d=pd.concat(frames,ignore_index=True)
assert len(d)==10006 and d.y.sum()==333 and d[['host','phage']].duplicated().sum()==0 and d.host.nunique()==200 and d.phage.nunique()==105
inter=pd.read_csv(raw/'phage_host_interactions.csv',index_col=0)
for h,p,y in zip(d.host,d.phage,d.y):assert int(inter.loc[h,p])==y,(h,p)
loci=pd.read_csv(raw/'esm2_embeddings_loci.csv').accession.astype(str).tolist(); score=np.loadtxt(raw/'all_loci_score_matrix.txt',delimiter='\t')
groups=np.full(len(loci),-1,dtype=int);gid=0
for i in range(len(loci)):
 cluster=np.flatnonzero(score[i]>=.995)
 if groups[i]<0:groups[cluster]=gid;gid+=1
assert gid==133
host_group=dict(zip(loci,groups))
assert all(host_group[h]==g for h,g in zip(d.host,d.group))
by=[]
for h,x in d.groupby('host',sort=True):
 eligible=len(x)>=5 and x.y.sum()>=1
 if not eligible:continue
 # Stable tie-order matches sorted phage order from the source script.
 ranked=x.sort_values(['score','phage'],ascending=[False,True],kind='stable')
 by.append({'host':h,'group':int(x.group.iloc[0]),'tested':len(x),'positive':int(x.y.sum()),'hit_at_5':int(ranked.y.iloc[:5].sum()>0), 'auroc':roc_auc_score(x.y,x.score) if x.y.sum()<len(x) else None})
per=pd.DataFrame(by)
assert len(per)==131 and per.host.is_unique
v=per[['hit_at_5','auroc']].to_numpy(float); rng=np.random.default_rng(20260929); ix=rng.integers(0,len(per),size=(10000,len(per))); boot=np.nanmean(v[ix],axis=1); ci=np.nanquantile(boot,[.025,.975],axis=0)
result={'scope':'complete author-parameter PhageHostLearn 0.995 LOGOCV, author training only; not exact original environment or external validation','groups':133,'hosts':200,'pairs':10006,'positive_pairs':333,'eligible_hosts_for_descriptive_hit_at_5':len(per),'eligible_criterion':'host >=5 tested and >=1 positive; not author notebook aggregate, only supplementary same-denominator description','eligible_hit_at_5':{'hits':int(per.hit_at_5.sum()),'point':float(per.hit_at_5.mean()),'host_bootstrap_ci95':ci[:,0].tolist()},'eligible_macro_host_auroc':{'hosts_defined':int(per.auroc.notna().sum()),'point':float(per.auroc.mean()),'host_bootstrap_ci95':ci[:,1].tolist()},'pooled_pair_auroc_all_200_hosts':float(roc_auc_score(d.y,d.score)),'seed':20260929,'bootstrap_draws':10000,'environment':{k:meta[k] for k in ('python','xgboost','sklearn','n_jobs','seed','phage_order')},'source_sha256':meta['sha256'],'prediction_sha256':hashlib.sha256(d.to_csv(index=False).encode()).hexdigest()}
(ROOT/'code'/'published_repro_summary.json').write_text(json.dumps(result,indent=2)+'\n')
per.to_csv(ROOT/'code'/'published_repro_perhost.csv',index=False)
# Commit complete pair predictions as deterministic gzip, rather than partial fold files.
with (ROOT/'code'/'published_repro_predictions.csv.gz').open('wb') as f:
 with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as z:z.write(d.to_csv(index=False).encode())
print(json.dumps(result,indent=2))
