import pandas as pd
import random
import datetime

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
conferences = pd.DataFrame(columns=['venueID', 'conferenceName', 'edition', 'startDate','endDate', 'issn', 'url'])
journals = pd.DataFrame(columns=['venueID', 'journalName', 'issn', 'url'])

for index, row in venues.iterrows():
    #Journals
    if row['type']=='journal':
        row_data = {'venueID': row['id'], 'journalName': row['name'], 'issn' : row['issn'], 'url' : row['url']}
        journals = pd.concat([journals, pd.DataFrame([row_data])], ignore_index=True)
    #Conferences (we assume null values are conferences)
    else:
        #Generate duration of the conference
        n = random.randint(1,30)  # Random duration days

        start_date = datetime.date(1940, 1, 1)
        end_date = datetime.date.today()

        days_between_dates = (end_date - start_date).days - n + 1
        random_number_of_days = random.randrange(days_between_dates)

        start_date = start_date + datetime.timedelta(days=random_number_of_days)
        end_date = start_date + datetime.timedelta(days=n - 1)


        row_data = {'venueID': row['id'], 'conferenceName': row['name'], 'edition': random.randint(1,70),
                    'startDate': start_date, 'endDate': end_date,  'issn' : row['issn'], 'url' : row['url']}
        conferences = pd.concat([conferences, pd.DataFrame([row_data])], ignore_index=True)


journals.to_csv(OUTPUT_PATH_JOURNALS,encoding='utf-8',index=False)
conferences.to_csv(OUTPUT_PATH_CONFERENCES,encoding='utf-8',index=False)


