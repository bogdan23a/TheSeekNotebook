import ipywidgets as widgets


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
    
def data_fileFormat(description, policy):
    
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
    # JSON['data']['relationships']['projects'] = {}
    # JSON['data']['relationships']['projects']['data'] = [{'id' : containing_project_id, 'type' : 'projects'}]
    relationsFormat(JSON, 'projects', 'data file')
    relationsFormat(JSON, 'creators', 'data file')
    relationsFormat(JSON, 'assays', 'data file')
    relationsFormat(JSON, 'publications', 'data file')
    relationsFormat(JSON, 'events', 'data file')
    
    return JSON