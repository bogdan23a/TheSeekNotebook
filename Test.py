import unittest
from unittest.mock import patch
import SEEK
import WriteObject
import getpass

PROT_DEFAULT_AUTHENTICATION_STRING = "DEFAULT"

class TestSEEK(unittest.TestCase):

    def setUp(self):

        self.auth = (PROT_DEFAULT_AUTHENTICATION_STRING,
                     PROT_DEFAULT_AUTHENTICATION_STRING)

        self.testObject = SEEK.module(self.auth)
        self.testSearch = SEEK.module(self.auth)

    def tearDown(self):

        del self.auth

        del self.testObject
    
    # Testing object initialization with authentication
    def test_InitWithAuth(self):

        self.assertEqual(self.testObject.session.auth,
                        (PROT_DEFAULT_AUTHENTICATION_STRING,
                        PROT_DEFAULT_AUTHENTICATION_STRING), 
                        "Request should have these credentials")

    # Testing object initialization without authentication
    @patch('SEEK.module.get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_InitWithoutAuth(self ,username, password):
        
        self.testObject = SEEK.module()

        self.assertEqual(self.testObject.session.auth, 
                        (PROT_DEFAULT_AUTHENTICATION_STRING,
                         PROT_DEFAULT_AUTHENTICATION_STRING), 
                            "Request should require user input")
                            

    # def test_AuthNotWorking(self):

    # Testing the request of an existent object
    def test_RequestReturnsTrue(self):

        self.assertTrue(self.testObject.request(type="assays", id="576"), 
                        "This request should return true")

    # Testing the request of an inexistent object
    def test_RequestReturnsFalse(self):

        self.assertFalse(self.testObject.request(type="assays", id="0"), 
                        "This request should return false")
    
    def test_RequestHasError(self):

        self.testObject.base_url = "wrong.url.com"
        self.assertRaises(Exception, self.testObject.request(type="assays", 
                                                            id="576"),
                          "This request should return error")

    @patch('SEEK.module.get_input', return_value='1')
    def testSearchAdvancedSetup(self, input):

        self.testSearch.searchAdvancedSetup()
        self.assertEqual(self.testSearch.searchResultsPerThread, 1)
        self.assertEqual(self.testSearch.relationshipsPerThread, 1)

    @patch('SEEK.module.get_input', return_value='what')
    def testSearchAdvancedSetupWithWrongInput(self, input):

        self.testSearch.searchAdvancedSetup()
        self.assertRaises(Exception, self.testSearch.searchResultsPerThread)
        self.assertRaises(Exception, self.testSearch.relationshipsPerThread)


if __name__ == '__main__':

    unittest.main()