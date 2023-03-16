import pandas as pd
import random
import datetime
from datetime import timedelta
import string

'''
SPLIT VENUES BETWEEN JOURNALS AND CONFERENCES.
 * Journal: pages and volume are generated randomly.
 * Conference: edition and date are generated randomly.
'''

VENUES_SOURCE = 'sample_csv/publication-venues-sample.csv'
OUTPUT_PATH_JOURNALS = 'sample_csv/journals.csv'
OUTPUT_PATH_CONFERENCES = 'sample_csv/conferences.csv'
OUTPUT_PATH_BELONGS_TO = 'sample_csv/is-from.csv'
OUTPUT_PATH_VOLUME_FROM = 'sample_csv/volume-from.csv'

def splitVenues():
    venues = pd.read_csv(VENUES_SOURCE)

    random_seed = 123
    random.seed(random_seed)

    #Generate files
    is_from = pd.DataFrame(columns=['editionID', 'conferenceID', 'edition', 'startDate', 'endDate'])
    volume_from = pd.DataFrame(columns=['journalID', 'volumeID', 'year', 'volume'])
    conferences = pd.DataFrame(columns=['conferenceID', 'conferenceName', 'issn', 'url'])
    journals = pd.DataFrame(columns=['venueID', 'journalName', 'issn', 'url'])

    for index, row in venues.iterrows():
        #Journals
        if row['type']=='journal':
            row_data = {'venueID': row['id'], 'journalName': row['name'], 'issn' : row['issn'], 'url' : row['url']}
            journals = pd.concat([journals, pd.DataFrame([row_data])], ignore_index=True)

            #Generate volumes per journal
            year = 2020
            for ny in range(4):
                num_volumes = random.randint(1, 2)
                for nv in range(num_volumes):
                    randomID = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(8)) + '-' + \
                               ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4)) + '-' + \
                               ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4)) + '-' + \
                               ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4)) + '-' + \
                               ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(12))
                    row_data = {'journalID': row['id'], 'volumeID': randomID,
                                'year': year + ny, 'volume': nv+1}
                    volume_from = pd.concat([volume_from, pd.DataFrame([row_data])], ignore_index=True)


        #Conferences (we assume null values are is_from)
        else:
            conferences_data = {'conferenceID': row['id'], 'conferenceName': row['name'], 'issn': row['issn'],'url': row['url']}
            conferences = pd.concat([conferences, pd.DataFrame([conferences_data])], ignore_index=True)

            #Generate duration of the conference
            n = random.randint(1,30)  # Random duration days

            start_date = datetime.date(1940, 1, 1)
            end_date = datetime.date.today()

            days_between_dates = (end_date - start_date).days - n + 1
            random_number_of_days = random.randrange(days_between_dates)

            start_date = start_date + datetime.timedelta(days=random_number_of_days)
            end_date = start_date + datetime.timedelta(days=n - 1)

            numEditions=random.randint(1,10)
            confernceIds=[]
            for edition in range(1,numEditions):
                randomID = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(8))+ '-' + \
                                ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))+ '-' + \
                                ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))+ '-' + \
                                ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))+ '-' + \
                                ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(12))
                # print(randomID)
                if randomID not in confernceIds:
                    confernceIds.append(randomID)
                    belongs_to_data = {'editionID': randomID, 'conferenceID': row['id'],  'edition': edition,
                                'startDate': start_date + timedelta(days=edition*30), 'endDate': end_date + timedelta(days=edition*30)}

                    is_from = pd.concat([is_from, pd.DataFrame([belongs_to_data])], ignore_index=True)

    volume_from.to_csv(OUTPUT_PATH_VOLUME_FROM,encoding='utf-8',index=False)
    journals.to_csv(OUTPUT_PATH_JOURNALS,encoding='utf-8',index=False)
    conferences.to_csv(OUTPUT_PATH_CONFERENCES, encoding='utf-8', index=False)
    is_from.to_csv(OUTPUT_PATH_BELONGS_TO, encoding='utf-8', index=False)

