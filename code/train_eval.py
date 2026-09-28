#!/usr/bin/env python3
"""Leakage-safe training-side evaluation, prereg v0.1.1:
leave-one-HOST-out over hosts with >=5 tested eligible phages and >=1 positive.
XGBoost (hist) on [mean-RBP | locus] ESM2 features, fixed seed 20260929.
Training data only; external Ghatbale test untouched."""
import pandas as pd, numpy as np, json, time
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
SEED=20260929
R='/tmp/deep-research/phage-kp/raw'
df=pd.read_csv('/tmp/deep-research/phage-kp/work_pairs.csv')
loci=pd.read_csv(f'{R}/esm2_embeddings_loci.csv',index_col=0)
rbp=pd.read_csv(f'{R}/esm2_embeddings_rbp.csv')
rbp_mean=rbp.groupby('phage_ID').mean(numeric_only=True)
L=loci.values.astype(np.float32); B=rbp_mean.values.astype(np.float32)
li={h:i for i,h in enumerate(loci.index)}; bi={p:i for i,p in enumerate(rbp_mean.index)}
X=np.concatenate([B[[bi[p] for p in df.phage]], L[[li[h] for h in df.host]]],axis=1)
y=df.y.values; hid=df.host.values
hosts=df.groupby('host').agg(n=('y','size'),pos=('y','sum'))
elig=hosts[(hosts.n>=5)&(hosts.pos>=1)].index.tolist()
print('eligible held-out hosts:',len(elig),flush=True)
res=[];t0=time.time()
for i,h in enumerate(elig):
    m_te=hid==h; m_tr=~m_te
    m=XGBClassifier(n_estimators=100,max_depth=5,learning_rate=0.15,subsample=0.9,
                    colsample_bytree=0.8,eval_metric='logloss',random_state=SEED,
                    n_jobs=4,tree_method='hist')
    m.fit(X[m_tr],y[m_tr])
    s=m.predict_proba(X[m_te])[:,1]; yte=y[m_te]
    top=np.argsort(-s)[:5]
    hit=1 if yte[top].sum()>=1 else 0
    res.append({'host':h,'n_tested':int(m_te.sum()),'n_pos':int(yte.sum()),'hit@5':hit,
        'auroc':roc_auc_score(yte,s) if 0<yte.sum()<len(yte) else None})
    if (i+1)%20==0: print(i+1,'done',round(time.time()-t0),'s',flush=True)
r=pd.DataFrame(res)
out={'eligible_hosts':len(elig),'mean_hit_at_5':round(float(r['hit@5'].mean()),4),
 'hosts_hit':int(r['hit@5'].sum()),'mean_auroc':round(float(r['auroc'].dropna().mean()),4),
 'auroc_n':int(r['auroc'].notna().sum()),
 'note':'host-grouped LOO on author training data only; XGB hist depth5 n100 seed 20260929'}
json.dump(out,open('repo/code/train_eval_baseline.json','w'),indent=2)
r.to_csv('repo/code/train_eval_baseline_perhost.csv',index=False)
print(json.dumps(out,indent=2),flush=True)
