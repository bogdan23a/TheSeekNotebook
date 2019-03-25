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

def studyFormat():

    # investigation_id = 41
    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'studies'
    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['title'] = input('Enter the title: ')
    JSON['data']['attributes']['description'] = input('Description: ')
    JSON['data']['attributes']['policy'] = {'access':'view', 'permissions': [{'resource': {'id': int(input("What is your user ID? ")),'type': 'people'},'access': 'manage'}]}
    JSON['data']['relationships'] = {}
    JSON['data']['relationships']['investigation'] = {}
    JSON['data']['relationships']['investigation']['data'] = {'id' : int(input("Please enter the investigation id: ")), 'type' : 'investigations'}

    # JSON['data']['attributes']['description'] = input('Please specify the description: ')
    # JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    # JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    # JSON['data']['attributes']['title'] = input('Please specify the title: ')

    # JSON['data']['attributes']['experimentalists'] = input('Please specify the experimentalists: ')
    # JSON['data']['attributes']['person_responsible_id'] = input('Please specify the id of the person responsible: ')

    # JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    # JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    # JSON['data']['attributes']['title'] = input('Please specify the title: ')

    # JSON['data']['relationships'] = {}

    
    # relationsFormat(JSON, 'assays', 'study')
    # relationsFormat(JSON, 'creators', 'study')
    # relationsFormat(JSON, 'data_files', 'study')
    # relationsFormat(JSON, 'documents', 'study')
    # relationsFormat(JSON, 'models', 'study')
    # relationsFormat(JSON, 'people', 'study')
    # relationsFormat(JSON, 'projects', 'study')
    # relationsFormat(JSON, 'publications', 'study')
    # relationsFormat(JSON, 'sops', 'study')
    # relationsFormat(JSON, 'submitters', 'study')

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
