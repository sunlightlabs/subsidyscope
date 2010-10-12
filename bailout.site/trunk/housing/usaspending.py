from faads.models import RecipientType
from sectors.models import Sector, Subsector
from fpds.models import ProductOrServiceCode, NAICSCode
from faads.models import ProgramDescription

def _get_sector():
    """ returns the energy sector codes """
    sector = None
    try:
        sector = Sector.objects.filter(name__icontains='energy')[0]
    except Exception, e:
        raise e
        
    return sector

def faads():
    """ defines SQL clause identifying relevant FAADS program records """
    sector = _get_sector()    

    cfda_programs = {}
    for p in ProgramDescription.objects.filter(sectors=sector):
        cfda_programs[p.program_number] = p

    sql = "TRIM(cfda_program_num) IN ('%s')" %  ("','".join(map(lambda x: str(x), cfda_programs.keys())))
    return { 'sector': { sector: sql }, 'subsectors': {} }

    
def fpds():
    """ defines SQL clause identifying relevant FPDS program records """

    sector = _get_sector()    

    psc_codes = ProductOrServiceCode.objects.filter(sectors=sector)
    naics_codes = NAICSCode.objects.filter(sectors=sector)
    
    psc_code_string = "'%s'" % "','".join(map(lambda x: str(x.code).upper().strip(), psc_codes)) # chars -- need quotes
    naics_code_string = "%s" % ",".join(map(lambda x: str(x.code), naics_codes)) # ints -- no quotes necessary
    
    sql = "TRIM(UPPER(extentCompeted)) NOT IN ('A', 'F', 'CDO') AND ((TRIM(UPPER(principalNAICSCode)) IN (%s)) OR ((TRIM(principalNAICSCode)='') AND (TRIM(UPPER(productOrServiceCode)) IN (%s))))" % (naics_code_string, psc_code_string)
    print sql
    exit()
    
    return { 'sector': { sector: sql }, 'subsectors': {} }    