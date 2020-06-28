import requests
url = "https://sandbox.api.visa.com/merchantsearch/v1/search"
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic NktRNzNBS0tBNVY4U1A4QjlZNlcyMWY5QVA1V1RGLUVtNV9QRE12VDg2Y0hpTUgySTpzalRrY3RWdGNmb05NcFRHdTZtNVV3b01XNjls',
  'Content-Type': 'application/json'
}

def merchantsearch(merchantName,,merchantPostalCode)
    payload = " \r\n{\r\n\"searchAttrList\": {\r\n\"merchantName\": \"STARBUCKS\", \
                                            \r\n\"merchantCity\": \"SAN FRANCISCO\",\
                                            \r\n\"merchantState\": \"CA\",\
                                            \r\n\"merchantPostalCode\": \"94127\",\
                                            \r\n\"merchantCountryCode\": \"840\"\r\n},\
                \r\n\"responseAttrList\": [\r\n\"GNSTANDARD\"\r\n],\
                \r\n\"searchOptions\": {\r\n\"wildCard\": [\r\n\"merchantName\"\r\n],\
                                        \r\n\"maxRecords\": \"5\",\
                                        \r\n\"matchIndicators\": \"true\",\
                                        \r\n\"matchScore\": \"true\",\
                                        \r\n\"proximity\": [\r\n\"merchantName\"\r\n]\r\n},\
                \r\n\"header\": {\r\n\"requestMessageId\": \"Request_001\",\
                                \r\n\"startIndex\": \"0\",\
                                \r\n\"messageDateTime\": \"2020-06-26T17:49:01.903\"\r\n}\r\n}"



    response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
