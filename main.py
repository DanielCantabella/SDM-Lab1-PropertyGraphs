from util import *
import warnings
from a2_getSampleData import getSampleData
from a2_generateCSV import generateCSV
from a2_splitVenues import splitVenues
from a2_generateRelations import generateRelations
from a2_importData2Database import importData2Database
from a3_evolving import evolveTheGraph
from b_queryExecution import queryExecution
from c_recommender import recommender
from d_algorithmExecution import algortihmExecution


if __name__ == '__main__':
    printLine("=",70)
    print("Property Graphs Lab")
    printLine("=", 70)
    print("Task A")
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
    print("5. Evolving the graph")
    printLine("-", 70)
    evolveTheGraph()
    printLine("=", 70)
    print("Task B")
    printLine("=", 70)
    print("Query executions")
    queryExecution()
    printLine("=", 70)
    print("Task C")
    printLine("=", 70)
    print("Recommender")
    recommender()
    printLine("=", 70)
    print("Task D")
    printLine("=", 70)
    print("Algorithms executions")
    algortihmExecution()





