import os
import pathlib
import pandas as pd

DATA_FOLDER = 'sample'
OUTPUT_FOLDER = 'sample_csv'

directory = os.getcwd()
data_source = directory + '\\' + DATA_FOLDER

#Create the output folder
directory = os.getcwd()
pathlib.Path(directory+'\\'+OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

for filename in os.listdir(data_source):
    inputfile = DATA_FOLDER + '/' + filename
    outputfile = OUTPUT_FOLDER + '/' + filename.split('.')[0] + '.csv'
    print(inputfile)
    df = pd.read_json(inputfile, lines=True, compression='gzip')
    df.to_csv(outputfile, encoding='utf-8',index=False)





