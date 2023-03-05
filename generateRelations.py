import pandas as pd
import random
import json

PAPERS_SOURCE = 'sample_csv/papers-sample.csv'
AUTHORS_SOURCE = 'sample_csv/authors-sample.csv'
CONFERENCES_SOURCE = 'sample_csv/conferences.csv'
JOURNALS_SOURCE = 'sample_csv/journals.csv'
OUTPUT_PATH_WRITTEN_BY = 'sample_csv/written-by.csv'
OUTPUT_PATH_REVIEWED_BY = 'sample_csv/reviewed-by.csv'
OUTPUT_PATH_BELONGS_TO = 'sample_csv/belongs-to.csv'
OUTPUT_PATH_PUBLISHED_IN = 'sample_csv/publisehd-in.csv'

papers = pd.read_csv(PAPERS_SOURCE)
authors = pd.read_csv(AUTHORS_SOURCE)
conferences = pd.read_csv(CONFERENCES_SOURCE)
journals = pd.read_csv(JOURNALS_SOURCE)

random_seed = 123
random.seed(random_seed)

#Generate files

belongs_to = pd.DataFrame(columns=['venueID', 'paperID'])
published_in = pd.DataFrame(columns=['venueID', 'paperID', 'year', 'volume', 'startPage', 'endPage'])
written_by = pd.DataFrame(columns=['paperID', 'authorID', 'is_corresponding'])
written_by['is_corresponding'] = written_by['is_corresponding'].astype(bool)
reviewed_by = pd.DataFrame(columns=['paperID', 'reviewerID', 'grade'])

authors_ids = list(authors['authorid'].unique())

for index, row in papers.iterrows():
    #Assign venue (randomly conference or journal)
    random_type = random.randint(0, 1)
    #Conference
    if random_type == 0:
        conference = conferences.sample(1)
        row_data = {'venueID': conference.loc[conference.index[0], 'venueID'], 'paperID': row['corpusid']}
        belongs_to = pd.concat([belongs_to, pd.DataFrame([row_data])], ignore_index=True)
    #Journal
    else:
        journal = journals.sample(1)
        year = random.randint(1940, 2023)
        volume = random.randint(1, 20)
        startPage = random.randint(1, 100)
        endPage = startPage + random.randint(1, 100)
        row_data = {'venueID':  journal.loc[journal.index[0], 'venueID'], 'paperID': row['corpusid'],  'year': year, 'volume': volume,
                    'startPage': startPage, 'endPage':endPage}
        published_in = pd.concat([published_in, pd.DataFrame([row_data])], ignore_index=True)
    #Assign authors
    n_authors = random.randint(1, 5)
    authors = random.sample(authors_ids, n_authors)
    for i, author in enumerate(authors):
        corresponding = False
        if i == 0:
            corresponding = True
        row_data = {'paperID': row['corpusid'], 'authorID': author, 'is_corresponding': bool(corresponding)}
        written_by = pd.concat([written_by, pd.DataFrame([row_data])], ignore_index=True)
    #Assign reviewers
    n_reviewers = random.randint(1, 3)
    # first we remove the authors as possible reviewers
    filtered_list = list(x for x in authors_ids if x not in authors)
    reviewers = random.sample(filtered_list, n_reviewers)
    for reviewer in reviewers:
        grade = random.randint(1, 5)
        row_data = {'paperID': row['corpusid'], 'reviewerID': reviewer, 'grade': grade}
        reviewed_by = pd.concat([reviewed_by, pd.DataFrame([row_data])], ignore_index=True)

belongs_to.to_csv(OUTPUT_PATH_BELONGS_TO,encoding='utf-8',index=False)
written_by.to_csv(OUTPUT_PATH_WRITTEN_BY,encoding='utf-8',index=False)
reviewed_by.to_csv(OUTPUT_PATH_REVIEWED_BY,encoding='utf-8',index=False)
published_in.to_csv(OUTPUT_PATH_PUBLISHED_IN,encoding='utf-8',index=False)

#Generate writen-by.csv using the true values
# df = pd.read_csv(PAPERS_SOURCE)
# df_out = pd.DataFrame(columns=['paperID', 'authorID', 'is_corresponding'])
# df_out['is_corresponding'] = df_out['is_corresponding'].astype(bool)
#
# for index, row in df.iterrows():
#     authors = json.loads(row['authors'].replace("'",'"'))
#     for i, author in enumerate(authors):
#         corresponding = False
#         if i == 0:
#             corresponding = True
#         row_data = {'paperID': row['corpusid'], 'authorID': author['authorId'], 'is_corresponding': bool(corresponding)}
#         df_out = pd.concat([df_out, pd.DataFrame([row_data])], ignore_index=True)
#
# df_out.to_csv(OUTPUT_PATH_WRITTEN_BY,encoding='utf-8',index=False)