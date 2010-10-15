import os, re, sys

sys.path.append('/home/Kevin Webb/docs/sunlight_workspace/subsidyscope_main/bailout.site/trunk')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from cfda.models import ProgramDescription
from sectors.models import Sector  

sector = Sector.objects.get(pk=5)
sector.programdescription_set.all().delete()

cfda_numbers = []

cfda_file = open('housing_cfda.txt')

for line in cfda_file.readlines():
    cfda_numbers.append(line.strip())

cfda_numbers = list(set(cfda_numbers))

for cfda_number in cfda_numbers:
    
    try:
        program = ProgramDescription.objects.get(program_number=cfda_number)
        program.sectors.add(sector)
        
        print '%s: %s' % (program.program_number, program.program_title)
                
    except:
        print '*Unable to locate CFDA %s' % cfda_number
        
print 'Done.'
    