import json
import requests
import Helper
from IPython.core.display import display, HTML

class WriteObject():

    def __init__(self):

        self.base_url = 'https://testing.sysmo-db.org'
            
        self.headers = {"Content-type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Connection": "close",
            "Accept-Charset": "ISO-8859-1"}

        self.type = None

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = ("bogdan23a","dominimus123")
       
        self.data = object()

    def SEEKForm(self):

        display(HTML('<h3>SEEK FORM</h3>'))
        self.type = input('\nThe type of object you want to upload to SEEK: ')
        print('\nYou need to complete the following form in order to succesfully upload your information to SEEK')
        
        if self.type == 'assays':
            self.JSON = Helper.assayFormat()
        elif self.type == 'investigations':
            self.JSON = Helper.investigationFormat()
        elif self.type == 'studies':
            self.JSON = Helper.studyFormat()

        print(self.JSON)

    def request(self):
        r = self.session.post(self.base_url + '/' + self.type, json=self.JSON)
        r.raise_for_status()