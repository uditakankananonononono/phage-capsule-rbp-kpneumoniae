#!/usr/bin/env python3
"""Author-training host LOO feature-removal check; NOT mechanistic proof.
Same folds, labels, seed and hyperparameters as train_eval.py; full sanity
must match archived full-model per-host predictions before interpreting deltas.
"""
import argparse, os, json
from pathlib import Path
import numpy as np, pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=0);p.add_argument('--end',type=int,default=None);a=p.parse_args()
root=Path(__file__).resolve().parents[1]; raw=Path(os.environ.get('PHAGE_RAW_DIR','raw'))
df=pd.read_csv(root/'data/work_pairs.csv'); loci=pd.read_csv(raw/'esm2_embeddings_loci.csv',index_col=0);rbp=pd.read_csv(raw/'esm2_embeddings_rbp.csv');rbp_mean=rbp.groupby('phage_ID').mean(numeric_only=True)
L=loci.values.astype(np.float32); B=rbp_mean.values.astype(np.float32)
li={h:i for i,h in enumerate(loci.index)};bi={q:i for i,q in enumerate(rbp_mean.index)}
B=B[[bi[q] for q in df.phage]];L=L[[li[h] for h in df.host]]
y=df.y.values;hid=df.host.values
hosts=df.groupby('host').agg(n=('y','size'),pos=('y','sum'));elig=hosts[(hosts.n>=5)&(hosts.pos>=1)].index.tolist()
outdir=root/'code'/'ablation_parts';outdir.mkdir(exist_ok=True)
for i in range(a.start,min(len(elig),a.end or len(elig))):
 h=elig[i];tr=hid!=h;te=~tr;row={'host':h,'n_tested':int(te.sum()),'n_pos':int(y[te].sum())}
 for key,feature in [('full',np.concatenate([B,L],axis=1)),('rbp_only',B),('locus_only',L)]:
  m=XGBClassifier(n_estimators=60,max_depth=4,learning_rate=.2,subsample=.9,colsample_bytree=.8,eval_metric='logloss',random_state=20260929,n_jobs=8,tree_method='hist')
  m.fit(feature[tr],y[tr]);s=m.predict_proba(feature[te])[:,1];yte=y[te]
  row[key+'_hit5']=int(yte[np.argsort(-s)[:5]].sum()>=1)
  row[key+'_auroc']=float(roc_auc_score(yte,s)) if 0<yte.sum()<len(yte) else None
 pd.DataFrame([row]).to_csv(outdir/f'host_{i:03d}.csv',index=False)
 print(i,h,row['full_hit5'],row['rbp_only_hit5'],row['locus_only_hit5'],flush=True)
