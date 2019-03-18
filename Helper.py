import ipywidgets as widgets

isClicked = False

def relationsFormat(JSON, type, source):
    numberOfRelations = int(input('Please specify how many ' + type + ' is this ' + source + ' related to: '))

    if numberOfRelations != 0:
        JSON['data']['relationships'][type] = {}
        JSON['data']['relationships'][type]['data'] = [{}]
        
        for index in range(1, numberOfRelations + 1):
            
            id = int(input('Please specify the id of the ' + type[:-1] + ' number ' + str(index) + ': '))
            JSON['data']['relationships'][type]['data'].pop(0)
            JSON['data']['relationships'][type]['data'].append({'id' : id, 'type' : type})


def relationFormat(JSON, type):

    # JSON['data']['relationships'][type] = {}
    id = input('Please specify the id of the ' + type[:-1] + ": ")
    if id != '':
        JSON['data']['relationships'][type]['data'] = {'id' : int(id), 'type' : type}

def buttonClicked():
    isClicked = True

def assayFormat():

    JSON = {}
    JSON['data'] = {}
    JSON['data']['type'] = 'assays'

    JSON['data']['attributes'] = {}
    JSON['data']['attributes']['description'] = input('Please specify the description: ')
    JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    # JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    JSON['data']['attributes']['title'] = input('Please specify the title: ')

    JSON['data']['attributes']['assay_class'] = {}
    JSON['data']['attributes']['assay_class']['description'] = input('Please specify the assay class description: ')
    select = widgets.Select(options=['EXP', 'MODEL'],
                        value='EXP',
                        rows=2,
                        description='Assay Class Key',
                        disabled=False)

    display(select)
    button = widgets.Button(
                        description='Accept',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Select',
                        icon='check'
                )
    display(button)
    while not isClicked:

        button.on_click(buttonClicked)

    JSON['data']['attributes']['assay_class']['key'] = select.value
        # input('Please specify the assay class key(EXP / MODEL): ')
    JSON['data']['attributes']['assay_class']['title'] = input('Please specify the assay class title(Experimental assay / Modelling Analysis): ')

    JSON['data']['attributes']['assay_type'] = {}
    JSON['data']['attributes']['assay_type']['label'] = input('Please specify the assay type label: ')
    JSON['data']['attributes']['assay_type']['uri'] = input('Please specify the assay type uri: ')

    JSON['data']['attributes']['technology_type'] = {}
    JSON['data']['attributes']['technology_type']['label'] = input('Please specify the technology type label: ')
    JSON['data']['attributes']['technology_type']['uri'] = input('Please specify the technology type uri: ')

    # JSON['data']['attributes']['other_creators'] = input('Please specify other creators: ')
    # JSON['data']['attributes']['snapshots'] = input('Please specify the snapshots: ')
    # JSON['data']['attributes']['title'] = input('Please specify the title: ')

    JSON['data']['relationships'] = {}

    
    relationsFormat(JSON, 'creators', 'assay')
    relationsFormat(JSON, 'data_files', 'assay')
    relationsFormat(JSON, 'documents', 'assay')
    relationFormat(JSON, 'investigations')
    relationsFormat(JSON, 'models', 'assay')
    relationsFormat(JSON, 'people', 'assay')
    relationsFormat(JSON, 'projects', 'assay')
    relationsFormat(JSON, 'publications', 'assay')
    relationsFormat(JSON, 'sops', 'assay')
    relationFormat(JSON, 'studies')
    relationsFormat(JSON, 'submitters', 'assay')

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
