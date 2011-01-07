
def splitInt(value):
    
    if not value is None:
        return int(value.split('.')[0])
    else:
        return None

def splitIntCode(value):

    code = splitCode(value)
    
    if not code == '':
        return int(code)
    else:
        return None

def splitCode(value):

    if not value is None:
        return  value.split(':')[0]
    else:
        return ''

def transformFlag(value):
    
    if value ==  '':
        return ''
    
    if value[0] == 'n' or value[0] == 'N' or value[0] == 'f':
        return 'f'
    elif value[0] == 'y' or value[0] == 'Y' or value[0] == 't':
        return 't'
    else:
        return ''