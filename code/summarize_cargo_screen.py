#!/usr/bin/env python3
"""Summarize a limited AMRFinderPlus protein-only screen, without safety clearance."""
import hashlib,json,os
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
raw=Path(os.environ.get('PHAGE_RAW_DIR','raw'))
result=Path(os.environ.get('PHAGE_SCREEN_DIR','/home/sandbox/phage-safety'))
phages=sorted(pd.read_csv(raw/'esm2_embeddings_rbp.csv').phage_ID.unique())
assert len(phages)==105
assert hashlib.md5((raw/'phages_genomes.zip').read_bytes()).hexdigest()=='f43159fd3473e2d22a56fec27e8d443c'
cols=['Protein id','Element symbol','Element name','Scope','Type','Subtype','Class','Subclass','Method','Target length','Reference sequence length','% Coverage of reference','% Identity to reference','Alignment length','Closest reference accession','Closest reference name','HMM accession','HMM description']
entries=[]
for name in phages:
 p=result/(name+'.tsv');log=result/(name+'.log');orf=result/(name+'.prot.fa')
 assert p.exists() and log.exists() and orf.exists(),name
 assert 'amrfinder took ' in log.read_text() and 'ERROR' not in log.read_text(),name
 d=pd.read_csv(p,sep='\t'); assert list(d.columns)==cols,(name,list(d.columns))
 entries.append({'phage':name,'predicted_orfs':sum(x.startswith('>') for x in orf.open()),'reported_hits':len(d),'types':d.Type.value_counts().to_dict(),'report_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out={'scope':'LIMITED curated cargo search of 105 author-training phage genomes; NOT safety clearance','input_zip_md5':'f43159fd3473e2d22a56fec27e8d443c','tool':'NCBI AMRFinderPlus 4.2.7 --plus protein-only search of Prodigal 2.6.3 meta predicted ORFs; no nucleotide blastx (OOM)','database':'NCBI AMRFinderPlus 2026-08-07.1','records_succeeded':len(entries),'reported_hits_total':sum(x['reported_hits'] for x in entries),'entries':entries,'limits':'No hit means only no report under these reference database, protein calling and cutoff settings; missing ORFs, novel cargo, toxin outside this database, unverified genome ends and incomplete curated viral lifecycle coverage remain. No phage is cleared. Commensal off-target panel and lifecycle-specific tools were not run.','nomination_count':0}
(ROOT/'code'/'cargo_screen_limited.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(entries),out['reported_hits_total'],sum(e['predicted_orfs'] for e in entries))
