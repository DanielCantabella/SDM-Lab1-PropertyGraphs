import pandas as pd

def printLine(c,n):
    print(c*n)
def printQuery(res):
    df = pd.DataFrame([dict(record) for record in res])
    if df.empty:
        print("No results")
    else:
        print(df)
