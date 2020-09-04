import spotlight
import requests
from urllib.request import urlretrieve
from urllib.parse import urlencode
#annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate', 'Barack Obama is tall', confidence=0.4, support=20, verify = False)
#spotlight.annotate()

#curl -X GET "https://api.dbpedia-spotlight.org/en/annotate?text=Who%20invented%20Skype" -H "accept: application/json"

#headers = {"accept: application/json"}
url = 'https://api.dbpedia-spotlight.org/en/annotate?text=Who%20invented%20Skype'
headers = {'accept': 'application/json'}
r = requests.get(url=url, headers=headers, verify=False)
print(r.json())
#print(r)


mydict = {'text': 'Who Invented Skype'}
querystring = urlencode(mydict)
url = "https://api.dbpedia-spotlight.org/en/annotate?"
# str resolves to: 'q=whee%21+Stanford%21%21%21&something=else'
final_url = url + querystring

r = requests.get(url=final_url, headers=headers, verify=False)
print(r.json())


