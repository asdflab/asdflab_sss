


def StateInfo():
    return {
        'Name': 'imapbackup',
        'TopLevel': 'imapaccount',
        'Classes': {

            'imapaccount': {
                'Parallelizable': True,
                'ParentClass': None,
                'ChildClasses': ['namespace'],
            
                'StateinfoFields': [
                ],
                'DocinfoFields': [
                    {'Name': 'ID',           'DataType': ''},
                    {'Name': 'Description',  'DataType': ''},
                    {'Name': 'Hostname',     'DataType': ''},
                    {'Name': 'Protocol',     'DataType': ''},
                    {'Name': 'Username',     'DataType': ''},
                    {'Name': 'Password',     'DataType': ''},
                ],

                'IDFields': [
                    'ID',
                ],
                'MetaFields': [
                    'Description',
                ],
                'BulkStreams': [
                ],
            },

            'namespace': {
                'Parallelizable': False,
                'ParentClass': 'imapaccount',
                'ChildClasses': ['mailbox'],
    
                'StateinfoFields': [
                    {'Name': 'Type',      'DataType': ''},
                    {'Name': 'Name',      'DataType': ''},
                    {'Name': 'Delimiter', 'DataType': ''},
                ],
                'DocinfoFields': [
                    {'Name': 'Type',          'DataType': ''},
                    {'Name': 'Name',          'DataType': ''},
                    {'Name': 'ScanMailboxes', 'DataType': ''},
                ],

                'IDFields': [
                    'Type',
                    'Name',
                ],
                'MetaFields': [
                    'Delimiter',
                ],
                'BulkStreams': [
                ],
            },

            'mailbox': {
                'Parallelizable': False,
                'ParentClass': 'namespace',
                'ChildClasses': ['message'],

                'StateinfoFields': [
                    {'Name': 'UIDValidity', 'DataType': ''},
                    {'Name': 'Fullname',    'DataType': ''},
                ],
                'DocinfoFields': [
                    {'Name': 'UIDValidity',  'DataType': ''},
                    {'Name': 'ScanMessages', 'DataType': ''},
                ],

                'IDFields': [
                    'UIDValidity',
                ],
                'MetaFields': [
                    'Fullname',
                ],
                'BulkStreams': [
                ],
            },

            'message': {
                'Parallelizable': False,
                'ParentClass': 'mailbox',
                'ChildClasses': [],

                'StateinfoFields': [
                    {'Name': 'UID',       'DataType': ''},
                    {'Name': 'MessageID', 'DataType': ''},
                    {'Name': 'From',      'DataType': ''},
                    {'Name': 'To',        'DataType': ''},
                    {'Name': 'Datetime',  'DataType': ''},
                    {'Name': 'Subject',   'DataType': ''},
                ],
                'DocinfoFields': [
                    {'Name': 'UID', 'DataType': ''},
                ],

                'IDFields': [
                    'UID',
                ],
                'MetaFields': [
                    'MessageID',
                    'From',
                    'To',
                    'Datetime',
                    'Subject',
                ],
                'BulkStreams': [
                    {'Name': 'Content', 'DataType': ''},
                ],
            },

        ],
    }





def EnumObjects(SnapshotDef, ParentObject, ClassName):

    def __generator_X():
        return None


    if ClassName=='imapaccount':
        return None

    return None

#END def EnumObjects

