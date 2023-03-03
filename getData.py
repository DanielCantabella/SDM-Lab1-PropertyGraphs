import requests
import urllib
import os
import pathlib

API_KEY = 'JFgojBji9Y7BmuhrVquD265rHCMX50js9sXwV45G'
DATASETS_LIST = {'abstracts', 'authors', 'citations', 'paper-ids', 'papers', 'publication-venues'}

# Create the output folder
directory = os.getcwd()
pathlib.Path(directory + '\\data').mkdir(parents=True, exist_ok=True)

# If we want to get all the datasets we use the API to get the names
# latest_release = requests.get("http://api.semanticscholar.org/datasets/v1/release/latest").json()
# datasets = [dataset['name'] for dataset in latest_release['datasets']]

# If we want only some datasets defined in the constant
datasets = DATASETS_LIST

# Get the libraries names
for dataset in datasets:
    get_link = "http://api.semanticscholar.org/datasets/v1/release/latest/dataset/" + dataset
    dwld_links = requests.get(get_link, headers={'x-api-key': API_KEY}).json()
    # Download the datasets
    print(dwld_links['files'][0])
    # urllib.request.urlretrieve(dwld_links['files'][0], 'data/'+dataset  + ".jsonl.gz")
