import io
import json
import requests
import tabulate
import threading
import getpass
import time
from IPython.core.display import display, HTML
import ipywidgets as widgets
import pandas as pd
from pandas.io.json import json_normalize


PROT_TEXTAREA_LAYOUT = widgets.Layout(flex='0 1 auto', 
                                      height='120px', 
                                      min_height='40px', 
                                      width='500px')

def auth():

    return (input("Username: "),getpass.getpass("Password: "))

def get_input(text):

    return input(text)

def get_input_testing(text):

    return input(text)

class read:

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
            self.session.auth = (get_input("Username: "),
                                 getpass.getpass("Password: "))

        self.json = None
        self.data = object()

        self.searchChoices = [
        "assays",
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
        self.searchResultsPerThread = 5
        self.relationshipsPerThread = 5

        self.time = {'start': 0, 'end': 0}

    def on_value_change(self, change):
        
        self.isNotChanged = False

    def get_search_choice(self):

        self.searchType = widgets.Dropdown(options=["assays",
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
                                                    "all"],
                                                value="all", disabled=False)


        return widgets.HBox([widgets.Label(value="Please enter one of: "), 
                self.searchType])

    

    def loadJSON(self, layerName, layer):

        try:
            layerName = lambda: None
            
            if hasattr(layer, 'items'):

                for key, value in layer.items():
                    
                    if hasattr(value, 'items'):

                        setattr(layerName, key, self.loadJSON(key, value))
                    else:

                        setattr(layerName, key, value)

                setattr(self,'data', layerName)
            else:

                for item in range(0, len(layer)):

                    for key, value in layer[item].items():

                        if hasattr(value, 'items'):

                            setattr(layerName, key, self.loadJSON(key, value))
                        else:

                            setattr(layerName, key, value)

            return layerName
        except Exception as e:

            print(str(e))
    
    def request(self, type, id):

        r = None

        try:
            r = self.session.get(self.base_url + type + "/" + id)
            
            self.session.close()
            r.close()
            if r.status_code != 200:
                return False

            self.json = r.json()
            self.loadJSON(self, self.json['data'])
            self.requestList = []
            
            return True

        except Exception as e:
            print(str(e))

    def printAttributes(self):

        print(self.data.attributes.title + "(id: " + self.data.id + 
             " | type: " + self.data.type +")\n")

        print("Description: ", end="")
        if hasattr(self.data.attributes, 'description') and self.data.attributes.description != None:

            print(self.data.attributes.description)
        else:

            print("missing")


    def printRelationshipsSearch(self):

        hasNoRelationships = True

        displayHTML = []
        index = 0

        for relation in dir(self.data.relationships):
            
            if relation[:2] != "__":

                r = getattr(self.data.relationships, relation)
            
                if r.data != [] and hasattr(r, 'newData'):
                        
                    displayHTML.append([])

                    displayHTML[index].append(relation.upper())

                    for d in r.newData:
                        hasNoRelationships = False
                        displayHTML[index].append(d.data.attributes.title)
                    
                    index = index + 1

        display(HTML(tabulate.tabulate(displayHTML, tablefmt='html')))
        if hasNoRelationships:
            print("Object has no relationships")

    def printRelationshipsBrowse(self):

        hasNoRelationships = True

        displayHTML = []
        index = 0

        for relation in dir(self.data.relationships):
            
            if relation[:2] != "__":

                r = getattr(self.data.relationships, relation)
            
                if r.data != [] and hasattr(r, 'newData'):
                        
                    displayHTML.append([])

                    displayHTML[index].append(relation.upper())

                    for data in r.newData:
                        hasNoRelationships = False
                        displayHTML[index].append(data.data.attributes.title)

                    index = index + 1

        display(HTML(tabulate.tabulate(displayHTML, tablefmt='html')))


        if hasNoRelationships:
            print("Object has no relationships")
    
    def printSearch(self):

        if hasattr(self, 'data'):

            if hasattr(self.data, 'attributes'):

                self.printAttributes()
                print("\n")

            if hasattr(self.data, 'relationships'):

                self.printRelationshipsSearch()
        else:

            print("Search item unavailable. Try again later.")

    
    def printBrowse(self):

        if hasattr(self, 'data'):

            if hasattr(self.data, 'attributes'):

                self.printAttributes()
                print("\n")

            if hasattr(self.data, 'relationships'):

                self.printRelationshipsBrowse()
        else:

            print("Search item unavailable. Try again later.")

    # Set up the multithreading amount
    def searchAdvancedSetup(self):

        display(HTML('<h3>Search multithreading</h3>'))
        print("Decide how fast will the search run\n")
        print("Search results are usually less and the search requires less to be requested at once.")
        print("Relationships are usually a lot more, therefore it requires more requests at once")
        
        try:

            self.searchResultsPerThread = int(get_input(
                "How many search results should be requested per thread: "))
            self.relationshipsPerThread = int(get_input_testing(
                "How many relationships should be requested per thread: "))
        except Exception as e:

            print(str(e))
    
    # Used for Demo Presentation
    # Searches without sofisticated interpretaion
    # Process the request and retrieve the JSON
    def APISearch(self):

        # Begin the search by inputing the search term
        self.searchTerm = get_input("Enter your search: \n")
        
        # Choose the category of search
        choice = None
        # while choice not in self.searchChoices:
        choice = get_input_testing("Please enter one of: " + 
                                        ', '.join(self.searchChoices) + ": ")
        
        if choice not in self.searchChoices:
            print("\nNot a choice! Try again!" + choice)
            return False
        
        # widget = self.get_search_choice()
        # display(widget)
        
        # self.isNotChanged = True
 
        # while self.isNotChanged:
        #     widget.observe(self.on_value_change, names=["values"])
        

        # Process the request and retrieve the JSON
        payload = {'q': self.searchTerm, 'search_type': choice}
        r = self.session.get(self.base_url + 'search', headers=self.headers, params=payload)

        if r.status_code != 200:
            return False

        self.json = r.json()

        return True

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

    # Each thread executes this method
    # Loops through each batch of requests received and executes them in turn, serialized
    # 1st param: the request batch
    # 2nd param: the total number of requests
    def makeRequests(self, requestsList, total):

        try:

            for r in requestsList:

                # Create new request
                request = read(self.session.auth)
                
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

    # Uses multithreading to read a number of request and retrieve results from the API
    # 1st param: the list of requests
    # 2nd param: the total number of requests
    # 3rd param: the number of requests that each thread has to process
    # return: none
    # Fills the 'requestList' attribute with the response
    def parallelRequest(self, requests, requestPerThread):
        
        self.requestList = []
        # Compute the number of threads 
        numberOfThreads = 1
        try:
            if len(requests) % requestPerThread == 0:
                numberOfThreads = len(requests) // requestPerThread
            else: 
                numberOfThreads = len(requests) // requestPerThread + 1

            if requestPerThread > 10:
                print("(" + str(numberOfThreads * 5) + ' s estimated)')
            else:
                print("(" + str(numberOfThreads) + ' s estimated)')
        except Exception as e:

            print(str(e))

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

    def getRelationshipsFrom(self, request):

        relations = []

        if hasattr(request.data, 'relationships'):

                for relationship in dir(request.data.relationships):
                
                    if relationship[:2] != '__':
                        relation = getattr(request.data.relationships, relationship)

                        if type(relation.data) == type([{'id':'x','type':'y'}]) and relation.data != []:
                            for r in relation.data:
                                relations.append(r)

                        elif relation.data != []:
                            relations.append({'id':relation.data.id,'type':relation.data.type})
        
        return relations
    # Create the relationship list by parsing the search result list
    # return: number of relations found
    def createRelationshipList(self):

        relations = []

        for request in self.requestList:
            
            relations.extend(self.getRelationshipsFrom(request))
            

        self.relationshipList = relations

        return len(relations)

    def removeDuplicateRelationships(self):
        
        noDuplicates = []
        for relation in self.relationshipList:
            
            if relation not in noDuplicates:
                
                noDuplicates.append(relation)

        self.relationshipList = noDuplicates

    def substituteRelationships(self, relationshipsList, total):

        self.percentageLoaded = 0
        if hasattr(self.data, 'relationships'):
            for r in range(0, len(dir(self.data.relationships))):
                
                if dir(self.data.relationships)[r][:2] != '__':
                    relation = getattr(self.data.relationships, dir(self.data.relationships)[r]) 
                    
                    
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
                                if item.data.id == ID and item.data.type == TYPE:

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

                                else:
                                    # print('ba')
                                    relation.newData = []
                                    relation.newData.append(item)

                                # Don't look anymore
                                break

    def search(self, TYPE, ID):

        r = read(self.session.auth)
        r.request(type=TYPE, id=ID)

        relations = r.getRelationshipsFrom(r)

        ps = read(self.session.auth)
        ps.parallelRequest(relations, 1)

        for thread in ps.threadList:
            thread.join()
        
        r.substituteRelationships(ps.requestList, len(ps.requestList))
        # print(str(ps.requestList))
        self.data = r.data

    # Substitute the information from the relationship list back to the original search results
    # 1st param: the relationship list (without duplicates)
    # 2nd param: the total number of relations in the search results that need to be filled out
    # return: none
    # Adds a 'newData' attribute in each search result relation
    def substituteRelationshipsForSearchResults(self, relationshipsList, total):
        
        print("\nSubstituting relationships into original search results: ")
        self.percentageLoaded = 0

        for i in self.requestList:

            i.substituteRelationships(relationshipsList, total)
            

    # Simplified method for the user in order to operate a browsing in the SEEK API
    def browse(self):

        self.APISearch()

        # Create the request list of the form [{'id':'x', 'type':'y'}]
        self.createRequestList()

        print("\n" + str(len(self.requestList)) + " results found",end='')

        # Create a paralelized request for each search result
        # 1st param: the search results to be requested
        # 2nd param: the total amount of request 
        # 3rd param: the number of request per thread for the paralelization
        self.time['start'] = time.time()
        
        ps = read(self.session.auth)
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

        PS = read(self.session.auth)
        PS.parallelRequest(ps.relationshipList, requestPerThread=self.relationshipsPerThread)

        # Wait for the requests to finish in order to continue
        for thread in PS.threadList:
            thread.join()
        
        self.time['end'] = time.time()

        print("\n" + str(PS.requestFails) + " ommited results (" + str(int(self.time['end'] - self.time['start'])) + " s elapsed)")

        ps.substituteRelationshipsForSearchResults(PS.requestList, totalNumberRelationships)

        self.requestList = ps.requestList
        print("\n\n                                        --SEARCH RESULTS--\n\n")
        for request in ps.requestList:

            request.printBrowse()
            print('\n____________________________________________________________________________\n')

    def find(self, string):

        results = []

        for request in self.requestList:
            if string in request.data.attributes.title:
                results.append(request)
        
        return results

    def download(self):

        if hasattr(self.data.attributes, 'content_blobs') == False:
            return "This method can be called from data files only"

        self.link = self.data.attributes.content_blobs[0]['link'] + "/download"
        self.fileName = self.data.attributes.content_blobs[0]['original_filename']

        r = None

        try:
            r = self.session.get(self.link)
            r.raise_for_status()
            # self.session.close()
            if r.status_code != 200:
                return False

            self.file = r
            # self.json = r.json()
            # self.loadJSON(self, self.json['data'])
            open(self.fileName, 'wb').write(r.content)

            return True

        except Exception as e:
            print(str(e))
    
    def view(self, columnForHeader, page):

        csv = pd.read_excel(self.fileName, header=header, sheet_name=page)
        return csv

class write:

    def __init__(self, auth = None):

        self.base_url = 'https://testing.sysmo-db.org'
            
        self.headers = {"Content-type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Connection": "close",
            "Accept-Charset": "ISO-8859-1"}

        self.type = None
        self.JSON = None
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        if auth != None:
            self.session.auth = auth
        else:
            self.session.auth = (get_input("Username: "),
                                 getpass.getpass("Password: "))

        self.dropdown = None
        self.data = object()

    


    def selectResearchType(self):

        display(HTML('<h3>SEEK FORM</h3>'))
        print('\nYou need to complete the following form in order to succesfully upload your information to SEEK')

        self.type = widgets.Dropdown(
            options=[
                "assays",
                "data_files",
                "studies",
                "investigations",
                "models",
                "sops",
                "publications"
            ],
            value='assays',
            disabled=False,
        )

        return widgets.HBox([widgets.Label(
                            value="What is it that you want to post?"), 
                            self.type])

    def fillSEEKForm(self):

        
        if self.type.value == 'assays':
            self.JSON = assayFormat(self.assayKind.value,
                                           self.description.value,
                                           self.policyAccess.value)

        elif self.type.value == 'investigations':
            self.JSON = investigationFormat()
        elif self.type.value == 'studies':
            self.JSON = studyFormat(self.description.value, 
                                           self.policyAccess.value)
        elif self.type.value == 'data_files':
            self.JSON = data_fileFormat(self.description.value,
                                               self.policyAccess.value)

        print(self.JSON)

    def fillDescription(self):

        self.description = widgets.Textarea(disabled=False,
                                            layout=PROT_TEXTAREA_LAYOUT)
        

        return widgets.HBox([widgets.Label(
                            value="Please provide your description:"), 
                            self.description])

    def selectAssayKind(self):

        self.assayKind = widgets.Dropdown(
            options=[
                "EXP",
                "MOD"
            ],
            value='EXP',
            disabled=False,
        )
        

        return widgets.HBox([widgets.Label(
                value="Please select the class of Assay you wish to create:"), 
                self.assayKind])

    def selectPolicyAccess(self):

        self.policyAccess = widgets.Dropdown(
            options=[
                "no_access",
                "view",
                "download",
                "edit",
                "manage"
            ],
            value='no_access',
            disabled=False,
        )
        

        return widgets.HBox([widgets.Label(
                value="Please select the policy access:"), 
                self.policyAccess])
    
    def post(self):
        r = None

        try:
            r = self.session.post(self.base_url + '/' + self.type.value, json=self.JSON)
            
            self.session.close()
            r.close()
            if r.status_code != 200:
                return False

            self.json = r.json()
            # self.loadJSON(self, self.json['data'])
            
            return True

        except Exception as e:
            print(str(e))


def relationsFormat(JSON, type, source):
    numberOfRelations = int(input("Please specify how many " + type + " is this " + source + " related to: "))

    if numberOfRelations != 0:
        JSON["data"]["relationships"][type] = {}
        JSON["data"]["relationships"][type]["data"] = []
        
        for index in range(1, numberOfRelations + 1):
            
            id = int(input("Please specify the id of the " + type[:-1] + " number " + str(index) + ": "))
            JSON["data"]["relationships"][type]["data"].append({"id" : id, "type" : type})


def relationFormat(JSON, type):

    JSON["data"]["relationships"][type] = {}
    id = input("Please specify the id of the " + type + ": ")
    if id != '':
        JSON["data"]["relationships"][type]["data"] = {"id" : int(id), "type" : type}


def assayFormat(assayKind, description, policy):

    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'assays'
    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['title'] = input('Enter the title: ')
    JSON['data']['attributes']['description'] = description
    JSON['data']['attributes']['policy'] = {'access':policy, 'permissions': []}

    other = ""
    other = input("Please list other creators: ")
    if other != "":
        JSON["data"]["attributes"]["other_creators"] = other

    JSON["data"]["attributes"]["assay_class"] = {}
    JSON["data"]["attributes"]["assay_class"]["key"] = assayKind

    

    assayTypeUri = ""
    assayTypeUri = input("Please specify the assay type uri: ")
    if assayTypeUri != "":
        JSON["data"]["attributes"]["assay_type"] = {}
        JSON["data"]["attributes"]["assay_type"]["uri"] = assayTypeUri

    

    techTypeUri = ""
    techTypeUri = input("Please specify the technology type uri: ")
    if techTypeUri != "":
        JSON["data"]["attributes"]["technology_type"] = {}
        JSON["data"]["attributes"]["technology_type"]["uri"] = techTypeUri

    JSON["data"]["relationships"] = {}

    
    relationsFormat(JSON, "data_files", "assay")
    relationsFormat(JSON, "documents", "assay")

    invID = ""
    invID = input("Please specify the id of the investigation: ")
    if invID != "":
        JSON["data"]["relationships"]["investigation"] = {}
        JSON["data"]["relationships"]["investigation"]["data"] = {"id": invID, "type":"investigations"}

    relationsFormat(JSON, "models", "assay")
    relationsFormat(JSON, "people", "assay")
    relationsFormat(JSON, "publications", "assay")
    relationsFormat(JSON, "sops", "assay")

    studyID = ""
    studyID = input("Please specify the id of the study: ")
    if studyID != "":
        JSON["data"]["relationships"]["study"] = {}
        JSON["data"]["relationships"]["study"]["data"] = {"id": studyID, "type":"studies"}

    relationsFormat(JSON, "organisms", "assay")

    return JSON

def studyFormat(description, policy):

    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'studies'
    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['title'] = input('Enter the title: ')
    JSON['data']['attributes']['description'] = description
    JSON['data']['attributes']['policy'] = {'access': policy, 'permissions': [{'resource': {'id': int(input("What is your user ID? ")),'type': 'people'},'access': 'manage'}]}
    JSON['data']['relationships'] = {}
    JSON['data']['relationships']['investigation'] = {}
    JSON['data']['relationships']['investigation']['data'] = {'id' : int(input("Please enter the investigation id: ")), 'type' : 'investigations'}

    other = ""
    other = input("Please list other creators: ")
    if other != "":
        JSON["data"]["attributes"]["other_creators"] = other

    JSON['data']['attributes']['experimentalists'] = input('Please specify the experimentalists: ')
    JSON['data']['attributes']['person_responsible_id'] = input('Please specify the id of the person responsible: ')

    relationsFormat(JSON, 'assays', 'study')
    relationsFormat(JSON, 'creators', 'study')
    relationsFormat(JSON, 'data_files', 'study')
    relationsFormat(JSON, 'documents', 'study')
    relationsFormat(JSON, 'models', 'study')
    relationsFormat(JSON, 'people', 'study')
    relationsFormat(JSON, 'projects', 'study')
    relationsFormat(JSON, 'publications', 'study')
    relationsFormat(JSON, 'sops', 'study')

    return JSON

def investigationFormat():

    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'investigations'
    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['title'] = input('Please enter the title: ')
    JSON['data']['attributes']['description'] = input('Please enter the description: ')
    JSON['data']['relationships'] = {}

    relationsFormat(JSON, 'assays', 'investigation')
    relationsFormat(JSON, 'creators', 'investigation')
    relationsFormat(JSON, 'data_files', 'investigation')
    relationsFormat(JSON, 'documents', 'investigation')
    relationsFormat(JSON, 'models', 'investigation')
    relationsFormat(JSON, 'people', 'investigation')
    relationsFormat(JSON, 'projects', 'investigation')
    relationsFormat(JSON, 'publications', 'investigation')
    relationsFormat(JSON, 'sops', 'investigation')
    relationsFormat(JSON, 'studies', 'investigation')
    relationsFormat(JSON, 'submitters', 'investigation')

    return JSON
    
def data_fileFormat( description, policy):
    
    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'data_files'
    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['title'] = input('Enter the title: ')

    numberOfRelations = int(input("Please specify the number of tags: "))

    if numberOfRelations != 0:
        JSON["data"]["attributes"]["tags"] = []
        
        for index in range(1, numberOfRelations + 1):
            
            tag = input("Tag #" + str(index) + ": ")
            JSON["data"]["attributes"]["tags"].append(tag)

    JSON['data']['attributes']['license'] = 'CC-BY-4.0'
    JSON['data']['attributes']['description'] = description
    JSON['data']['attributes']['policy'] = {'access': policy}

    remote_blob = {'url' : input('Provide the url/ null if uploading local file'), 'original_filename': input('File name: ')}
    JSON['data']['attributes']['content_blobs'] = [remote_blob]


    JSON['data']['relationships'] = {}
    relationsFormat(JSON, 'projects', 'data file')
    relationsFormat(JSON, 'creators', 'data file')
    relationsFormat(JSON, 'assays', 'data file')
    relationsFormat(JSON, 'publications', 'data file')
    relationsFormat(JSON, 'events', 'data file')
    
    return JSON