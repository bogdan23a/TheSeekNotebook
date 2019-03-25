import ipywidgets as widgets
import json
import requests
import Helper
import getpass
from IPython.core.display import display, HTML

PROT_TEXTAREA_LAYOUT = widgets.Layout(flex='0 1 auto', 
                                      height='120px', 
                                      min_height='40px', 
                                      width='500px')

class WriteObject():

    def __init__(self):

        self.base_url = 'https://testing.sysmo-db.org'
            
        self.headers = {"Content-type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
            "Connection": "close",
            "Accept-Charset": "ISO-8859-1"}

        self.type = None
        self.JSON = None
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = (input("Username: "),getpass.getpass("Password: "))
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
            self.JSON = Helper.assayFormat(self.assayKind.value,
                                           self.description.value)

        elif self.type.value == 'investigations':
            self.JSON = Helper.investigationFormat()
        elif self.type.value == 'studies':
            self.JSON = Helper.studyFormat()

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
    
    def request(self):
        r = self.session.post(self.base_url + '/' + self.type.value, json=self.JSON)
        r.raise_for_status()
        self.json = r.json()
        r.close()
        self.session.close()
