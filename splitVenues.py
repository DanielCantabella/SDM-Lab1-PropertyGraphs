import pandas as pd
import random

'''
SPLIT VENUES BETWEEN JOURNALS AND CONFERENCES.
 * Journal: pages and volume are generated randomly.
 * Conference: edition and date are generated randomly.
'''

VENUES_SOURCE = 'sample_csv/publication-venues-sample.csv'
OUTPUT_PATH_JOURNALS = 'sample_csv/journals.csv'
OUTPUT_PATH_CONFERENCES = 'sample_csv/conferences.csv'

venues = pd.read_csv(VENUES_SOURCE)

random_seed = 123
random.seed(random_seed)

#Generate files
conferences = pd.DataFrame(columns=['venueID', 'conferenceName', 'edition', 'date'])
journals = pd.DataFrame(columns=['venueID', 'journalName', 'pages', 'volume'])

for index, row in venues.iterrows():
    #Journals
    if row['type']=='journal':
        row_data = {'venueID': row['id'], 'journalName': row['name'], 'pages': random.randint(30,300), 'volume': random.randint(1,100)}
        journals = pd.concat([journals, pd.DataFrame([row_data])], ignore_index=True)
    #Conferences
    elif row['type']=='conference':
        row_data = {'venueID': row['id'], 'conferenceName': row['name'], 'edition': random.randint(1,70), 'date': str(random.randint(1940,2023))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,31))}
        conferences = pd.concat([conferences, pd.DataFrame([row_data])], ignore_index=True)
    #More conferences (we assume null values are conferences)
    else:
        row_data = {'venueID': row['id'], 'conferenceName': row['name'], 'edition': random.randint(1, 70),
                    'date': str(random.randint(1940, 2023)) + '-' + str(random.randint(1, 12)) + '-' + str(
                        random.randint(1, 31))}
        conferences = pd.concat([conferences, pd.DataFrame([row_data])], ignore_index=True)


journals.to_csv(OUTPUT_PATH_JOURNALS,encoding='utf-8',index=False)
conferences.to_csv(OUTPUT_PATH_CONFERENCES,encoding='utf-8',index=False)


