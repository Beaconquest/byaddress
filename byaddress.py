# byaddress.py
# script take an an csv file of usa address
# searches the data of the file from usps.com 
# returns a csv file with an extra line to confirm if the address exists

from bs4 import BeautifulSoup

import requests
import csv
import re
import argparse

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}
POST_URL:str = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress' 

class AddressFinder:

    # used to search for a 'success' result from scraping output
    valid_address_indicator = re.compile("SUCCESS")
    
    def __init__(self, csv_org_file):
        self.__csv_org_file = csv_org_file
        self.post_url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress' 
    
    def __repr__(self):
        return f"AddressFinder({self.__csv_org_file})"

    def get_post_soup(self, url, data):
        '''returns a beautifulsoup object of POST method'''
        response = requests.post(url, data=data, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        results = soup.find('p')
        return results.text

    def get_list_of_addresses(self):
        '''reads a csv file and iterates to a list with a 
        dictionary of address data.'''
        
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
            address_search = self.get_post_soup(self.post_url, validated_data[i])
            if self.valid_address_indicator.search(address_search):
                # uncomment print statements for terminal output
                # print(f"Address for {validated_data[i]['companyName']} is Valid")
                validated_data[i].update({'addressStatus':'Valid'})
            else:
                # print(f"Address for {validated_data[i]['companyName']} is Not Valid")
                validated_data[i].update({'addressStatus':'Not Valid'})
        
        return validated_data

    def saveResults(self, address_list):
        ''' Writes a csv file, with additional column of "valid" '''

        row: list = address_list
        with open(csv_org_file, 'w') as csv_mod_file:
            fieldnames: list = ['Company', 'Street', 'City', 'St', 'ZIPCode', 'AddressStatus']
            
            csv_writer = csv.DictWriter(csv_mod_file, fieldnames=fieldnames)

            csv_writer.writeheader()

            # NEED TO CLEAN THIS PORTION
            for i in range(len(row)):
                write_to_row = {
                    'Company': f'{row[i]["companyName"]}', 
                    'Street': f'{row[i]["address1"]}', 
                    'City': f'{row[i]["city"]}', 
                    'St': f'{row[i]["state"]}', 
                    'ZIPCode': f'{row[i]["zip"]}', 
                    'AddressStatus': f'{row[i]["addressStatus"]}'}

                csv_writer.writerow(write_to_row)

    def get_list_of_addresses(self) -> list:
        '''reads a csv file and iterates to a list with a 
        dictionary of address data.'''
        
        # list to hold the data from the address file
        address_list = []
        
        # opens the .csv file and reads the data to address_list 
        with open(self.__csv_org_file, 'r') as f:
            csv_reader: dict = csv.DictReader(f)
            for row in csv_reader:
                address_list.append(row)
        
        return address_list

class USPS:
    """Gets data from the the USPS website."""

    def __init__(self, url, headers) -> None:
        self.__url = url
        self.__headers = headers

    def get_post_soup(self, url: str, headers, data) -> str:
        '''returns a beautifulsoup object of POST method'''
        
        response = requests.post(url, data=data, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        results = soup.find('p')
        return results.text
    
    
class AddressFinder:

    # used to search for a 'success' result from scraping output
    valid_address_indicator = re.compile("SUCCESS")
    
    def __init__(self, csv_org_file) -> None:
        self.__csv_org_file = csv_org_file
        self.post_url: str = 
    
    def __repr__(self):
        return f"AddressFinder({self.__csv_org_file})"

    def get_payload(self, a_list: list) -> dict:
        '''formats the dictionary keys to be accepted for posting.'''

        post_keys: list = ['companyName','address1', 'city', 'state', 'zip']
        
        post_values: list = list(a_list.values())
        
        post_payload: dict = {}

        for i in range(len(post_keys)):                
            post_payload[post_keys[i]]= post_values[i]
        
        return post_payload

    def validate_address(self, list_address_dict: list) -> list:
        '''Valdiates the address and returns a list of the address dictionaries,
        with the additional validation column.'''

        validated_data: list = []

        for i in range(len(list_address_dict)):
            validated_data.append(self.get_payload(list_address_dict[i]))
        
        for i in range(len(validated_data)):
            address_search = self.get_post_soup(self.post_url, validated_data[i])
            if self.valid_address_indicator.search(address_search):
                validated_data[i].update({'addressStatus':'Valid'})
            else:
                validated_data[i].update({'addressStatus':'Not Valid'})
        
        return validated_data

def main():
    search = AddressFinder(csv_original_file)
    list_address = search.get_list_of_addresses()
    validated_address_list = search.validate_address(list_address)
    search.saveResults(validated_address_list)


if __name__ == '__main__':
    main()
    