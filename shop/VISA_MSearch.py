import requests
import json
import zipcodes
import pycountry
import datetime


cert='shop\\cert.pem'
key="shop\\private.pem"
url = "https://sandbox.api.visa.com/merchantsearch/v1/search"
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic VlpIRzRSSk9JS1JQMVhaNjdPRE4yMTBIems2ZzRhdVJJc3JrNThsRzEwWjR0c2NQdzo3NjRyZ3BORXlFUGN0WHAxNFpadkJRYkE=',
  'Content-Type': 'application/json'
}
date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
date=date[0:23]

payload = json.loads('''
{
"searchAttrList": {
"merchantName": "STARBUCKS",
"merchantCity": "",
"merchantState": "",
"merchantPostalCode": "94127",
"merchantCountryCode": "840"
},
"responseAttrList": [
"GNSTANDARD"
],
"searchOptions": {
"wildCard": [
"merchantName"
],
"maxRecords": "5",
"matchIndicators": "true",
"matchScore": "true",
"proximity": [
"merchantName"
]
},
"header": {
"requestMessageId": "Request_001",
"startIndex": "0",
"messageDateTime": "'''+date+'''"
}
}''')

def merchantSearch(merchantName,merchantPostalCode):
	country=zipcodes.matching(merchantPostalCode)[0]["country"]
	merchantCountryCode = pycountry.countries.get(alpha_2=country).numeric
	payload["searchAttrList"]["merchantName"]=merchantName
	payload["searchAttrList"]["merchantPostalCode"]=merchantPostalCode
	payload["searchAttrList"]["merchantCountryCode"]=merchantCountryCode

	response = requests.request("POST",  url,cert=(cert,key), headers=headers, json = payload)
	return(response.text.encode('utf8'))
