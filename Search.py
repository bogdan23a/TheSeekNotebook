from IPython.core.display import display, HTML
from ParallelSearch import ParallelSearch
from ReadObject import ReadObject

class Search(ReadObject):

    def __init__(self):
        super().__init__()

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
        self.searchResultsPerThread = 4
        self.relationshipsPerThread = 10 

    # Simplified method for the user in order to operate a browsing in the SEEK API
    def search(self):

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

        # Create the request list of the form [{'id':'x', 'type':'y'}]
        self.createRequestList()

        print("\n" + str(len(self.requestList)) + " results found")

        # Create a paralelized request for each search result
        # 1st param: the search results to be requested
        # 2nd param: the total amount of request 
        # 3rd param: the number of request per thread for the paralelization
        ps = ParallelSearch()
        ps.parallelRequest(self.requestList, requestPerThread=self.searchResultsPerThread)

        # Wait for the requests to finish in order to continue
        for thread in ps.threadList:
            thread.join()

        print("\n" + str(ps.requestFails) + " ommited results")

        # Get the total number of places where there is a relationship
        totalNumberRelationships = ps.createRelationshipList()

        ps.removeDuplicateRelationships()

        print("\n" + str(len(ps.relationshipList)) + " relationships found")       

        # Create a paralelized request for each relationship in the search results 
        PS = ParallelSearch()
        PS.parallelRequest(ps.relationshipList, requestPerThread=self.relationshipsPerThread)

        # Wait for the requests to finish in order to continue
        for thread in PS.threadList:
            thread.join()

        print("\n" + str(PS.requestFails) + " ommited results")

        ps.substituteRelationships(PS.requestList, totalNumberRelationships)

        print("\n\n                                        --SEARCH RESULTS--\n\n")
        for request in ps.requestList:

            request.print()
            print('\n____________________________________________________________________________\n')
    
    # Set up the multithreading amount
    def searchAdvancedSetup(self):

        display(HTML('<h3>Search multithreading</h3>'))
        print("Decide how fast will the search run\n")
        print("Search results are usually less and the search requires less to be requested at once.")
        print("Relationships are usually a lot more, therefore it requires more requests at once")
        self.searchResultsPerThread = int(input("How many search results should be requested per thread: "))
        self.relationshipsPerThread = int(input("How many relationships should be requested per thread: "))

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