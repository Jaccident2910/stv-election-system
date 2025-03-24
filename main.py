import pandas
from election import run_election
from fraudCheck import nameCheck

# --- SETTINGS ---
fraudProtection = True
fileName = "generalMT24.csv"

# ----------------


resultsDF = pandas.read_csv(fileName)
#do identity checks here:

if fraudProtection:
    protectedDF = nameCheck(resultsDF)
else:
    protectedDF = resultsDF

#need to extract just the vote tables from the csv
#should be the same amount of added fields every time?
numCols = len(protectedDF.columns)
votesDF = protectedDF.iloc[:, 5:numCols:1]


#print(protectedDF)
#print(protectedDF.iloc[:, 5:numCols:1])
for series_name, series in votesDF.items():
    print(series_name.rstrip())
    run_election(series_name.rstrip(), series)


#print(resultsDF.to_string)