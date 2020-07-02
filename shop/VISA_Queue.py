
import requests
import json
import zipcodes
import pycountry
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP_DIR = os.path.join(BASE_DIR,'shop')
CERT_DIR=os.path.join(SHOP_DIR,'cert.pem')
KEY=os.path.join(SHOP_DIR,'private.pem')
#print(BASE_DIR)

cert= CERT_DIR
key=KEY
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
