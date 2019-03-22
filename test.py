import json
from io import StringIO
import sys
import unittest
from unittest import TestCase
from unittest.mock import patch
import SEEK
# import WriteObject
import getpass

PROT_DEFAULT_AUTHENTICATION_STRING = "DEFAULT"

class TestSEEK(TestCase):

    def setUp(self):

        self.auth = (PROT_DEFAULT_AUTHENTICATION_STRING,
                    PROT_DEFAULT_AUTHENTICATION_STRING)

        self.testOBJ = SEEK.module(self.auth)

        self.goodFormat_RequestList = {'id':'1','type':'assays',
                                       'id':'2','type':'assays'}

        self.badFormat_RequestList = {'id':'0','type':'assays',
                                       'id':'2','type':'assay'}

    
    def tearDown(self):

        del self.auth

        del self.testOBJ

        del self.goodFormat_RequestList

        del self.badFormat_RequestList

    @patch("SEEK.module.get_input", "some input")
    def test_get_input_Method(self):
        
        self.assertEqual(self.testOBJ.get_input, "some input")

    @patch("SEEK.module.get_input_testing", "some other input")
    def test_get_input_testing_Method(self):
        
        self.assertEqual(self.testOBJ.get_input_testing, 'some other input')
    
    def test_init_WithAuth(self):

        self.assertEqual(self.testOBJ.session.auth,
                        (PROT_DEFAULT_AUTHENTICATION_STRING,
                        PROT_DEFAULT_AUTHENTICATION_STRING))

    @patch('SEEK.module.get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_init_WithoutAuth(self, username, password):

        self.testOBJ = SEEK.module()

        self.assertEqual(self.testOBJ.session.auth,
                         (PROT_DEFAULT_AUTHENTICATION_STRING,
                          PROT_DEFAULT_AUTHENTICATION_STRING))
    
    def test_loadJSON_Method(self):
        
        r = self.testOBJ.session.get(self.testOBJ.base_url + "assays/576")
            
        self.testOBJ.session.close()

        self.testOBJ.json = r.json()
        self.testOBJ.loadJSON(self.testOBJ, self.testOBJ.json['data'])

        for item in ['attributes','id','links','meta','relationships','type']:
            self.assertIn(item, dir(self.testOBJ.data))

    def test_request_Method(self):
        self.assertTrue(self.testOBJ.request(type="assays", id="576"))

    def test_request_Method_BadRequest(self):
        self.assertFalse(self.testOBJ.request(type="assays", id="0"))

    def test_request_Method_HasError(self):

        self.testOBJ.base_url = "www.wrong.url.com/"
        self.assertRaises(Exception, 
                            self.testOBJ.request(type="assays", id="576"))
    
    def test_printAttributes(self):
        
        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.request("assays","576")

        self.testOBJ.printAttributes()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(), 
        "PGK 70C model(id: 576 | type: assays)\n\nDescription: PGK 70C model\n")

    def test_printRelationships(self):
        
        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.request("assays","576")

        self.testOBJ.printRelationships()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(), 
                                            "Object has no relationships\n")

    def test_print(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.request("assays","576")

        self.testOBJ.print()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(), 
        "PGK 70C model(id: 576 | type: assays)\n\nDescription: PGK 70C model\n\n\nObject has no relationships\n")
    
    @patch("SEEK.module.get_input", return_value="liver")
    @patch("SEEK.module.get_input_testing", return_value="assays")
    def test_APISearch_Method(self, keyword, type):
        
        self.assertTrue(self.testOBJ.APISearch())

    @patch("SEEK.module.get_input", return_value="liver")
    @patch("SEEK.module.get_input_testing", return_value="wrong type")
    def test_APISearch_Method_BadRequest(self, keyword, type):
        
        self.assertFalse(self.testOBJ.APISearch())

    @patch("SEEK.module.get_input", return_value="liver")
    @patch("SEEK.module.get_input_testing", return_value="assays")
    def test_createRequestList_Method(self, keyword, type):
        
        self.testOBJ.APISearch()
        self.testOBJ.createRequestList()

        self.assertTrue(len(self.testOBJ.requestList) ,6)

    def test_makeRequests_Method(self):
        pass
    
    def test_makeRequests_Method_EmptyList(self):
        pass

    def test_makeRequests_Method_ListWithBadItem(self):
        pass

    def test_parallelRequest_Method(self):
        pass

    def test_parallelRequest_Method_EmptyRequestList(self):
        pass

    def test_parallelRequest_Method_ZeroRequestsPerThread(self):
        pass

    def test_parallelRequest_Method_BadRequestList(self):
        pass

    def test_createRelationshipsList_Method(self):
        pass

    def test_createRelationshipsList_Method_EmptyRequestList(self):
        pass

    def test_createRelationshipsList_Method_BadRequestList(self):
        pass

    def test_removeDuplicateRelationships_Method(self):
        pass

    def test_removeDuplicateRelationships_Method_ZeroRelationships(self):
        pass

    def test_removeDuplicateRelationships_Method_BadRequestList(self):
        pass

    def test_substituteRelationships_Method(self):
        pass

    def test_substituteRelationships_Method_EmptyRequestList(self):
        pass

    def test_search_Method(self):
        pass

    def test_find_Method(self):
        pass

if __name__ == '__main__':
    unittest.main()