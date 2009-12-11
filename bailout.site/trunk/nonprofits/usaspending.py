from faads.models import RecipientType

def faads():
    """ defines SQL clause identifying relevant FAADS program records """
    
    recipient_type_codes = []
    for keyword in ('nonprofit', 'education'):
        try:
            recipient_type_codes.append(RecipientType.objects.filter(name__icontains=keyword)[0].code)
        except:
            pass
            
    return "CONVERT(recipient_type, SIGNED) IN (%s)" % ','.join(map(lambda x: str(x), recipient_type_codes))
    
    
def fpds(self):
    """ defines SQL clause identifying relevant FPDS program records """
    pass