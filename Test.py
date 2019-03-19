import unittest
import SEEK

PROT_DEFAULT_AUTHENTICATION_STRING = "DEFAULT"

class TestSEEK(unittest.TestCase):

    def setUp(self):

        self.auth = (PROT_DEFAULT_AUTHENTICATION_STRING,
                     PROT_DEFAULT_AUTHENTICATION_STRING)

        self.testObject = SEEK.module(self.auth)

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
    def test_InitWithoutAuth(self):
        
        self.testObject = SEEK.module()

        self.assertNotEqual(self.testObject.session.auth, None, 
                            "Request should have these credentials")

    # def test_AuthNotWorking(self):

    # Testing the request of an existent object
    def test_RequestReturnsTrue(self):

        self.assertTrue(self.testObject.request(type="assays", id="576"), 
                        "This request should return true")

    # Testing the request of an inexistent object
    def test_RequestReturnsFalse(self):

        self.assertFalse(self.testObject.request(type="assays", id="0"), 
                        "This request should return false")

if __name__ == '__main__':

    unittest.main()