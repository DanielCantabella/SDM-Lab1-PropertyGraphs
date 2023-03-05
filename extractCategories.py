import pandas as pd
import random
import json
import ast


# When using full data
PAPERS_SOURCE = 'sample_csv/papers-sample.csv'
OUTPUT_PATH_CATEGORIES = 'sample_csv/categoriesRelations.csv'
OUTPUT_PATH_UNIQUECATEGORIES = 'sample_csv/uniqueCategories.csv'


papers = pd.read_csv(PAPERS_SOURCE)

random_seed = 123
random.seed(random_seed)

#Generate files
categories = pd.DataFrame(columns=['categoryName', 'paperID'])
uniqueCategories = pd.DataFrame(columns=['categoryName'])
categoriesList=['Unknown']
uniqueCategories = pd.concat([uniqueCategories, pd.DataFrame([{'categoryName': "Unknown"}])], ignore_index=True)
for index, row in papers.iterrows():

    if str(row['s2fieldsofstudy']) != 'nan':
        journalCategories=ast.literal_eval(row['s2fieldsofstudy'])
        for category in journalCategories:
            journalCategoryJson = json.loads(str(category).replace("'", '"'))
            if journalCategoryJson["category"] not in categoriesList:
                categoriesList.append(journalCategoryJson["category"])
                row_uniqueData={'categoryName': journalCategoryJson["category"]}
                uniqueCategories = pd.concat([uniqueCategories, pd.DataFrame([row_uniqueData])], ignore_index=True)
            row_data = {'categoryName': journalCategoryJson["category"], 'paperID': row['corpusid']}
            categories = pd.concat([categories, pd.DataFrame([row_data])], ignore_index=True)
    else:
        row_data = {'categoryName': 'Unknown', 'paperID': row['corpusid']}
        categories = pd.concat([categories, pd.DataFrame([row_data])], ignore_index=True)


categories.to_csv(OUTPUT_PATH_CATEGORIES,encoding='utf-8',index=False)
uniqueCategories.to_csv(OUTPUT_PATH_UNIQUECATEGORIES,encoding='utf-8',index=False)
