#!/usr/bin/env python3
"""Genome availability/completeness triage only. NEVER a safety clearance."""
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
import json, hashlib, os
import pandas as pd
r=Path(os.environ.get('PHAGE_RAW_DIR','raw'))
z=r/'phages_genomes.zip'
expected='f43159fd3473e2d22a56fec27e8d443c'
assert hashlib.md5(z.read_bytes()).hexdigest()==expected
rbp=set(pd.read_csv(r/'esm2_embeddings_rbp.csv').phage_ID)
with ZipFile(z) as archive:
 files={Path(n).stem:n for n in archive.namelist() if n.startswith('phages_genomes/') and n.endswith(('.fasta','.fa','.fna')) and not Path(n).name.startswith('._')}
 entries=[]
 for name in sorted(rbp):
  path=files.get(name)
  if path:
   raw=archive.read(path).decode('utf-8')
   headers=[line for line in raw.splitlines() if line.startswith('>')]
   letters=''.join(line.strip() for line in raw.splitlines() if not line.startswith('>')).upper()
   entries.append({'phage':name,'genome_present':True,'contigs':len(headers),'bases':len(letters),'ambiguous_bases':sum(ch not in 'ACGT' for ch in letters),'ends_verified':False,'lifecycle_verified':False,'amr_toxin_virulence_screen_verified':False,'commensal_panel_verified':False,'eligible_for_nomination':False})
  else: entries.append({'phage':name,'genome_present':False,'contigs':None,'bases':None,'ambiguous_bases':None,'ends_verified':False,'lifecycle_verified':False,'amr_toxin_virulence_screen_verified':False,'commensal_panel_verified':False,'eligible_for_nomination':False})
 out={'scope':'Author training phages, availability/QC only, NOT curated cargo, lifestyle or off-target screening','genome_zip_md5':expected,'phages_with_rbp':len(rbp),'genome_present':sum(e['genome_present'] for e in entries),'multi_contig':sum((e['contigs'] or 0)>1 for e in entries),'nomination_count':0,'reason':'No verified curated AMR/toxin/virulence/lifestyle screen, genome closure or prespecified commensal panel; no external eligible test','entries':entries}
Path(__file__).with_name('safety_inventory.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items() if k!='entries'})
