from cfda.models import ProgramDescription
from sectors.models import Sector, Subsector

def faads():
    """ defines SQL clause identifying relevant FAADS program records """
    
    cfda_programs = {}
    for p in ProgramDescription.objects.filter(sectors__name__icontains='transportation'):
        cfda_programs[p.program_number] = p
    
    sector = None
    try:
        sector = Sector.objects.filter(name__icontains='transportation')[0]
    except Exception, e:
        raise e
    
    return { 'sector': { sector: "TRIM(cfda_program_num) IN ('%s')" %  "','".join(map(lambda x: str(x), cfda_programs.keys())) }, 'subsectors': {} }
    
def fpds():
    """ defines SQL clause identifying relevant FPDS program records """
    return None