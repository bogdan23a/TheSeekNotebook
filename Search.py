from ReadObject import ReadObject
from ParallelSearch import ParallelSearch

class Search(ReadObject):
    def __init__(self):

        super().__init__()

        self.searchChoices =["assays",
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
        
        # logging.basicConfig(level=logging.DEBUG,
                            # format='(%(threadName)-10s) %(message)s',)
        

        self.requestList = []

    def search(self):

        self.searchTerm = input("Enter your search: \n")

        choice = None
        while choice not in self.searchChoices:
            choice = input("Please enter one of: " + ', '.join(self.searchChoices))
        self.searchType = choice

        payload = {'q': self.searchTerm, 'search_type': self.searchType}

        r = self.session.get(self.base_url + 'search', headers=self.headers, params=payload)

        r.raise_for_status()

        self.json = r.json()

        numberOfResults = self.createRequestList()

        print(numberOfResults)

        ps = ParallelSearch()
        ps.parallelRequest(self.requestList, int(numberOfResults[1:-14]), requestPerThread=5)



    def demoSearch(self):

        self.searchTerm = input("Enter your search: \n")

        choice = None
        while choice not in self.searchChoices:
            choice = input("Please enter one of: " + ', '.join(self.searchChoices))
        self.searchType = choice

        payload = {'q': self.searchTerm, 'search_type': self.searchType}

        r = self.session.get(self.base_url + 'search', headers=self.headers, params=payload)

        r.raise_for_status()

        self.json = r.json()

    def request(self, requestsList):
        
        for r in requestsList:

            try:

                req = ReadObject()
                
                req.request(type=r['type'], id=r['id'])

                # logging.debug("requesting " + r['id'])
                
                self.requestList.append(req)

            except Exception as e:

                print(str(e))

    
    
    # create the list of requests from a search result list
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

        return "\n" + str(len(requestList)) + " results found"

    
        
        