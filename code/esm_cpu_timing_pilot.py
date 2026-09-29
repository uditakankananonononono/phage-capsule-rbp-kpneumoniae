#!/usr/bin/env python3
"""Nine public reference RBPs only: ESM-2 CPU resource timing. No design or inference scores."""
import hashlib,json,os,platform,resource,sys,time,urllib.request
from pathlib import Path
import pandas as pd
import numpy as np
import torch,esm
T=time.monotonic(); out=Path('timing-results');out.mkdir(exist_ok=True)
url='https://zenodo.org/api/records/11061100/files/RBPbase.csv/content'
p=out/'RBPbase.csv'; urllib.request.urlretrieve(url,p)
assert hashlib.md5(p.read_bytes()).hexdigest()=='fc235f3acfcd4dcadb71527bdf6704a3'
r=pd.read_csv(p);r['length']=r.protein_sequence.str.len();assert len(r)==274
# Outcome-blind length strata, deterministic three representatives per stratum.
selected=[]
for label,lower,upper in [('short',200,350),('medium',700,800),('long',1300,1500)]:
 band=r[(r.length>=lower)&(r.length<=upper)].sort_values(['length','protein_ID'],kind='stable')
 assert len(band)>=3,(label,len(band))
 # Choose quantile positions in stratum, avoiding an accidental duplicate.
 ix=sorted({0,len(band)//2,len(band)-1});assert len(ix)==3
 selected += [(label,row) for _,row in band.iloc[ix].iterrows()]
print('SELECTED',[(b,x.protein_ID,int(x.length)) for b,x in selected],flush=True)
torch.set_num_threads(4)
model,alphabet=esm.pretrained.esm2_t33_650M_UR50D();model.eval();conv=alphabet.get_batch_converter()
w=Path.home()/'.cache/torch/hub/checkpoints/esm2_t33_650M_UR50D.pt';expected='ea9d0522b335a8778dea6535a65301f10208dece28cd5865482b0b1fc446168c'
assert hashlib.sha256(w.read_bytes()).hexdigest()==expected
print('PINNED',expected,'versions',platform.python_version(),torch.__version__,getattr(esm,'__version__','2.0.0'),flush=True)
rows=[]
for band,row in selected:
 if time.monotonic()-T>17*60: print('STOP: internal 17-minute cap',flush=True);break
 pid=row.protein_ID;seq=row.protein_sequence;start=time.monotonic()
 _,_,tokens=conv([(pid,seq)])
 with torch.no_grad(): result=model(tokens,repr_layers=[33],return_contacts=False)
 vec=result['representations'][33][0,1:len(seq)+1].mean(0).cpu().numpy()
 assert vec.shape==(1280,) and np.isfinite(vec).all()
 elapsed=time.monotonic()-start
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
 item={'stratum':band,'protein_ID':pid,'length_aa':int(row.length),'forward_seconds':round(elapsed,3),'process_peak_rss_mib':round(rss,1),'elapsed_job_seconds':round(time.monotonic()-T,2)}
 rows.append(item);(out/'checkpoint.json').write_text(json.dumps({'completed':rows,'weights_sha256':expected,'source_md5':'fc235f3acfcd4dcadb71527bdf6704a3'},indent=2)+'\n');print('TIMED',item,flush=True)
 del tokens,result,vec
assert len(rows)==9,f'Only {len(rows)} of 9: partial timing, no extrapolation'
print('DONE',time.monotonic()-T,'peak_rss_mib',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,flush=True)
