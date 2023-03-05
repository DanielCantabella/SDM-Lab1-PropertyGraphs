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
OUTPUT_PATH_CONFERENCES = 'sample_csv/conferences.csv'

papers = pd.read_csv(PAPERS_SOURCE)
authors = pd.read_csv(AUTHORS_SOURCE)
venues = pd.read_csv(VENUES_SOURCE)

random_seed = 123
random.seed(random_seed)

#Generate files
conferences = pd.DataFrame(columns=['venueID', 'conferenceName', 'edition', 'date'])
journals = pd.DataFrame(columns=['venueID', 'journalName', 'pages', 'volume'])
belongs_to = pd.DataFrame(columns=['venueID', 'paperID'])
written_by = pd.DataFrame(columns=['paperID', 'authorID', 'is_corresponding'])
written_by['is_corresponding'] = written_by['is_corresponding'].astype(bool)
reviewed_by = pd.DataFrame(columns=['paperID', 'reviewerID', 'grade'])



venue_ids = venues['id'].unique()
authors_ids = list(authors['authorid'].unique())

problematicVenues=[]
for index, row in papers.iterrows():

    #Assign venue
    venue_id = random.choice(venue_ids)
    row_data = {'venueID': venue_id, 'paperID': row['corpusid']}
    belongs_to = pd.concat([belongs_to, pd.DataFrame([row_data])], ignore_index=True)
    try:
        if str(row['journal']) != 'nan':
            journalProperties=json.loads(str(row['journal']).replace("'", '"'))

            journalPages = journalProperties["pages"]
            journalVolume = journalProperties["volume"]
            if journalProperties["name"] != "":
                journalName = journalProperties["name"]
                # print(journalName)
            else:
                journalName = str(venues[venues['id']==venue_id]['name'])
                # print(venue_id)
                # print(journalName)

            row_data_journals = {'venueID': venue_id, 'paperID': row['corpusid'], 'journalName': journalName, 'pages': journalPages, 'volume': journalVolume}
            print(row_data_journals)
            journals = pd.concat([journals, pd.DataFrame([row_data_journals])], ignore_index=True)

        else:
            conferenceName = "Conference " + str(index)
            conferenceEdition = random.randint(1,5)
            conferenceDate = row['publicationdate']
            row_data_conferences={'venueID': venue_id, 'conferenceName': conferenceName, 'edition': conferenceEdition, 'date':conferenceDate}
            conferences = pd.concat([conferences, pd.DataFrame([row_data_conferences])], ignore_index=True)
    except:
            print("Error in venueId: ",venue_id)
            problematicVenues.append(venue_id)
#
print(len(problematicVenues))
# belongs_to.to_csv(OUTPUT_PATH_BELONGS_TO,encoding='utf-8',index=False)
# written_by.to_csv(OUTPUT_PATH_WRITTEN_BY,encoding='utf-8',index=False)
# reviewed_by.to_csv(OUTPUT_PATH_REVIEWED_BY,encoding='utf-8',index=False)
journals.to_csv(OUTPUT_PATH_JOURNALS,encoding='utf-8',index=False)
conferences.to_csv(OUTPUT_PATH_CONFERENCES,encoding='utf-8',index=False)


