import pandas as pd
import random
import json

# When using sample data
PAPERS_SOURCE = 'sample_csv/papers-sample.csv'
OUTPUT_PATH_WRITTEN_BY = 'sample_csv/written-by.csv'

# When using full data
PAPERS_SOURCE = 'sample_csv/papers-sample.csv'
AUTHORS_SOURCE = 'sample_csv/authors-sample.csv'
VENUES_SOURCE = 'sample_csv/publication-venues-sample.csv'
OUTPUT_PATH_WRITTEN_BY = 'sample_csv/written-by.csv'
OUTPUT_PATH_REVIEWED_BY = 'sample_csv/reviewed-by.csv'
OUTPUT_PATH_BELONGS_TO = 'sample_csv/belongs-to.csv'
OUTPUT_PATH_JOURNALS = 'sample_csv/journals.csv'

papers = pd.read_csv(PAPERS_SOURCE)
authors = pd.read_csv(AUTHORS_SOURCE)
venues = pd.read_csv(VENUES_SOURCE)

random_seed = 123
random.seed(random_seed)

#Generate files

journals = pd.DataFrame(columns=['venueID', 'journalName', 'pages', 'volume'])
belongs_to = pd.DataFrame(columns=['venueID', 'paperID'])
written_by = pd.DataFrame(columns=['paperID', 'authorID', 'is_corresponding'])
written_by['is_corresponding'] = written_by['is_corresponding'].astype(bool)
reviewed_by = pd.DataFrame(columns=['paperID', 'reviewerID', 'grade'])



venue_ids = venues['id'].unique()
authors_ids = list(authors['authorid'].unique())

for index, row in papers.iterrows():

    #Assign venue
    venue_id = random.choice(venue_ids)
    row_data = {'venueID': venue_id, 'paperID': row['corpusid']}
    belongs_to = pd.concat([belongs_to, pd.DataFrame([row_data])], ignore_index=True)
    if row['journals'].notnull():
        row_data_journals = row['journals'].json()
        journals = pd.concat([journals, pd.DataFrame([])])
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
