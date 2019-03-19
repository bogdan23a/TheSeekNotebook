import ipywidgets as widgets


def relationsFormat(JSON, type, source):
    numberOfRelations = int(input("Please specify how many " + type + " is this " + source + " related to: "))

    if numberOfRelations != 0:
        JSON["data"]["relationships"][type] = {}
        JSON["data"]["relationships"][type]["data"] = [{}]
        
        for index in range(1, numberOfRelations + 1):
            
            id = int(input("Please specify the id of the " + type[:-1] + " number " + str(index) + ": "))
            JSON["data"]["relationships"][type]["data"].pop(0)
            JSON["data"]["relationships"][type]["data"].append({"id" : id, "type" : type})


def relationFormat(JSON, type):

    JSON["data"]["relationships"][type] = {}
    id = input("Please specify the id of the " + type[:-1] + ": ")
    if id != '':
        JSON["data"]["relationships"][type]["data"] = {"id" : int(id), "type" : type}


def assayFormat(assayKind):

    JSON = {}
    JSON["data"] = {}
    JSON["data"]["type"] = "assays"

    JSON["data"]["attributes"] = {}
    # JSON["data"]["attributes"]["description"] = description
    # JSON["data"]["attributes"]["other_creators"] = input("Please list other creators: ")
    # JSON["data"]["attributes"]["policy"] = {}
    # JSON["data"]["attributes"]["policy"]["access"] = policy
    # JSON["data"]["attributes"]["policy"]["permissions"] = []
    JSON["data"]["attributes"]["title"] = input("Please specify the title: ")

    JSON["data"]["attributes"]["assay_class"] = {}
    JSON["data"]["attributes"]["assay_class"]["key"] = assayKind

    JSON["data"]["attributes"]["assay_type"] = {}
    JSON["data"]["attributes"]["assay_type"]["uri"] = input("Please specify the assay type uri: ")

    JSON["data"]["attributes"]["technology_type"] = {}
    JSON["data"]["attributes"]["technology_type"]["uri"] = input("Please specify the technology type uri: ")

    JSON["data"]["relationships"] = {}

    
    # relationsFormat(JSON, "data_files", "assay")
    # relationsFormat(JSON, "documents", "assay")
    # JSON["data"]["relationships"]["investigation"] = {}
    # JSON["data"]["relationships"]["investigation"]["data"] = {"id": input("Please specify the id of the investigation: "), "type":"investigations"}
    # relationsFormat(JSON, "models", "assay")
    # relationsFormat(JSON, "people", "assay")
    # relationsFormat(JSON, "publications", "assay")
    # relationsFormat(JSON, "sops", "assay")
    JSON["data"]["relationships"]["study"] = {}
    JSON["data"]["relationships"]["study"]["data"] = {"id": input("Please specify the id of the study: "), "type":"studies"}
    # relationsFormat(JSON, "organisms", "assay")

    return JSON

def studyFormat():

    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'assays'

    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['description'] = input('Please specify the description: ')
    JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    JSON['data']['attributes']['title'] = input('Please specify the title: ')

    JSON['data']['attributes']['experimentalists'] = input('Please specify the experimentalists: ')
    JSON['data']['attributes']['person_responsible_id'] = input('Please specify the id of the person responsible: ')

    JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    JSON['data']['attributes']['title'] = input('Please specify the title: ')

    JSON['data']['relationships'] = {}

    
    relationsFormat(JSON, 'assays', 'study')
    relationsFormat(JSON, 'creators', 'study')
    relationsFormat(JSON, 'data_files', 'study')
    relationsFormat(JSON, 'documents', 'study')
    relationsFormat(JSON, 'investigations', 'study')
    relationsFormat(JSON, 'models', 'study')
    relationsFormat(JSON, 'people', 'study')
    relationsFormat(JSON, 'projects', 'study')
    relationsFormat(JSON, 'publications', 'study')
    relationsFormat(JSON, 'sops', 'study')
    relationsFormat(JSON, 'submitters', 'study')

    return JSON

def investigationFormat():

    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'investigations'

    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['description'] = input('Please specify the description: ')
    JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    JSON['data']['attributes']['title'] = input('Please specify the title: ')

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
