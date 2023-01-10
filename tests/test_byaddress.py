import unittest
from byaddress import AddressFinder

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

class TestAddress(unittest.TestCase):


    # sample csv file 
    test_data_file = 'test_data.csv'

    def test__repr__(self):
        rep = AddressFinder(self.test_data_file)
        self.assertEqual(rep.__repr__(), "AddressFinder(test_data.csv)")

    """    
    def test_post_soup(self):
        post_url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'
        data = {'companyName':'BEND PAWN & TRADING CO-LAPINE','address1':'52504 U.S. 97', 'city':'LA PINE', 'state':'OR', 'zip':97739}
    """

if __name__ == '__main__':
    unittest.main()