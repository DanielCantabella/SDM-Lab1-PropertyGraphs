import pandas as pd
import csv

tables=['abstracts', 'authors', 'citations', 'embeddings', 'paper-ids', 'papers', 'publication-venues', 's2orc', 'tldrs']
for table in tables:
    df = pd.read_json('./data/samples/'+table+'/'+table+'-sample.jsonl.gz', lines=True, compression='gzip')
    df.to_csv('./data/csv/SemanticScholar/'+table+'.csv')