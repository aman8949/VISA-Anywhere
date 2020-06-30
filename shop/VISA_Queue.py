
import requests
import json
import zipcodes
import pycountry
import datetime


cert='shop\\cert.pem'
key="shop\\private.pem"
url = "https://sandbox.api.visa.com/visaqueueinsights/v1/queueinsights"
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic VlpIRzRSSk9JS1JQMVhaNjdPRE4yMTBIems2ZzRhdVJJc3JrNThsRzEwWjR0c2NQdzo3NjRyZ3BORXlFUGN0WHAxNFpadkJRYkE=',
  'Content-Type': 'application/json'
}
date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
date=date[0:23]

payload = json.loads('''
{
"requestHeader": {
"messageDateTime": "'''+date+'''",
"requestMessageId": "@a1v2cev2"
},
"requestData": {
"kind": "predict"
}
}
''')

def merchantQueue():
	response = requests.request("POST",  url,cert=(cert,key), headers=headers, json = payload)
	return(response.text.encode('utf8'))
