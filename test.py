import getpass
from io import StringIO
import json
import sys
import SEEK
import unittest
from unittest import TestCase
from unittest.mock import patch


PROT_DEFAULT_AUTHENTICATION_STRING = "DEFAULT"

class TestSEEK(TestCase):

    def setUp(self):

        self.auth = (PROT_DEFAULT_AUTHENTICATION_STRING,
                    PROT_DEFAULT_AUTHENTICATION_STRING)

        self.testOBJ = SEEK.read(self.auth)

        self.goodFormat_RequestList = [{'id':'281','type':'investigations'},
                                       {'id':'953','type':'assays'}]
        
        self.empty_RequestList = [{}]

        self.badRequest_RequestList = [{'id':'1','type':'wrong type'}]

        self.badFormat_RequestList = {'id':'1','type':'assays',
                                      'id':'2','type':'assays'}
    
    def tearDown(self):

        del self.auth

        del self.testOBJ

        del self.goodFormat_RequestList

        del self.badFormat_RequestList



    # @patch("SEEK.read.get_input", "some input")
    # def test_get_input_Method(self):
        
    #     self.assertEqual(self.testOBJ.get_input("Prompt:"), "some input")

    # @patch("SEEK.read.get_input_testing", "some other input")
    # def test_get_input_testing_Method(self):
        
    #     self.assertEqual(self.testOBJ.get_input_testing("Prompt:"), 'some other input')
    
    def test_init_WithAuth(self):

        self.assertEqual(self.testOBJ.session.auth,
                        (PROT_DEFAULT_AUTHENTICATION_STRING,
                        PROT_DEFAULT_AUTHENTICATION_STRING))

    @patch('SEEK.read.get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_init_WithoutAuth(self, username, password):

        self.testOBJ = SEEK.read()

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

    @patch("SEEK.read.get_input", return_value='3')
    @patch("SEEK.read.get_input_testing", return_value='10')
    def test_searchAdvancedSettings_Method(self, srpt, rpt):
        
        self.testOBJ.searchAdvancedSetup()
        self.assertEqual(self.testOBJ.searchResultsPerThread, 3)
        self.assertEqual(self.testOBJ.relationshipsPerThread, 10)

    # @patch("SEEK.read.get_input", return_value='douazecisitrei')
    # @patch("SEEK.read.get_input_testing", return_value='august')
    # def test_searchAdvancedSettings_Method_BadInput(self, srpt, rpt):
        
    #     self.assertRaises(Exception, self.testOBJ.searchAdvancedSetup)

    def test_print(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.request("assays","576")

        self.testOBJ.print()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(), 
        "PGK 70C model(id: 576 | type: assays)\n\nDescription: PGK 70C model\n\n\nObject has no relationships\n")
    
    @patch("SEEK.read.get_input", return_value="liver")
    @patch("SEEK.read.get_input_testing", return_value="assays")
    def test_APISearch_Method(self, keyword, type):
        
        self.assertTrue(self.testOBJ.APISearch())

    @patch("SEEK.read.get_input", return_value="liver")
    @patch("SEEK.read.get_input_testing", return_value="wrong type")
    def test_APISearch_Method_BadRequest(self, keyword, type):
        
        self.assertFalse(self.testOBJ.APISearch())

    @patch("SEEK.read.get_input", return_value="liver")
    @patch("SEEK.read.get_input_testing", return_value="assays")
    def test_createRequestList_Method(self, keyword, type):
        
        self.testOBJ.APISearch()
        self.testOBJ.createRequestList()

        self.assertTrue(len(self.testOBJ.requestList) ,6)

    def test_makeRequests_Method(self):
        
        self.testOBJ.makeRequests(self.goodFormat_RequestList, 
                                  len(self.goodFormat_RequestList))

        properties = [
            'attributes', 
            'id', 
            'type', 
            'links', 
            'meta', 
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))
    
    def test_makeRequests_Method_EmptyList(self):
        
        self.assertRaises(Exception, 
                         self.testOBJ.makeRequests(self.empty_RequestList, 
                                                   len(self.empty_RequestList)))

    def test_makeRequests_Method_ListWithBadItem(self):
        
        self.assertRaises(Exception, 
                          self.testOBJ.makeRequests(self.badRequest_RequestList, 
                                              len(self.badRequest_RequestList)))

        # properties = [
        #     'attributes', 
        #     'id', 
        #     'type', 
        #     'links', 
        #     'meta', 
        #     'relationships']

        # # for request in self.testOBJ.requestList:
        # for prop in properties:
        #     self.assertNotIn(prop, dir(self.testOBJ.requestList[0].data))
    
    def test_makeRequests_Method_BadFormat(self):
        
        self.assertRaises(Exception, 
                         self.testOBJ.makeRequests(self.badFormat_RequestList, 
                                                   len(self.badFormat_RequestList)))

    def test_parallelRequest_Method(self):
        
        self.testOBJ.parallelRequest(self.goodFormat_RequestList, 1)
        for thread in self.testOBJ.threadList:
            thread.join()

        properties = [
            'attributes', 
            'id', 
            'type', 
            'links', 
            'meta', 
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))
    
    def test_parallelRequest_Method_ManyRequestPerThread(self):
        
        self.testOBJ.parallelRequest(self.goodFormat_RequestList, 15)
        for thread in self.testOBJ.threadList:
            thread.join()

        properties = [
            'attributes', 
            'id', 
            'type', 
            'links', 
            'meta', 
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))

    def wait(self, rList):
                        
        self.testOBJ.parallelRequest(rList, 1)
        for thread in self.testOBJ.threadList:
            thread.join()

    def test_parallelRequest_Method_EmptyRequestList(self):
        
        self.assertRaises(Exception, self.wait(self.empty_RequestList))

    def test_parallelRequest_Method_ZeroRequestsPerThread(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList, 0)
        for thread in self.testOBJ.threadList:
            thread.join()

        properties = [
            'attributes', 
            'id', 
            'type', 
            'links', 
            'meta', 
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))

    def test_parallelRequest_Method_BadRequestList(self):

        self.assertRaises(Exception, self.wait(self.badRequest_RequestList))

    def test_createRelationshipsList_Method(self):
        
        self.testOBJ.parallelRequest(self.goodFormat_RequestList,1)
        for thread in self.testOBJ.threadList:
            thread.join()
        
        self.testOBJ.createRelationshipList()
        self.assertEqual(len(self.testOBJ.relationshipList), 17)

    def test_removeDuplicateRelationships_Method(self):
        pass

    def test_removeDuplicateRelationships_Method_ZeroRelationships(self):
        pass

    def test_removeDuplicateRelationships_Method_BadRequestList(self):
        pass

    def test_substituteRelationships_Method(self):
        
        self.testOBJ.parallelRequest(self.goodFormat_RequestList,1)
        for thread in self.testOBJ.threadList:
            thread.join()
        
        self.testOBJ.createRelationshipList()
        self.testOBJ.substituteRelationships(self.testOBJ.relationshipList,
                                            len(self.testOBJ.relationshipList))
        self.assertEqual(1,1)

    def test_substituteRelationships_Method_EmptyRequestList(self):
        pass

    def test_search_Method(self):
        pass

    def test_find_Method(self):
        pass

if __name__ == '__main__':
    unittest.main()