import pandas
from election import run_election
from fraudCheck import nameCheck
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename',type=str,help='name of election file',default='Anonymized.csv')
    parser.add_argument('--fraud_protect',type=bool,help='whether fraud protection is enabled',default=True)
    parser.add_argument('-c','--col_start',type=int,help='column of first election',default=6)

    args = parser.parse_args()

    fileName = args.filename
    fraudProtection = args.fraud_protect
    beginningColumnIndex = args.col_start

    resultsDF = pandas.read_csv(fileName)
    #do identity checks here:

    if fraudProtection:
        protectedDF = nameCheck(resultsDF)
    else:
        protectedDF = resultsDF

    #need to extract just the vote tables from the csv
    #should be the same amount of added fields every time?
    numCols = len(protectedDF.columns)
    votesDF = protectedDF.iloc[:, beginningColumnIndex:numCols:1]


    #print(protectedDF)
    #print(protectedDF.iloc[:, 5:numCols:1])
    for series_name, series in votesDF.items():
        print(series_name.rstrip())
        run_election(series_name.rstrip(), series)


    #print(resultsDF.to_string)