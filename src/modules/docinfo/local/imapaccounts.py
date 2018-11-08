



def EnumObjects(SnapshotDef, ParentObject, ClassName):


    def __generator_imapaccounts():

        if ParentObject != None:
            for _item in [
                { 'ID': 1,
                    'Description': 'amj@tyst.dk',
                    'Hostname':    'mail.tyst.dk',
                    'Protocol':    'tls',
                    'Username':    'amj',
                    'Password':    '1234',
                },
                { 'ID': 2,
                    'Description': 'mbv@kangodt.dk',
                    'Hostname':    'mail.tyst.dk',
                    'Protocol':    'tls',
                    'Username':    'mbv',
                    'Password':    '1234',
                },
            ]: yield _item

        else:
            return None

    #END def __generator_imapaccounts



    def __generator_namespaces():

        if ParentObject == '1':
            for _item in [
                {'Type': 'P', 'Name': 'INBOX',
                    'ScanMailboxes': True,
                }, 
            ]: yield _item

        elif ParentObject == '2':
            for _item in [
                {'Type': 'P', 'Name': 'INBOX',
                    'ScanMailboxes': True,
                },
            ]: yield _item

        else:
            return None

    #END def __generator_namespaces



    





    if ClassName=='imapaccount':
        return __generator_imapaccounts

    return None 


#END def EnumObjects
            

