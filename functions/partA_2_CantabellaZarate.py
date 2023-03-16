import warnings
from functions.a2_getSampleData import getSampleData
from functions.a2_generateCSV import generateCSV
from functions.a2_splitVenues import splitVenues
from functions.a2_generateRelations import generateRelations
from functions.a2_importData2Database import importData2Database
from functions.util import *

def partA2():
    printLine("=", 70)
    print("Task A.2")
    printLine("=", 70)
    print("1. Getting Sample Data")
    getSampleData()
    printLine("-", 70)
    print("2. Generate CSV")
    generateCSV()
    printLine("-", 70)
    print("3 Setting the data")
    printLine("-", 70)
    print("3.1. Splitting Venues into Conferences and Journals")
    splitVenues()
    printLine("-", 70)
    print("3.2. Generate Relations")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        generateRelations()
    printLine("-", 70)
    print("4. Upload de data to the graph")
    importData2Database()
    printLine("-", 70)
