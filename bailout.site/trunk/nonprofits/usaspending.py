from faads.models import RecipientType
from sectors.models import Sector, Subsector

def _get_sector():
    """ returns the nonprofit sector codes """
    sector = None
    try:
        sector = Sector.objects.filter(name__icontains='nonprofit')[0]
    except Exception, e:
        raise e
        
    return sector

def faads():
    """ defines SQL clause identifying relevant FAADS program records """
    
    recipient_type_codes = []
    for keyword in ('nonprofit', 'education'):
        try:
            recipient_type_codes.append(RecipientType.objects.filter(name__icontains=keyword)[0].code)
        except:
            pass
            
    sector = _get_sector()
    
    return { 'sector': { sector: " CONVERT('0'+recipient_type, SIGNED) IN (%s) " % ','.join(map(lambda x: str(x), recipient_type_codes)) }, 'subsectors': {} }
    
    
def fpds():
    """ defines SQL clause identifying relevant FPDS program records """
    sector = _get_sector()
    return { 'sector': { sector: "TRIM(UPPER(extentCompeted)) NOT IN ('A', 'F', 'CDO') AND (LOWER(TRIM(nonprofitOrganizationFlag))='t' OR LOWER(TRIM(educationalInstitutionFlag))='t')"}, 'subsectors': {}}