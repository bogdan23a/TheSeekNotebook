import json
import requests
import threading
import getpass
import time
from IPython.core.display import display, HTML

class module:

    def __init__(self, auth = None):

        self.base_url = 'http://www.fairdomhub.org/'
            
        self.headers = {"Content-type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Connection": "close",
            "Accept-Charset": "ISO-8859-1"}

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        if auth != None:
            self.session.auth = auth
        else:
            self.session.auth = (input("Username: "), 
                                 getpass.getpass("Password: "))

        self.json = None
        self.data = object()

        self.searchChoices = ["assays",
        "data_files",
        "events",
        "institutions",
        "investigations",
        "models",
        "organisms",
        "people",
        "presentations",
        "programmes",
        "projects",
        "publications",
        "sample_types",
        "sops",
        "studies",
        "all"]       

        self.requestList = []
        self.relationshipList = []
        self.requestFails = 0
        self.percentageLoaded = 0
        self.threadList = []

        self.requestList = []
        self.searchResultsPerThread = 4
        self.relationshipsPerThread = 10

        self.time = {'start': 0, 'end': 0}

    def request(self, type, id):

        r = None

        try:
            r = self.session.get(self.base_url + type + "/" + id)

            if r.status_code != 200:
                return False

            self.json = r.json()
            self.loadJSON(self, self.json['data'])
            
            return True

        except Exception as e:
            print(str(e))

    def loadJSON(self, layerName, layer):

        layerName = lambda: None
        
        if hasattr(layer,'items'):
            for key, value in layer.items():
                
                if hasattr(value, 'items') == True:
                    setattr(layerName, key, self.loadJSON(key, value))
                else:
                    setattr(layerName, key, value)
        else:
            for item in layer:
                for key, value in item.items():
                        
                    if hasattr(value, 'items') == True:
                        setattr(layerName, key, self.loadJSON(key, value))
                    else:
                        setattr(layerName, key, value)

        setattr(self,'data', layerName)

        return layerName

    def print(self):

        if hasattr(self, 'data'):
            if hasattr(self.data, 'attributes'):
                self.printAttributes()
                print("\n")
            if hasattr(self.data, 'relationships'):
                self.printRelationships()
        else:
            print("Search item unavailable. Try again later.")

    def printAttributes(self):

        print(self.data.attributes.title + "(id: " + self.data.id + " | type: " + self.data.type +")\n")

        print("Description: ", end="")
        if hasattr(self.data.attributes, 'description') and self.data.attributes.description != None:
            print(self.data.attributes.description)
        else:
            print("missing")

    def printRelationships(self):

        hasNoRelationships = True

        for relation in dir(self.data.relationships):
            if relation[:2] != "__":

                r = getattr(self.data.relationships, relation)
            
                if r.data != [] and hasattr(r, 'newData'):
                        
                    print(relation.upper())
                    for data in r.newData:
                        hasNoRelationships = False
                        print(data.data.attributes.title)
            
        if hasNoRelationships:
            print("Object has no relationships")

    # Set up the multithreading amount
    def searchAdvancedSetup(self):

        display(HTML('<h3>Search multithreading</h3>'))
        print("Decide how fast will the search run\n")
        print("Search results are usually less and the search requires less to be requested at once.")
        print("Relationships are usually a lot more, therefore it requires more requests at once")
        self.searchResultsPerThread = int(input("How many search results should be requested per thread: "))
        self.relationshipsPerThread = int(input("How many relationships should be requested per thread: "))

    # Simplified method for the user in order to operate a browsing in the SEEK API
    def search(self):

        # Begin the search by inputing the search term
        self.searchTerm = input("Enter your search: \n")
        
        # Choose the category of search
        choice = None
        while choice not in self.searchChoices:
            choice = input("Please enter one of: " + ', '.join(self.searchChoices) + ": ")
        self.searchType = choice

        # Process the request and retrieve the JSON
        payload = {'q': self.searchTerm, 'search_type': self.searchType}
        r = self.session.get(self.base_url + 'search', headers=self.headers, params=payload)
        r.raise_for_status()
        self.json = r.json()

        # Create the request list of the form [{'id':'x', 'type':'y'}]
        self.createRequestList()

        print("\n" + str(len(self.requestList)) + " results found",end='')

        # Create a paralelized request for each search result
        # 1st param: the search results to be requested
        # 2nd param: the total amount of request 
        # 3rd param: the number of request per thread for the paralelization
        self.time['start'] = time.time()
        
        ps = module(self.session.auth)
        ps.parallelRequest(self.requestList, requestPerThread=self.searchResultsPerThread)

        # Wait for the requests to finish in order to continue
        for thread in ps.threadList:
            thread.join()

        self.time['end'] = time.time()
         
        print("\n" + str(ps.requestFails) + " ommited results (" + str(int(self.time['end'] - self.time['start'])) + " s elapsed)")

        # Get the total number of places where there is a relationship
        totalNumberRelationships = ps.createRelationshipList()

        ps.removeDuplicateRelationships()

        print("\n" + str(len(ps.relationshipList)) + " relationships found",end='')       

        # Create a paralelized request for each relationship in the search results 
        self.time['start'] = time.time()

        PS = module(self.session.auth)
        PS.parallelRequest(ps.relationshipList, requestPerThread=self.relationshipsPerThread)

        # Wait for the requests to finish in order to continue
        for thread in PS.threadList:
            thread.join()
        
        self.time['end'] = time.time()

        print("\n" + str(PS.requestFails) + " ommited results (" + str(int(self.time['end'] - self.time['start'])) + " s elapsed)")

        ps.substituteRelationships(PS.requestList, totalNumberRelationships)

        self.requestList = ps.requestList
        print("\n\n                                        --SEARCH RESULTS--\n\n")
        for request in ps.requestList:

            request.print()
            print('\n____________________________________________________________________________\n')
    
    # Used for Demo Presentation
    # Searches without sofisticated interpretaion
    # Process the request and retrieve the JSON
    def demoSearch(self):

        # Begin the search by inputing the search term
        self.searchTerm = input("Enter your search: \n")
        
        # Choose the category of search
        choice = None
        while choice not in self.searchChoices:
            choice = input("Please enter one of: " + ', '.join(self.searchChoices))
        self.searchType = choice

        # Process the request and retrieve the JSON
        payload = {'q': self.searchTerm, 'search_type': self.searchType}
        r = self.session.get(self.base_url + 'search', headers=self.headers, params=payload)
        r.raise_for_status()
        self.json = r.json()

    # Creates the list of requests by parsing a RAW Search Result JSON
    def createRequestList(self):

        requestList = []

        for item in self.json['data']:
            ID = ""
            TYPE = ""
            for prop in item.items():
                
                if prop[0] == 'id':
                    ID = prop[1]
                    
                if prop[0] == 'type':
                    TYPE = prop[1]
                
                
            requestList.append({'id':ID, 'type':TYPE})
        
        self.requestList = requestList       

    # Uses multithreading to read a number of request and retrieve results from the API
    # 1st param: the list of requests
    # 2nd param: the total number of requests
    # 3rd param: the number of requests that each thread has to process
    # return: none
    # Fills the 'requestList' attribute with the response
    def parallelRequest(self, requests, requestPerThread):
        
        # if len(requests) < 20:
        #     requestPerThread = 1
        # elif len(requests) < 100:
        #     requestPerThread = 2
        # elif len(requests) < 500:
        #     requestPerThread = 10
        # elif len(requests) < 1500:
        #     requestPerThread = 30
        # else:
        #     requestPerThread = 40

        # Compute the number of threads 
        if len(requests) % requestPerThread == 0:
            numberOfThreads = len(requests) // requestPerThread
        else: 
            numberOfThreads = len(requests) // requestPerThread + 1

        if requestPerThread > 10:
            print("(" + str(numberOfThreads * 5) + ' s estimated)')
        else:
            print("(" + str(numberOfThreads) + ' s estimated)')

        for currentThread in range(0, numberOfThreads):

            # Compute the index of the next batch of requests that are going to be processed
            if currentThread == (numberOfThreads - 1):
                rightArrayBound = len(requests)
            else:
                rightArrayBound = (currentThread + 1) * requestPerThread

            # Create the thread with the specified number of requests
            newThread = threading.Thread(name="Thread number " + str(currentThread), target=self.makeRequests, args=(requests[currentThread * requestPerThread : rightArrayBound], len(requests),))
            newThread.start()

            # Add the thread to the list of threads
            self.threadList.append(newThread)
    
    # Each thread executes this method
    # Loops through each batch of requests received and executes them in turn, serialized
    # 1st param: the request batch
    # 2nd param: the total number of requests
    def makeRequests(self, requestsList, total):

        for r in requestsList:

            try:
                # Create new request
                request = module(self.session.auth)
                
                # Check if it is successful
                if request.request(type=r['type'], id=r['id']) == False:
                    self.requestFails = self.requestFails + 1

                else:
                    # Compute percentace for user info
                    p = self.percentageLoaded / total * 100

                    if p >= (100 - (1 / total) * 100):
                        print("Loading " + str(round(p,2)) + "%\r", end='')
                        print("\rLoading Completed\n", end='')

                    else:
                        print("Loading " + str(round(p,2)) + "%\r", end='')

                    self.requestList.append(request)

                self.percentageLoaded = self.percentageLoaded + 1

            except Exception as e:

                print(str(e))

    # Create the relationship list by parsing the search result list
    # return: number of relations found
    def createRelationshipList(self):

        relations = []

        for request in self.requestList:
            
            if hasattr(request.data, 'relationships'):

                for relationship in dir(request.data.relationships):
                
                    if relationship[:2] != '__':
                        relation = getattr(request.data.relationships, relationship)

                        if type(relation.data) == type([{'id':'x','type':'y'}]) and relation.data != []:
                            for r in relation.data:
                                relations.append(r)

                        elif relation.data != []:
                            relations.append({'id':relation.data.id,'type':relation.data.type})

        self.relationshipList = relations

        return len(relations)
    
    # Substitute the information from the relationship list back to the original search results
    # 1st param: the relationship list (without duplicates)
    # 2nd param: the total number of relations in the search results that need to be filled out
    # return: none
    # Adds a 'newData' attribute in each search result relation
    def substituteRelationships(self, relationshipsList, total):
        
        print("\nSubstituting relationships into original search results: ")
        self.percentageLoaded = 0

        for i in self.requestList:

            if hasattr(i.data, 'relationships'):
                for r in range(0, len(dir(i.data.relationships))):
                    
                    if dir(i.data.relationships)[r][:2] != '__':
                        relation = getattr(i.data.relationships, dir(i.data.relationships)[r]) 

                        if type(relation.data) == type([{'id':'x','type':'y'}]) and relation.data != []:

                            for k in relation.data:
                                
                                ID = 0
                                TYPE = ''
                                for key, value in k.items():
                                    if key == 'id':
                                        ID = value
                                    if key == 'type':
                                        TYPE = value

                                # Search to match relation
                                for item in relationshipsList:

                                    # Check if relation in search results matches the one in the list
                                    if type(item.data) != type(object()) and item.data.id == ID and item.data.type == TYPE:
                                        
                                        # Compute percentace for user info
                                        p = round(self.percentageLoaded / total * 100, 2)
                                        
                                        if p >= (100 - (1 / total) * 100):    
                                            print("Loading " + str(p) + "%\r", end='')
                                            print("\nLoading Completed\r")
                                        else:
                                            print("Loading " + str(p) + "%\r", end='')

                                        self.percentageLoaded = self.percentageLoaded + 1
                                        
                                        if hasattr(relation, 'newData'):
                                            relation.newData.append(item)

                                            # Don't look anymore
                                            break
                                        else:
                                            relation.newData = []
                                            relation.newData.append(item)

                                            # Don't look anymore
                                            break

                        elif relation.data != []:

                            # Search to match relation
                            for item in relationshipsList:

                                # Check if relation in search result matches the one in the list                 
                                if type(item.data) != type(object()) and item.data.id == relation.data.id and item.data.type == relation.data.type:
                                    
                                    # Compute percentace for user info
                                    p = round(self.percentageLoaded / total * 100, 2)

                                    if p >= (100 - (1 / total) * 100):    
                                        print("Loading " + str(p) + "%\r", end='')
                                        print("\nLoading Completed\r")
                                    else:
                                        print("Loading " + str(p) + "%\r", end='')   
                                    
                                    self.percentageLoaded = self.percentageLoaded + 1

                                    if hasattr(relation, 'newData'):
                                        relation.newData.append(item)

                                        # Don't look anymore 
                                        break
                                    else:
                                        
                                        relation.newData = []
                                        relation.newData.append(item)

                                        # Don't look anymore
                                        break
    
    def removeDuplicateRelationships(self):
        
        noDuplicates = []
        for relation in self.relationshipList:
            
            if relation not in noDuplicates:
                
                noDuplicates.append(relation)

        self.relationshipList = noDuplicates

    def find(self, string):

        results = []

        for request in self.requestList:
            if string in request.data.attributes.title:
                results.append(request)
        
        return results