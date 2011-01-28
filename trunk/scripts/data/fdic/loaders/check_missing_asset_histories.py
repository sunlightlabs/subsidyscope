import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import *

for institution in Institution.objects.all():
    
    if institution.institutionassethistory_set.all().count() == 0 and institution.transaction_set.all().count() > 0:
        
        if institution.fdic_number:
            print 'FDIC %d: %s' % (institution.fdic_number, institution.name)
        elif institution.ots_number:
            print 'OTS %s: %s' % (institution.ots_number, institution.name)
        elif institution.fed_number:
            print 'FED %d: %s' % (institution.fed_number, institution.name)
        else:
            print '%d: %s' % (institution.id, institution.name)