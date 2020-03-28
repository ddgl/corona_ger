import requests
import lxml.html as lh
import pandas as pd

url='https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'

page = requests.get(url) #Response object called page containing bytes, handle for contents
#print (type(page))

doc = lh.fromstring(page.content) #parses the string to a correct HTML document with <html> as parent node, doc is a lxml.html.HtmlElement object
#print (type(doc))

tr_elements = doc.xpath('//tr') #tr_elements is a list of all tr-elements (//) in doc (which also are HtmlElements)
#print (type(tr_elements))

#check content and size of tr_elements in order to check if correct elements where selected
#print (tr_elements)
#print (len(tr_elements))
for T in tr_elements:
    #print (len(T))
    #print (type(T))
    print(T.text_content())