from bs4 import BeautifulSoup
import requests
import csv
import re

# URL of the address search site
post_url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

# sample csv file 
csv_original_file = 'Python Quiz Input - Sheet1.csv'

# used to search for a 'success' result from scraping output
valid_address_pattern = re.compile("SUCCESS")

class AddressFinder:
    
    def __init__(self, csv_org_file):
        self.__csv_org_file = csv_org_file

    def get_post_soup(self, url, data):
        '''returns a beautifulsoup object of POST method'''
        response = requests.post(url, data=data, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        results = soup.find('p')
        return results.text

    def get_list_of_addresses(self):
        '''reads a csv file and iterates to a list with a 
        dictionary of address data. '''
        
        # list to hold the data from the address file
        address_list = []
        
        # opens the .csv file and reads the data to address_list 
        with open(self.__csv_org_file, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                address_list.append(row)
        
        return address_list

    def get_payload(self, a_list):
        '''formats the dictionary keys to be accepted for posting.'''

        # list of keys to be used as the accepted post key data
        post_keys = ['companyName','address1', 'city', 'state', 'zip']
        
        # list of values 
        post_values = list(a_list.values())
        
        post_payload = {}
        for i in range(len(post_keys)):                
            post_payload[post_keys[i]]= post_values[i]
        
        return post_payload

    def validate_address(self, list_address_dict):
        '''Valdiates the address and returns a list of the address dictionaries,
        with the additional validation column.'''

        validated_data = []

        for i in range(len(list_address_dict)):
            validated_data.append(self.get_payload(list_address_dict[i]))
        
        for i in range(len(validated_data)):
            address_search = self.get_post_soup(post_url, validated_data[i])
            if valid_address_pattern.search(address_search):
                # uncomment print statements for terminal output
                # print(f"Address for {validated_data[i]['companyName']} is Valid")
                validated_data[i].update({'addressStatus':'Valid'})
            else:
                # print(f"Address for {validated_data[i]['companyName']} is Not Valid")
                validated_data[i].update({'addressStatus':'Not Valid'})
        
        return validated_data

    def saveResults(self, address_list):
        ''' Writes a csv file, with additional column of "valid" '''
        row = address_list
        with open(self.__csv_org_file, 'w') as csv_mod_file:
            fieldnames = ['Company', 'Street', 'City', 'St', 'ZIPCode', 'AddressStatus']
            
            csv_writer = csv.DictWriter(csv_mod_file, fieldnames=fieldnames)

            csv_writer.writeheader()

            for i in range(len(row)):
                write_to_row = {
                    'Company': f'{row[i]["companyName"]}', 
                    'Street': f'{row[i]["address1"]}', 
                    'City': f'{row[i]["city"]}', 
                    'St': f'{row[i]["state"]}', 
                    'ZIPCode': f'{row[i]["zip"]}', 
                    'AddressStatus': f'{row[i]["addressStatus"]}'}

                csv_writer.writerow(write_to_row)

"""
def post_soup(url, data):
    '''returns a beautifulsoup object of POST method'''
    response = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find('p')
    return results.text

def get_list_of_addresses(csv_file):
    '''reads a csv file and iterates to a list with a 
    dictionary of address data. '''
    
    # list to hold the data from the address file
    address_list = []
    
    # opens the .csv file and reads the data to address_list 
    with open(csv_file, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            address_list.append(row)
    
    return address_list

def get_payload(a_list):
    '''formats the dictionary keys to be accepted for posting.'''

    # list of keys to be used as the accepted post key data
    post_keys = ['companyName','address1', 'city', 'state', 'zip']
    
    # list of values 
    post_values = list(a_list.values())
    
    post_payload = {}
    for i in range(len(post_keys)):                
        post_payload[post_keys[i]]= post_values[i]
    
    return post_payload

def validate_address(list_address_dict, url_to_post):
    '''Valdiates the address and returns a list of the address dictionaries,
    with the additional validation column.'''

    validated_data = []

    for i in range(len(list_address_dict)):
        validated_data.append(get_payload(list_address_dict[i]))
    
    for i in range(len(validated_data)):
        address_search = post_soup(url_to_post, validated_data[i])
        if valid_address_pattern.search(address_search):
            # uncomment print statements for terminal output
            # print(f"Address for {validated_data[i]['companyName']} is Valid")
            validated_data[i].update({'addressStatus':'Valid'})
        else:
            # print(f"Address for {validated_data[i]['companyName']} is Not Valid")
            validated_data[i].update({'addressStatus':'Not Valid'})
    
    return validated_data

def saveResults(csv_address_File, address_list):
    ''' Writes a csv file, with additional column of "valid" '''
    row = address_list
    with open(csv_address_File, 'w') as csv_mod_file:
        fieldnames = ['Company', 'Street', 'City', 'St', 'ZIPCode', 'AddressStatus']
        
        csv_writer = csv.DictWriter(csv_mod_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for i in range(len(row)):
            write_to_row = {
                'Company': f'{row[i]["companyName"]}', 
                'Street': f'{row[i]["address1"]}', 
                'City': f'{row[i]["city"]}', 
                'St': f'{row[i]["state"]}', 
                'ZIPCode': f'{row[i]["zip"]}', 
                'AddressStatus': f'{row[i]["addressStatus"]}'}

            csv_writer.writerow(write_to_row)
"""

def main():
    """list_of_addresses = get_list_of_addresses(csv_original_file)

    val_list = validate_address(list_of_addresses, post_url)
    
    saveResults(csv_original_file, val_list)"""

    search = AddressFinder(csv_original_file)
    list_address = search.get_list_of_addresses()
    validated_address_list = search.validate_address(list_address)
    search.saveResults(validated_address_list)


if __name__ == '__main__':
    main()
    