"""Metadata-only dataset audit; never reads interaction outcomes.

Usage: python3 src/audit_sources.py --phagehost-rbp RBPbase.csv --phagehost-loci Locibase.json --townsend-xml townsend.xml --out audit/metadata-only.json
Inputs: PhageHostLearn Zenodo 11061100 RBPbase and Locibase; Townsend Europe PMC fullTextXML.
"""
import argparse, csv, json, re
from collections import Counter
from xml.etree import ElementTree as ET


def cells(table):
    return [[' '.join(' '.join(c.itertext()).split()) for c in row] for row in table.findall('.//tr')]


def audit(args):
    rbps = list(csv.DictReader(open(args.phagehost_rbp, newline='')))
    loci = json.load(open(args.phagehost_loci))
    root = ET.parse(args.townsend_xml).getroot()
    tables = {t.attrib['id']: cells(t) for t in root.findall('.//table-wrap')}
    if not {'tb1', 'tb2'} <= set(tables):
        raise ValueError('Townsend Table 1 or 2 missing')
    train_phages = {x['phage_ID'] for x in rbps}
    train_hosts = set(loci)
    external_phages = []
    for row in tables['tb2'][1:]:
        if len(row) < 8: continue
        name = row[0].removeprefix('Klebsiella phage ')
        external_phages.append({'phage': name, 'lifecycle_paper': row[2], 'ena_project': row[-1], 'exact_name_in_train': name in train_phages})
    species = ''
    external_hosts = []
    for row in tables['tb1'][1:]:
        if len(row) < 6: continue
        if row[0].startswith('Klebsiella '): species = row[0]
        external_hosts.append({'species': species, 'strain': row[1], 'k_locus': row[2], 'exact_id_in_train': row[1] in train_hosts})
    report = {
      'scope':'metadata-only, no interaction matrix opened; no sequence-homology or resistance proof',
      'train_rbp_records':len(rbps),'train_phages':len(train_phages),'train_hosts':len(train_hosts),
      'townsend_phages':external_phages,'townsend_hosts':external_hosts,
      'exact_phage_name_matches':sum(x['exact_name_in_train'] for x in external_phages),
      'exact_host_id_matches':sum(x['exact_id_in_train'] for x in external_hosts),
      'external_lifecycle_counts':dict(Counter(x['lifecycle_paper'] for x in external_phages)),
      'status':'NOT CLEARED: genome/RBP and host/K-locus homology audit outstanding; resistance phenotypes independently checked for NCTC 13439, 13440, 13442, 13443 only; labels unopened.'}
    with open(args.out,'w') as f: json.dump(report,f,indent=2,sort_keys=True)
    print(json.dumps({k:v for k,v in report.items() if k not in ('townsend_phages','townsend_hosts')},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for opt in ('phagehost-rbp','phagehost-loci','townsend-xml','out'): parser.add_argument('--'+opt,required=True)
    audit(parser.parse_args())
