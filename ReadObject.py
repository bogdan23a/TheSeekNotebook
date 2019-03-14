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
       
        self.data = object()

    def request(self, type, id):

        r = None

        try:

            r = self.session.get(self.base_url + type + "/" + id)

            if r.status_code != 200:
                print("\nInternal Error(result ommited)\n", end='')
                return False
            
            # r.raise_for_status()
            callback = r.json()
            self.loadJSON(self, callback['data'])
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


    def assayAttributes(self):

        if self.data.type == 'assays':

            if self.data.attributes.title != None:
                print(self.data.attributes.title)

            if self.data.attributes.assay_class != None and self.data.attributes.assay_type != None:
                print(self.data.attributes.assay_class.title + " | " + self.data.attributes.assay_type.label)
    
            if self.data.attributes.description != None:
                print("\n" + self.data.attributes.description)

    def assayRelationships(self):
        
        print("\n\n STUDY:")
        if hasattr(self.data.relationships.study, 'newData'):
            self.data.relationships.study.newData.studyAttributes()
        print("\n\n INVESTIGATION:")
        if hasattr(self.data.relationships.investigation, 'newData'):
           self.data.relationships.investigation.newData.investigationAttributes()
        print("\n\n PROJECTS: ")
        if hasattr(self.data.relationships.projects, 'newData'):
            self.data.relationships.projects.newData.projectsAttributes()
        print("\n\n")
    
    def assaySummary(self):
        self.assayAttributes()
        self.assayRelationships()

    def studyAttributes(self):

        if self.data.type == 'studies':

            print(self.data.attributes.title)
            print("\n" + self.data.attributes.description)
    
    def studyRelationships(self):

        print("\n\n INVESTIGATION:")
        self.data.relationships.investigation.investigationAttributes()
        print("\n\n PROJECTS: ")
        self.data.relationships.projects.projectsAttributes()
        print("\n\n")
    
    def studySummary(self):
        self.studyAttributes()
        self.studyRelationships()

    def investigationAttributes(self):

        if self.data.type == 'investigations':

            print(self.data.attributes.title)
            print("\n" + self.data.attributes.description)
    
    def investigationRelationships(self):

        print("\n\n PROJECTS: ")
        self.data.relationships.projects.projectsAttributes()
        print("\n\n")


    def investigationSummary(self):
        self.investigationAttributes()
        self.investigationRelationships()


    def projectsAttributes(self):

        if self.data.type == 'projects':

            print(self.data.attributes.title)
            print(self.data.attributes.default_license + " | " + self.data.attributes.default_policy.access)
            print("Web Page: " + self.data.attributes.web_page)
            print("\n" + self.data.attributes.description)