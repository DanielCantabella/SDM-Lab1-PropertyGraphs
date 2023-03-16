import os
import pathlib
import requests

MANIFEST_URL = "https://s3-us-west-2.amazonaws.com/ai2-s2ag/samples/MANIFEST.txt"
DATASETS_LIST = {'abstracts', 'authors', 'citations', 'paper-ids', 'papers', 'publication-venues'}


def getSampleData():
    response = requests.get(MANIFEST_URL)
    manifest = response.text.strip().split("\n")

    for file in manifest:
        if ('jsonl' in file and any(word in file for word in DATASETS_LIST)):
            file_url = f"https://s3-us-west-2.amazonaws.com/ai2-s2ag/{file}"
            index = file.rfind('/')
            filename = 'sample/' + file[index + 1:]
            print(filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                response = requests.get(file_url)
                f.write(response.content)