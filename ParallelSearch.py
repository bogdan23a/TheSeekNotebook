import threading
from ReadObject import ReadObject

PROT_REQUESTS_PER_THREAD = 50

class ParallelSearch():

    def __init__(self):
        # super().__init__(self)

        # logging.basicConfig(level=logging.DEBUG,
                            # format='(%(threadName)-10s) %(message)s',)
        self.requestList = [] # better name is resultList = []
        self.relationshipList = []
        self.requestFails = 0
        self.percentageLoaded = 0

    def parallelRequest(self, requests, total, requestPerThread = PROT_REQUESTS_PER_THREAD):
        
        """ 
        The requests argument contains an array of {id,type} form 
        """

        # print("Loading results. Please wait.",end='')
        threadList = []

        if len(requests) % requestPerThread == 0:
            numberOfThreads = len(requests) // requestPerThread
        else: 
            numberOfThreads = len(requests) // requestPerThread + 1

        for currentThread in range(0, numberOfThreads):

            """ 
            Make a new thread as needed and give as args requestPerThread requests per thread
            or if the number of request does not split equally assign the last thread
            less
            """
            
            if currentThread == (numberOfThreads - 1):
                rightArrayBound = len(requests)
            else:
                rightArrayBound = (currentThread + 1) * requestPerThread

            newThread = threading.Thread(name="Thread " + str(currentThread), target=self.makeRequests, args=(requests[currentThread * requestPerThread : rightArrayBound], total,))
            newThread.start()
            threadList.append(newThread)
            # newThread.join()


    def makeRequests(self, requestsList, total):
        

        for r in requestsList:

            try:

                request = ReadObject()
                
                if request.request(type=r['type'], id=r['id']) == False:
                    self.requestFails = self.requestFails + 1
                else:
                    # logging.debug("requesting " + r['id'])
                    p = self.percentageLoaded / total * 100
                    if p >= (100 - (1 / total) * 100):
                        print("Loading " + str(round(p,2)) + "%\r", end='')
                        print("\nLoading Completed")
                    else:
                        print("Loading " + str(round(p,2)) + "%\r", end='')
                    self.requestList.append(request)

                self.percentageLoaded = self.percentageLoaded + 1
            except Exception as e:

                print(str(e))
            

    def getRelationships(self, rawRelationships):

        relationships = []
        for item in rawRelationships:

            for relation, data in item.items():
            
                for name,IDType in data.items():

                    for d in IDType:
                        
                        retainID = ""
                        retainType = ""
            
                        for ID,Type in d.items():
                    
                            if ID == 'id':
                                retainID = Type
                            else:
                                retainType = Type
                        
                        relationships.append({'id': retainID, 'type':retainType})
                
        return relationships

    # create the list of requests from a search result list
    def createRelationshipList(self):

        # form the relationships request list
        # ommited 'investigation' object!!!
        relations = []
        for request in self.requestList:
            
            if hasattr(request.data, 'relationships'):
                for relationship in dir(request.data.relationships):
                
                    if relationship[:2] != '__': # and relationship != 'investigation':# and  relationship != 'investigations':
                    
                        relation = getattr(request.data.relationships, relationship)
                        if type(relation.data) == type([{'id':'x','type':'y'}]) and relation.data != []:
                            for r in relation.data:
                                relations.append(r)
                        elif relation.data != []:
                            # print(relation.data.id)
                            relations.append({'id':relation.data.id,'type':relation.data.type})
        self.relationshipList = relations

    
    def substituteRelationships(self, relationshipsList):
        
        print("Substituting relationships into original search results: ")
        for i in self.requestList:

            if hasattr(i.data, 'relationships'):
                for r in range(0, len(dir(i.data.relationships))):
                    
                    if dir(i.data.relationships)[r][:2] != '__':
                        # print("relation : " + dir(i.data.relationships)[r] + "\n")
                        relation = getattr(i.data.relationships, dir(i.data.relationships)[r]) 

                        if type(relation.data) == type([{'id':'x','type':'y'}]) and relation.data != []:

                            
                            for k in relation.data:
                                
            #                     print(k)
                                ID = 0
                                TYPE = ''
                                for key, value in k.items():
                                    if key == 'id':
                                        ID = value
                                    if key == 'type':
                                        TYPE = value
                                # print()
                                for item in relationshipsList:

                                    if type(item.data) != type(object()) and item.data.id == ID and item.data.type == TYPE:
                                        print(".", end='')
                                        if hasattr(relation, 'newData'):
                                            relation.newData.append(item)
                                            break
                                        else:
                                            relation.newData = []
                                            relation.newData.append(item)
                                            break

                        elif relation.data != []:
                                
                            for item in relationshipsList:
                                                    
                                if type(item.data) != type(object()) and item.data.id == relation.data.id and item.data.type == relation.data.type:
                                    print(".", end='')
                                    if hasattr(relation, 'newData'):
                                        relation.newData.append(item)
                                        break
                                    else:
                                        
                                        relation.newData = []
                                        relation.newData.append(item)
                                        break

    def removeDuplicateRelationships(self):
        
        noDuplicates = []
        for relation in self.relationshipList:
            
            if relation not in noDuplicates:
                
                noDuplicates.append(relation)

        self.relationshipList = noDuplicates