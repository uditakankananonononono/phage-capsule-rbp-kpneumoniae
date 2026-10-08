#!/usr/bin/env python3
"""Audit existing public diagnostic outputs. Never fit models or design sequences.
Requires numpy and pandas. Optional --raw-dir verifies author labels and hashes.
"""
import argparse, gzip, hashlib, json, platform
from zipfile import ZipFile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def auc(y, score):
    y = np.asarray(y, dtype=int)
    positive = int(y.sum())
    negative = len(y) - positive
    if not positive or not negative:
        return None
    ranks = pd.Series(np.asarray(score)).rank(method='average').to_numpy()
    return float((ranks[y == 1].sum() - positive * (positive + 1) / 2) / (positive * negative))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-dir', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT/'audit/retrospective-check-2026-10-08.json')
    args = parser.parse_args()
    paths = ['data/work_pairs.csv', 'code/train_eval_baseline_perhost.csv',
             'code/ablation_perhost.csv', 'code/published_repro_perhost.csv',
             'code/published_repro_predictions.csv.gz', 'code/safety_inventory.json',
             'code/cargo_screen_limited.json']
    result = {'scope': 'retrospective arithmetic, coverage and provenance only; no model refit, design, efficacy or safety clearance',
              'audit_environment': {'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__},
              'artifact_sha256': {p: sha(ROOT/p) for p in paths}, 'checks': {}}
    c = result['checks']
    pairs = pd.read_csv(ROOT/'data/work_pairs.csv', dtype={'host':str, 'phage':str})
    assert len(pairs) == 10006 and pairs.y.sum() == 333
    assert not pairs[['host','phage']].duplicated().any()
    assert set(pairs.y) == {0,1}
    counts = pairs.groupby('host').y.agg(['size','sum'])
    eligible = counts[(counts['size'] >= 5) & (counts['sum'] >= 1)].index
    assert len(eligible) == 131
    base = pd.read_csv(ROOT/'code/train_eval_baseline_perhost.csv', dtype={'host':str}).sort_values('host')
    ab = pd.read_csv(ROOT/'code/ablation_perhost.csv', dtype={'host':str}).sort_values('host')
    assert base.host.is_unique and ab.host.is_unique
    assert set(base.host) == set(ab.host) == set(eligible)
    assert np.array_equal(base['hit@5'], ab.full_hit5)
    assert np.allclose(base.auroc, ab.full_auroc, atol=1e-12, rtol=0)
    assert np.array_equal(base.n_tested, counts.loc[base.host,'size'])
    assert np.array_equal(base.n_pos, counts.loc[base.host,'sum'])
    assert base['hit@5'].sum() == 103
    assert base.auroc.between(0,1).all()
    rng = np.random.default_rng(20260929)
    ix = rng.integers(0,131,size=(10000,131))
    values = base[['hit@5','auroc']].to_numpy(float)
    ci = np.quantile(values[ix].mean(axis=1), [.025,.975], axis=0)
    original_ci = json.loads((ROOT/'code/training_side_ci.json').read_text())
    assert np.allclose(ci[:,0], original_ci['hit_at_5']['ci95'])
    assert np.allclose(ci[:,1], original_ci['macro_auroc']['ci95'])
    c['prototype'] = {'eligible_hosts':131,'hits':103,'hit_at_5':float(values[:,0].mean()),
                      'macro_auroc':float(values[:,1].mean()),'hit_ci95':ci[:,0].tolist(),
                      'auroc_ci95':ci[:,1].tolist(), 'full_ablation_matches_all_archived_host_metrics':True,
                      'pair_scores_archived':False, 'model_refit_performed':False}
    c['ablation'] = {}
    published_ablation = json.loads((ROOT/'code/ablation_summary.json').read_text())
    for arm in ['full','rbp_only','locus_only']:
        point = {'hits':int(ab[f'{arm}_hit5'].sum()),'hit_at_5':float(ab[f'{arm}_hit5'].mean()),
                 'macro_auroc':float(ab[f'{arm}_auroc'].mean())}
        assert np.isclose(point['macro_auroc'],published_ablation['arm'][arm]['macro_auroc'])
        assert point['hits'] == published_ablation['arm'][arm]['hit_hosts']
        c['ablation'][arm] = point
        if arm != 'full':
            delta = np.column_stack((ab.full_hit5-ab[f'{arm}_hit5'],ab.full_auroc-ab[f'{arm}_auroc']))
            bounds = np.quantile(delta[ix].mean(axis=1),[.025,.975],axis=0)
            claimed = published_ablation['contrast_full_minus'][arm]
            assert np.allclose(bounds[:,0],claimed['hit_at_5_ci95'])
            assert np.allclose(bounds[:,1],claimed['macro_auroc_ci95'])
    predpath = ROOT/'code/published_repro_predictions.csv.gz'
    pred = pd.read_csv(predpath, dtype={'host':str,'phage':str})
    claimed = json.loads((ROOT/'code/published_repro_summary.json').read_text())
    decompressed_hash = hashlib.sha256(gzip.decompress(predpath.read_bytes())).hexdigest()
    assert decompressed_hash == claimed['prediction_sha256']
    assert len(pred) == 10006 and pred.y.sum() == 333
    assert not pred[['host','phage']].duplicated().any()
    assert pred.score.between(0,1).all() and set(pred.y)=={0,1}
    assert pred.host.nunique() == 200 and pred.phage.nunique() == 105
    assert set(pred.group) == set(range(133))
    assert pred.groupby('host').group.nunique().eq(1).all()
    labels = pred.merge(pairs,on=['host','phage'],validate='one_to_one',suffixes=('_pred','_work'))
    assert len(labels)==10006 and labels.y_pred.eq(labels.y_work).all()
    rows=[]
    for host,x in pred.groupby('host',sort=True):
        if host not in eligible:
            continue
        ranked=x.sort_values(['score','phage'],ascending=[False,True],kind='stable')
        rows.append({'host':host,'group':int(x.group.iloc[0]),'tested':len(x),'positive':int(x.y.sum()),
                     'hit_at_5':int(ranked.y.iloc[:5].sum()>0),'auroc':auc(x.y,x.score)})
    recomputed=pd.DataFrame(rows)
    archived=pd.read_csv(ROOT/'code/published_repro_perhost.csv',dtype={'host':str}).sort_values('host').reset_index(drop=True)
    for col in ['host','group','tested','positive','hit_at_5']:
        assert np.array_equal(recomputed[col],archived[col]),col
    assert np.allclose(recomputed.auroc,archived.auroc,atol=1e-12,rtol=0)
    v=recomputed[['hit_at_5','auroc']].to_numpy(float)
    pci=np.quantile(v[ix].mean(axis=1),[.025,.975],axis=0)
    assert int(v[:,0].sum()) == claimed['eligible_hit_at_5']['hits']
    assert np.isclose(v[:,1].mean(),claimed['eligible_macro_host_auroc']['point'])
    assert np.allclose(pci[:,0],claimed['eligible_hit_at_5']['host_bootstrap_ci95'])
    assert np.allclose(pci[:,1],claimed['eligible_macro_host_auroc']['host_bootstrap_ci95'])
    pooled=auc(pred.y,pred.score)
    assert np.isclose(pooled,claimed['pooled_pair_auroc_all_200_hosts'])
    c['author_parameter_reimplementation']={'groups_covered':133,'hosts':200,'pairs':10006,'positives':333,
        'eligible_hosts':131,'hits':int(v[:,0].sum()),'hit_at_5':float(v[:,0].mean()),
        'macro_auroc':float(v[:,1].mean()),'pooled_pair_auroc':pooled,
        'hit_ci95':pci[:,0].tolist(),'macro_auroc_ci95':pci[:,1].tolist(),
        'canonical_prediction_sha256':decompressed_hash,'model_refit_performed':False}
    inventory=json.loads((ROOT/'code/safety_inventory.json').read_text())
    cargo=json.loads((ROOT/'code/cargo_screen_limited.json').read_text())
    ie=inventory['entries']; ce=cargo['entries']
    assert len(ie)==len(ce)==105
    assert {x['phage'] for x in ie}=={x['phage'] for x in ce}==set(pred.phage)
    assert all(not x['eligible_for_nomination'] for x in ie)
    assert inventory['nomination_count']==cargo['nomination_count']==0
    assert sum(x['reported_hits'] for x in ce)==cargo['reported_hits_total']==0
    c['safety_evidence']={'inventoried_phages':105,'cleared':0,'nominated':0,
        'reported_protein_only_cargo_search_records':105,'reported_cargo_hits':0,
        'reported_predicted_orfs':sum(x['predicted_orfs'] for x in ce),
        'raw_cargo_reports_logs_orf_files_in_repository':False,
        'cargo_execution_independently_verified':False,
        'unchecked':['closed genome ends','viral lifestyle','complete AMR/toxin/virulence coverage',
                     'uncalled ORFs and nucleotide-mode search','commensal off-target panel','empirical safety']}
    if args.raw_dir:
        raw=args.raw_dir
        hashes={}
        for name,expected in claimed['source_sha256'].items():
            actual=sha(raw/name);assert actual==expected,name;hashes[name]=actual
        matrix=pd.read_csv(raw/'phage_host_interactions.csv',index_col=0)
        for row in pred.itertuples(index=False):
            assert int(matrix.loc[row.host,row.phage])==row.y
        hosts=pd.read_csv(raw/'esm2_embeddings_loci.csv').accession.astype(str).tolist()
        similarities=np.loadtxt(raw/'all_loci_score_matrix.txt',delimiter='\t')
        assert similarities.shape==(200,200)
        groups=np.full(len(hosts),-1,dtype=int);gid=0
        for i in range(len(hosts)):
            cluster=np.flatnonzero(similarities[i]>=.995)
            if groups[i]<0:groups[cluster]=gid;gid+=1
        assert gid==133 and np.all(groups>=0)
        mapping=dict(zip(hosts,groups))
        assert all(mapping[h]==g for h,g in zip(pred.host,pred.group))
        assert hashlib.md5((raw/'phages_genomes.zip').read_bytes()).hexdigest()==inventory['genome_zip_md5']
        record=json.loads((raw/'record.json').read_text())
        md5s={}
        for item in record['files']:
            name=item['key']
            if name in claimed['source_sha256'] or name=='phages_genomes.zip':
                actual='md5:'+hashlib.md5((raw/name).read_bytes()).hexdigest()
                assert actual==item['checksum'],name
                md5s[name]=actual
        with ZipFile(raw/'phages_genomes.zip') as archive:
            files={Path(n).stem:n for n in archive.namelist()
                   if n.startswith('phages_genomes/') and n.endswith(('.fasta','.fa','.fna'))
                   and not Path(n).name.startswith('._')}
            for entry in ie:
                assert entry['phage'] in files
                text=archive.read(files[entry['phage']]).decode('utf-8')
                headers=[line for line in text.splitlines() if line.startswith('>')]
                letters=''.join(line.strip() for line in text.splitlines() if not line.startswith('>')).upper()
                assert len(headers)==entry['contigs']
                assert len(letters)==entry['bases']
                assert sum(ch not in 'ACGT' for ch in letters)==entry['ambiguous_bases']
        c['live_author_inputs']={'deposited_md5_matches':md5s,'genome_inventory_counts_match':True,'source_sha256_matches':hashes,'all_labels_and_group_assignments_match':True,
            'genome_zip_md5_matches':True}
    else:
        c['live_author_inputs']={'verified':False,'reason':'--raw-dir not supplied'}
    result['limits']=['Arithmetic verification does not attest model execution or fitted provenance.',
        'Prototype/ablation pair-level scores and individual fold files are not archived.',
        'Raw AMRFinder reports, logs and ORFs are not archived; only their summary hashes are present.',
        'Different host vs locus-group partitions preclude a fair paired superiority claim.',
        'Bootstrap resamples fixed training-side host results, not retrained models or external cohorts.']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
