import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
import json
import urllib.request
import math

#data source handle
url='https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'

#fetch data from data source and convert
httpResponse = urllib.request.urlopen(url) #type http.client.HTTPResponse
byteStream = httpResponse.read() #type bytes
jsonString = byteStream.decode() #type string
jsonObject = json.loads(jsonString) #type dictionary
jsonList = jsonObject["records"] #type list

#convert to pandas dataframe
df = pd.json_normalize(jsonList)
print(df)

#filter for data from Germany and invert data sequence
dfGer = pd.DataFrame(df[df.geoId == 'DE'])
dfGer = dfGer.sort_index(axis=0, ascending=False)
print(dfGer)

#extract number of cases from dataframe to list
casesList = dfGer["cases_weekly"].astype(int).tolist()

#create new column in dataframe for cumulative number of cases
casesCum = casesList.copy()
for i in range(1,len(casesCum)): #since first row has no predecessor you have to start loop from second row
    casesCum[i] = casesCum[i] + casesCum[i-1]
dfGer['casesCum'] = casesCum

#create new column in dataframe for log of cumulative number of cases
casesCumLog = casesCum.copy()
for i in range(1,len(casesCumLog)):
    if(casesCumLog[i] != 0):
        casesCumLog[i] = math.log(casesCumLog[i])
dfGer['casesCumLog'] = casesCumLog

print(dfGer)

#plot cumulative number of cases over time
casesCumPlot = plt.figure(1)
plt.plot(range(len(dfGer["dateRep"].tolist())), dfGer["casesCum"].tolist())
plt.xticks(range(len(dfGer["dateRep"].tolist())), dfGer["dateRep"].tolist(), rotation='vertical')
plt.xlabel("Datum")
plt.ylabel("Fallzahlen")
plt.title("Covid-19 Fallzahlen in Deutschland")

#plot log of cumulative number of cases over time
casesCumLogPlot = plt.figure(2)
plt.plot(range(len(dfGer["dateRep"].tolist())), dfGer["casesCumLog"].tolist())
plt.xticks(range(len(dfGer["dateRep"].tolist())), dfGer["dateRep"].tolist(), rotation='vertical')
plt.xlabel("Datum")
plt.ylabel("Logarithmierte Fallzahlen")
plt.title("Logarithmierte Covid-19 Fallzahlen in Deutschland")

plt.show()