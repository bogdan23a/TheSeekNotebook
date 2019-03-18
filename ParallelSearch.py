from ReadObject import ReadObject
import threading

PROT_REQUESTS_PER_THREAD = 10

class ParallelSearch():

    def __init__(self):
        # super().__init__(self)

        self.requestList = []
        self.relationshipList = []
        self.requestFails = 0
        self.percentageLoaded = 0
        self.threadList = []

    # Uses multithreading to read a number of request and retrieve results from the API
    # 1st param: the list of requests
    # 2nd param: the total number of requests
    # 3rd param: the number of requests that each thread has to process
    # return: none
    # Fills the 'requestList' attribute with the response
    def parallelRequest(self, requests, requestPerThread = PROT_REQUESTS_PER_THREAD):
        
        # Compute the number of threads 
        if len(requests) % requestPerThread == 0:
            numberOfThreads = len(requests) // requestPerThread
        else: 
            numberOfThreads = len(requests) // requestPerThread + 1

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
                request = ReadObject()
                
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