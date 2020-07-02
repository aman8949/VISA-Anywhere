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
url='https://sandbox.api.visa.com/merchantlocator/v1/locator'
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic VlpIRzRSSk9JS1JQMVhaNjdPRE4yMTBIems2ZzRhdVJJc3JrNThsRzEwWjR0c2NQdzo3NjRyZ3BORXlFUGN0WHAxNFpadkJRYkE=',
  'Content-Type': 'application/json'
}
date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
date=date[0:23]

payload=json.loads('''
  
 
{
"header": {
"messageDateTime": "'''+date+'''",
"requestMessageId": "Request_001",
"startIndex": "0"
},
"searchAttrList": {
"merchantName": "Starbucks",
"merchantCountryCode": "840",
"merchantPostalCode": "95110",
"distance": "100",
"distanceUnit": "KM"
},
"responseAttrList": [
"GNLOCATOR"
],
"searchOptions": {
"maxRecords": "5",
"matchIndicators": "true",
"matchScore": "true"
}
}
''')

def merchantSearch(merchantName,merchantPostalCode):
	country=zipcodes.matching(merchantPostalCode)[0]["country"]
	merchantCountryCode = pycountry.countries.get(alpha_2=country).numeric
	payload["searchAttrList"]["merchantName"]=merchantName
	payload["searchAttrList"]["merchantPostalCode"]=merchantPostalCode
	payload["searchAttrList"]["merchantCountryCode"]=merchantCountryCode

	response = requests.request("POST",  url,cert=(cert,key), headers=headers, json = payload)
	return(response.text.encode('utf8'))
