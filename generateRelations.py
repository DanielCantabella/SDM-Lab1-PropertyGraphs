import pandas as pd
import json

PAPERS_SOURCE = 'sample_csv/papers-sample.csv'
OUTPUT_PATH_WRITTEN_BY = 'sample_csv/written-by.csv'

#Generate writen-by.csv
df = pd.read_csv(PAPERS_SOURCE)
df_out = pd.DataFrame(columns=['paperID', 'authorID', 'is_corresponding'])
df_out['is_corresponding'] = df_out['is_corresponding'].astype(bool)

for index, row in df.iterrows():
    authors = json.loads(row['authors'].replace("'",'"'))
    for i, author in enumerate(authors):
        corresponding = False
        if i == 0:
            corresponding = True
        row_data = {'paperID': row['corpusid'], 'authorID': author['authorId'], 'is_corresponding': bool(corresponding)}
        df_out = pd.concat([df_out, pd.DataFrame([row_data])], ignore_index=True)

df_out.to_csv(OUTPUT_PATH_WRITTEN_BY,encoding='utf-8',index=False)