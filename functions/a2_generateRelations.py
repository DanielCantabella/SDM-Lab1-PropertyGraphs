import pandas as pd
import random
import json

PAPERS_SOURCE = 'sample_csv/papers-sample.csv'
AUTHORS_SOURCE = 'sample_csv/authors-sample.csv'
CONFERENCES_SOURCE = 'sample_csv/is-from.csv'
JOURNALS_SOURCE = 'sample_csv/volume-from.csv'
KEYWORDS_SOURCE = 'sample_csv/keywords.csv'
ABSTRACTS_SOURCE = 'sample_csv/abstracts-sample.csv'
COMPANIES_SOURCE = 'sample_csv/companies.csv'
UNIVERSITIES_SOURCE = 'sample_csv/universities.csv'
REVIEWS_SOURCE = 'sample_csv/reviews.csv'
OUTPUT_PATH_WRITTEN_BY = 'sample_csv/written-by.csv'
OUTPUT_PATH_REVIEWED_BY = 'sample_csv/reviewed-by.csv'
OUTPUT_PATH_BELONGS_TO = 'sample_csv/belongs-to.csv'
OUTPUT_PATH_PUBLISHED_IN = 'sample_csv/published-in.csv'
OUTPUT_PATH_PAPERS = 'sample_csv/papers-processed.csv'
OUTPUT_PATH_CITED_BY = 'sample_csv/cited-by.csv'
OUTPUT_RELATED_TO = 'sample_csv/related-to.csv'
OUTPUT_ABSTRACTS = 'sample_csv/withAbstracts.csv'
OUTPUT_PATH_AFFILIATED_TO = 'sample_csv/affiliated-to.csv'

def generateRelations():
    papers = pd.read_csv(PAPERS_SOURCE)
    authors = pd.read_csv(AUTHORS_SOURCE)
    conferences = pd.read_csv(CONFERENCES_SOURCE)
    journals = pd.read_csv(JOURNALS_SOURCE)
    keywords = pd.read_csv(KEYWORDS_SOURCE)
    abstracts = pd.read_csv(ABSTRACTS_SOURCE)
    companies = pd.read_csv(COMPANIES_SOURCE)
    universities = pd.read_csv(UNIVERSITIES_SOURCE)
    reviews = pd.read_csv(REVIEWS_SOURCE)

    random_seed = 123
    random.seed(random_seed)

    #Generate files

    belongs_to = pd.DataFrame(columns=['venueID', 'paperID'])
    published_in = pd.DataFrame(columns=['venueID', 'paperID', 'startPage', 'endPage'])
    written_by = pd.DataFrame(columns=['paperID', 'authorID', 'is_corresponding'])
    written_by['is_corresponding'] = written_by['is_corresponding'].astype(bool)
    reviewed_by = pd.DataFrame(columns=['paperID', 'reviewerID', 'grade', 'review'])
    cited_by = pd.DataFrame(columns=['paperID_cited', 'paperID_citing'])
    related_to = pd.DataFrame(columns=['paperID', 'keyword'])
    withAbstract = pd.DataFrame(columns=['paperID', 'abstract'])
    affiliated_to = pd.DataFrame(columns=['affiliation', 'authorID', 'type'])


    authors_ids = list(authors['authorid'].unique())
    papers_ids = list(papers['corpusid'].unique())
    keywords = list(keywords['keyword'].unique())


    #Get the aditional fields for papers
    colnames = set(json.loads(papers.loc[0, 'externalids'].replace("'",'"').replace("None",'""')).keys())
    colnames.remove('CorpusId')
    papers = papers.assign(**{column_name: pd.Series() for column_name in colnames})


    for index, row in papers.iterrows():
        #Assign venue (randomly conference or journal)
        random_type = random.randint(0, 1)
        #Conference
        if random_type == 0:
            n_conf = random.randint(5, 15)
            conf_sample = conferences.sample(n_conf)
            for _ , conference in conf_sample.iterrows():
                row_data = {'venueID':  conference['editionID'], 'paperID': row['corpusid']}
                belongs_to = pd.concat([belongs_to, pd.DataFrame([row_data])], ignore_index=True)

        #Journal
        else:
            n_journals = random.randint(5, 15)
            journal_sample = journals.sample(n_journals)
            for _ , journal in journal_sample.iterrows():
                startPage = random.randint(1, 100)
                endPage = startPage + random.randint(1, 100)
                row_data = {'venueID':  journal['volumeID'], 'paperID': row['corpusid'],
                            'startPage': int(startPage), 'endPage': int(endPage)}
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
            review = reviews.sample(1)
            row_data = {'paperID': row['corpusid'], 'reviewerID': reviewer, 'grade': grade, 'review': review.loc[review.index[0], 'review']}
            reviewed_by = pd.concat([reviewed_by, pd.DataFrame([row_data])], ignore_index=True)
        #Extract the aditional values of papers as columns
        new_values = json.loads(papers.loc[index, 'externalids'].replace("'", '"').replace("None", '""'))
        new_values.pop("CorpusId")
        for key, value in new_values.items():
            papers.at[index, key] = value
        #Assign citations
        n_cited_by = random.randint(1, 25)
        filtered_list = papers_ids.copy()
        filtered_list.remove(row['corpusid'])
        citing_papers = random.sample(filtered_list, n_cited_by)
        for paper in citing_papers:
            row_data = {'paperID_cited': row['corpusid'], 'paperID_citing': paper}
            cited_by = pd.concat([cited_by, pd.DataFrame([row_data])], ignore_index=True)
        #Assign keywords
        n_keywords = random.randint(1, 5)
        keywords_paper = random.sample(keywords, n_keywords)
        for kw in keywords_paper:
            row_data = {'paperID': row['corpusid'], 'keyword': kw}
            related_to = pd.concat([related_to, pd.DataFrame([row_data])], ignore_index=True)
        #Assign abstracts
        row_data = {'paperID': row['corpusid'], 'abstract': abstracts.loc[index, 'abstract']}
        withAbstract = pd.concat([withAbstract, pd.DataFrame([row_data])], ignore_index=True)
        #Assign organization
        random_organization = random.randint(0, 1)
        if random_organization == 0: #Company
            company = companies.sample(1)
            row_data = {'affiliation': company.loc[company.index[0], 'companyid'], 'authorID': authors_ids[index], 'type': "company"}
            affiliated_to = pd.concat([affiliated_to, pd.DataFrame([row_data])], ignore_index=True)

        else: #University
            university = universities.sample(1)
            row_data = {'affiliation': university.loc[university.index[0], 'universityid'], 'authorID': authors_ids[index], 'type': "university"}
            affiliated_to = pd.concat([affiliated_to, pd.DataFrame([row_data])], ignore_index=True)

    #Generate de csv relations
    written_by.to_csv(OUTPUT_PATH_WRITTEN_BY,encoding='utf-8',index=False)
    reviewed_by.to_csv(OUTPUT_PATH_REVIEWED_BY,encoding='utf-8',index=False)
    published_in.to_csv(OUTPUT_PATH_PUBLISHED_IN,encoding='utf-8',index=False)
    belongs_to.to_csv(OUTPUT_PATH_BELONGS_TO,encoding='utf-8',index=False)
    papers.to_csv(OUTPUT_PATH_PAPERS,encoding='utf-8',index=False)
    cited_by.to_csv(OUTPUT_PATH_CITED_BY,encoding='utf-8',index=False)
    related_to.to_csv(OUTPUT_RELATED_TO,encoding='utf-8',index=False)
    withAbstract.to_csv(OUTPUT_ABSTRACTS,encoding='utf-8',index=False)
    affiliated_to.to_csv(OUTPUT_PATH_AFFILIATED_TO,encoding='utf-8',index=False)

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