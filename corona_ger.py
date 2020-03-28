import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt

url='https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'

page = requests.get(url) #Response object called page containing bytes, handle for contents
#print (type(page))

doc = lh.fromstring(page.content) #parses the string to a correct HTML document with <html> as parent node, doc is a lxml.html.HtmlElement object
#print (type(doc))

tr_elements = doc.xpath('//tbody/tr') #tr_elements is a list of all tr-elements (//) which are children of tbody in doc (which also are HtmlElements)
#print (type(tr_elements))

""" #check content and size of tr_elements in order to check if correct elements where selected
#print (tr_elements)
#print (len(tr_elements))
for T in tr_elements:
    #print (len(T))
    #print (type(T))
    print(T[0].text_content(), T[1].text_content()) """

total_cases = {}
for i in tr_elements:
    total_cases[i[0].text_content()] = int(i[1].text_content().replace(".",""))

""" for x in total_cases:
    print(x, total_cases[x]) """

df = pd.DataFrame(total_cases.items(), columns=['Bundesland','Fallzahlen'])
print(df)
#print (df.head())

plt.bar(range(len(df["Bundesland"].tolist())), df["Fallzahlen"].tolist())
plt.xticks(range(len(df["Bundesland"].tolist())), df["Bundesland"].tolist(), rotation='vertical')
plt.xlabel("Bundesland")
plt.ylabel("Fallzahlen")
plt.title("Covid-19 Fallzahlen in den deutschen Bundesländern")
#df.plot(kind='bar')

plt.show()