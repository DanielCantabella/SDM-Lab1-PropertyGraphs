import os
import pathlib
import pandas as pd
import gzip
import json
import csv

# When using sample data
DATA_FOLDER = 'sample'
OUTPUT_FOLDER = 'sample_csv'

def generateCSV():
    directory = os.getcwd()
    data_source = directory + '\\' + DATA_FOLDER

    #Create the output folder
    directory = os.getcwd()
    pathlib.Path(directory+'\\'+OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(data_source):

        inputfile = DATA_FOLDER + '/' + filename
        outputfile = OUTPUT_FOLDER + '/' + filename.split('.')[0] + '.csv'
        print(outputfile)

        # Using pandas for small files
        df = pd.read_json(inputfile, lines=True, compression='gzip')
        df.to_csv(outputfile, encoding='utf-8',index=False)

        # Using regular coding for big files
        # with gzip.open(inputfile, 'rt', encoding='utf-8') as f_in:
        #     with open(outputfile, 'w', encoding='utf-8', newline='') as f_out:
        #         writer = csv.writer(f_out)
        #         for line in f_in:
        #             data = json.loads(line)
        #             writer.writerow(data.values())





