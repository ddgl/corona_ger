import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
import json
import urllib.request
import math

url='https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'

jsondata = urllib.request.urlopen(url).read().decode()

jsonobj = json.loads(jsondata)

jsonlist = jsonobj["records"]
#print(jsonlist)

#print(jsonobj)
print(type(jsonobj))
print(type(jsonlist))

df = pd.json_normalize(jsonlist)
print(df)

dfger = pd.DataFrame(df[df.geoId == 'DE'])
dfger = dfger.sort_index(axis=0, ascending=False)
print(dfger)

cases_list = dfger["cases"].astype(int).tolist()
cases_cum = cases_list.copy()
for i in range(1,len(cases_cum)):
    cases_cum[i] = cases_cum[i] + cases_cum[i-1]

print(cases_cum)
print(len(cases_cum))
dfger['cases_cum'] = cases_cum

cases_cum_log = cases_cum.copy()
for i in range(1,len(cases_cum_log)):
    if(cases_cum_log[i] != 0):
        cases_cum_log[i] = math.log(cases_cum_log[i])

print(cases_cum_log)
print(len(cases_cum_log))
dfger['cases_cum_log'] = cases_cum_log

print(dfger)


plt.plot(range(len(dfger["dateRep"].tolist())), dfger["cases_cum"].tolist())
plt.xticks(range(len(dfger["dateRep"].tolist())), dfger["dateRep"].tolist(), rotation='vertical')
plt.xlabel("Datum")
plt.ylabel("Fallzahlen")
plt.title("Covid-19 Fallzahlen in Deutschland")

plt.show()