from cfda.models import ProgramDescription

def faads():
    """ defines SQL clause identifying relevant FAADS program records """
    
    cfda_programs = {}
    for p in ProgramDescription.objects.filter(sectors__name__icontains='transportation'):
        cfda_programs[p.program_number] = p
        
    return "TRIM(cfda_program_num) IN ('%s')" %  "','".join(map(lambda x: str(x), cfda_programs.keys()))
    
def fpds(self):
    """ defines SQL clause identifying relevant FPDS program records """
    pass