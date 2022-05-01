from bs4 import BeautifulSoup
import requests
import csv
import re

# URL of the address search site
base_url = 'https://tools.usps.com/zip-code-lookup.htm?byaddress'
post_url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

# original csv file to be used
csv_original_file = 'Python Quiz Input - Sheet1.csv'

# modified csv file to be used 
csv_modified_file = 'Python Quiz Input - Sheet1_Modified.csv'

valid_address_pattern = re.compile("SUCCESS")

def get_soup(url):
    '''Returns a beautifulSoup object of GET method'''
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def post_soup(url, data):
    '''returns a beautifulsoup object of POST method'''
    response = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find('p')
    return results.text

# Step one read csv to the address_dict list
def listAddress(address_file):
    '''iterates through a csv file and appends a list 
    with a dictionary of address information. '''
    
    # list to hold the data from the address file
    address_list = []
    
    # opens the .csv file and reads the data to address_list 
    with open(address_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            address_list.append(row)
    
    return address_list

def payload_list(a_list):
    '''formats the dictionary keys to be acceptable for posting.'''
    post_keys = ['companyName','address1', 'city', 'state', 'zip']
    post_values = list(a_list.values())
    
    post_payload = {}
    for i in range(len(post_keys)):                
        post_payload[post_keys[i]]= post_values[i]
    
    return post_payload

def validate_address(csv_file, url_to_post):
    '''Valdiates the address adn returns a list of dictionaries,
    with the additional validation column.'''

    list_Of_Original_Addresses = listAddress(csv_file)
   
    payload_data = []

    for i in range(len(list_Of_Original_Addresses)):
        payload_data.append(payload_list(list_Of_Original_Addresses[i]))
    
    for i in range(len(payload_data)):
        address_search = post_soup(url_to_post, payload_data[i])
        if valid_address_pattern.search(address_search):
            print(f"Address for {payload_data[i]['companyName']} is Valid")
            payload_data[i].update({'addressStatus':'Valid'})
        else:
            print(f"Address for {payload_data[i]['companyName']} is Not Valid")
            payload_data[i].update({'addressStatus':'Not Valid'})
    
    return payload_data

def validated_list(validated_list):
    '''formats the dictionary keys of a validated list to the original values'''
    post_keys = ['Company', 'Street', 'City', 'St', 'ZIPCode', 'AddressStatus']
    for i in range(len(validated_list)):
        post_values = list(validated_list.values())
    
    post_payload = {}
    for i in range(len(post_keys)):                
        post_payload[post_keys[i]]= post_values[i]
    
    return post_payload

def saveResults(csv_address_File, address_list):
    ''' Writes a csv file, with additional column of "valid" '''

    row = address_list

    #post_values = list(address_list.values())

    post_payload = {}

    with open(csv_address_File, 'w') as csv_mod_file:
        fieldnames = ['Company', 'Street', 'City', 'St', 'ZIPCode', 'AddressStatus']
        
        csv_writer = csv.DictWriter(csv_mod_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for i in range(len(row)):
            csv_writer.writerow({'Company': f'{row[i]["companyName"]}', 'Street': f'{row[i]["address1"]}', 'City': f'{row[i]["city"]}', 'St': f'{row[i]["state"]}', 'ZIPCode': f'{row[i]["zip"]}', 'AddressStatus': f'{row[i]["addressStatus"]}'})

if __name__ == '__main__':
    val_list = validate_address(csv_original_file, post_url)
    saveResults(csv_modified_file, val_list)