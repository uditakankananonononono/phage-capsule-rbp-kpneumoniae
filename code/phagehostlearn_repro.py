#!/usr/bin/env python3
"""Author-parameter PhageHostLearn training-side LOGOCV, Zenodo 11061100.

Feature order and cluster assignment follow upstream phagehostlearn_features.py
and phagehostlearn_training.ipynb cells 23/30/31. Outputs are *not* external validation.
Unlike upstream v1.5.0, installed xgboost version is recorded at runtime.
"""
import argparse, hashlib, json, os, platform
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn, xgboost
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--raw-dir',type=Path,default=Path(os.environ.get('PHAGE_RAW_DIR','raw')))
parser.add_argument('--start',type=int,default=0);parser.add_argument('--end',type=int,default=None)
parser.add_argument('--threshold',type=float,default=.995)
parser.add_argument('--jobs',type=int,default=2,help='XGBoost CPU threads (does not alter trees or splits)')
parser.add_argument('--output-dir',type=Path,default=ROOT/'code'/'published_repro_parts')
a=parser.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
r=a.raw_dir
names=('esm2_embeddings_loci.csv','esm2_embeddings_rbp.csv','phage_host_interactions.csv','all_loci_score_matrix.txt')
sha={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in names}
loci=pd.read_csv(r/names[0]); rbp=pd.read_csv(r/names[1]); interactions=pd.read_csv(r/names[2],index_col=0)
# Author function averages each phage's RBP protein vectors, appends after locus embedding.
# Sorting phage ids affects only sample order, not fit inputs; XGBoost is order-sensitive,
# so this script gives a deterministic order and discloses the deviation from author's set().
phage=rbp.groupby('phage_ID',sort=True).mean(numeric_only=True)
host_ids=loci.accession.astype(str).tolist(); pair_h=[];pair_p=[];y=[]
for h in host_ids:
 for p in phage.index:
  label=interactions.loc[h,p]
  if pd.notna(label):pair_h.append(h);pair_p.append(p);y.append(int(label))
loci=loci.set_index('accession'); hmat=loci.loc[pair_h].to_numpy(dtype=np.float32)
pmat=phage.loc[pair_p].to_numpy(dtype=np.float32)
X=np.hstack((hmat,pmat)); y=np.asarray(y,dtype=int)
score=np.loadtxt(r/names[3],delimiter='\t'); assert score.shape==(len(host_ids),len(host_ids))
groups=np.full(len(host_ids),-1,dtype=int);gid=0
for i in range(len(host_ids)):
 cluster=np.flatnonzero(score[i]>=a.threshold)
 if groups[i]<0:
  groups[cluster]=gid;gid+=1
assert np.all(groups>=0)
host_group=dict(zip(host_ids,groups)); pg=np.asarray([host_group[h] for h in pair_h])
print('pairs',len(y),'groups',gid,'threshold',a.threshold,'groups of size>1',sum(np.bincount(groups)>1),flush=True)
for g in range(a.start,min(gid,a.end if a.end is not None else gid)):
 tr=pg!=g;te=~tr
 imbalance=y[tr].sum()/(len(y[tr])-y[tr].sum())
 model=XGBClassifier(scale_pos_weight=1/imbalance,learning_rate=.3,n_estimators=250,max_depth=7,n_jobs=a.jobs,eval_metric='logloss',tree_method='auto',random_state=20260929)
 model.fit(X[tr],y[tr]);s=model.predict_proba(X[te])[:,1]
 out=pd.DataFrame({'host':np.asarray(pair_h)[te],'phage':np.asarray(pair_p)[te],'y':y[te],'score':s,'group':g})
 out.to_csv(a.output_dir/f'group_{g:03d}.csv',index=False)
 if (g-a.start)%5==0:print('completed group',g, 'test rows',len(out),flush=True)
meta={'source':'PhageHostLearn published training LOGOCV code, cells 23/30/31','threshold':a.threshold,'groups':gid,'tested_pairs':len(y),'positive_pairs':int(y.sum()),'feature_order':'locus embedding then mean phage RBP embedding','phage_order':'sorted, versus upstream Python set iteration','xgboost':xgboost.__version__,'sklearn':sklearn.__version__,'python':platform.python_version(),'seed':20260929,'n_jobs':a.jobs,'sha256':sha}
(a.output_dir/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
