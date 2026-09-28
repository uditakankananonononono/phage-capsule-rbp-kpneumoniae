#!/usr/bin/env python3
"""Feature construction: phage = mean of its RBP ESM2 embeddings (multi-instance mean,
matching PhageHostLearn's multi-view spirit in a single view); host = locus ESM2 embedding.
Pair feature = concatenation [rbp_mean, locus] (2560 dims). Training data only."""
import pandas as pd, numpy as np, json
R='/tmp/deep-research/phage-kp/raw'
def build():
    M=pd.read_csv(f'{R}/phage_host_interactions.csv',index_col=0)
    loci=pd.read_csv(f'{R}/esm2_embeddings_loci.csv',index_col=0)
    rbp=pd.read_csv(f'{R}/esm2_embeddings_rbp.csv')
    rbp_mean=rbp.groupby('phage_ID').mean(numeric_only=True)
    rbp_mean.index.name='phage'
    pairs=[]
    for h,row in M.iterrows():
        if h not in loci.index: continue
        for p,y in row.items():
            if pd.isna(y) or p not in rbp_mean.index: continue
            pairs.append((h,p,int(y)))
    df=pd.DataFrame(pairs,columns=['host','phage','y'])
    return df,loci,rbp_mean
if __name__=='__main__':
    df,loci,rbp_mean=build()
    print(df['y'].value_counts().to_dict(), df.shape)
    df.to_csv('/tmp/deep-research/phage-kp/work_pairs.csv',index=False)
