import json
import requests

class ReadObject():

    def __init__(self):

        self.base_url = 'http://www.fairdomhub.org/'
            
        self.headers = {"Content-type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Connection": "close",
            "Accept-Charset": "ISO-8859-1"}

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = ("asda","asda")
        self.json = None
        self.data = object()

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
                # if len(r.newData) != 0:
                
                if r.data != [] and hasattr(r, 'newData'):
                    
                    
                    print(relation.upper())
                    for data in r.newData:
                        hasNoRelationships = False
                        print(data.data.attributes.title)
        
        if hasNoRelationships:
            print("Object has no relationships")