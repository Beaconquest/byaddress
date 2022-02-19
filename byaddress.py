import requests
import csv

with open('Python Quiz Input - Sheet1.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    address_dict = []
    for row in csv_reader:
        address_dict.append(row)

# for i in range(len(address_dict)):
#     print(address_dict[i])


URL = 'https://tools.usps.com/zip-code-lookup.htm?byaddress'
address_data = {'tCompany': 'CASH AMERICA PAWN', 'tAddress': '2618 W INTERSTATE 20', 'tCity': 'GRAND PRAIRIE', 'tUrbanCode': 'TX', 'tZip-byaddress': '75052-7031'}
resp = requests.get(URL, params=address_data, headers={'user-agent': 'webscrapper.py'}, allow_redirects=False)
print(resp.json())