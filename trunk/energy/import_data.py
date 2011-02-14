from sectors.models import *
from cfda.models import ProgramDescription
from fpds.models import NAICSCode, ProductOrServiceCode
import csv

def get_energy_sector():
    e = Sector.objects.filter(name__icontains='energy')
    return e[0]

def cfda_import(s):
    f = open('energy_cfda', 'r')
    while True:
        l = f.readline()
        if not l:
            break
        program_number = l.strip()
        
        p_matches = ProgramDescription.objects.filter(program_number=program_number)
        if len(p_matches)==0:
            print "PROGRAM %s NOT FOUND" % program_number
        else:
             p = p_matches[0]   
             p.sectors.add(s)
             p.save()        

    f.close()
    
    
def check_cfda():
    f = open('energy_cfda', 'r')
    i = 0
    while True:
        i += 1
        l = f.readline()
        if not l:
            break
        program_number = l.strip()
    
        p = ProgramDescription.objects.filter(program_number=program_number)
        print "%3d: %s" % (i, p[0].sectors.values())
    
    f.close()

def simplify_naics():
    """ eliminate diplicates -- this table is sort of a mess, for unknown reasons"""
    to_examine = {}
    for c in NAICSCode.objects.all():
        to_examine[c.code] = True
    
    
    for i in to_examine.keys():        
        print i
        
        matching_codes = NAICSCode.objects.filter(code=i)
        c = matching_codes[0]
        to_delete = []
        code = False
        name = False
        for d in matching_codes:
            code = code or d.code
            name = name or d.name
            if d.id!=c.id: # save the first one
                to_delete.append(d.id)

        c.code = code
        c.name = name
        c.save()

        NAICSCode.objects.filter(id__in=to_delete).delete() # delete the rest


def shared_import(model, filename):
    
    energy_sector = get_energy_sector()
    
    f = open(filename, 'rU')
    reader = csv.reader(f)
    while True:
        row = reader.next()
        if not row:
            break

        code = row[0].strip()
        name = row[1].strip()
        
        if code and name:
            obj, created = model.objects.get_or_create(code=code, defaults={'name': name})
            obj.sectors.add(energy_sector)
            obj.save()
        
    f.close()
    
def import_naics():
    shared_import(NAICSCode, 'energy/energy_naics.csv')

def import_psc():
    shared_import(ProductOrServiceCode, 'energy/energy_psc.csv')
