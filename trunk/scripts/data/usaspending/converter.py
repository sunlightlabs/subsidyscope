import csv
import sys
import os
import re

from fpds import *
from faads import *

re_contracts = re.compile('.*[cC]ontracts.*')

def parseFile(input, output, fields):
    
    reader = csv.DictReader(input)

    for line in reader:
        
        insert_fields = []
        
        for field in fields:
            
            csv_fieldname = field[0]
            db_fieldname = field[1]
            transform = field[2]
            
            
            try:
                if transform:
                    value = transform(line[csv_fieldname])
                else:
                    value = line[csv_fieldname]
                    
            except:
                value = None
                print >> sys.stderr, csv_fieldname, line[csv_fieldname]
                

            if value:
                if isinstance(value, int):
                    field_assignment = '"%d"' % value
                elif isinstance(value, float):
                    field_assignment = '"%f"' % value
                else:
                    field_assignment = '"%s"' % value
                
                insert_fields.append(field_assignment)
                
            else:
                insert_fields.append('NULL')
        
        print >> output, ','.join(insert_fields)    



def parseDirectory(path):
    
    out_path = os.path.join(path, 'out')
    
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    
    out_grants = open(os.path.join(os.path.join(out_path, 'grants.out')), 'w')
    out_contracts = open(os.path.join(os.path.join(out_path, 'contracts.out')), 'w')

    for file in os.listdir(path):
        
        file_path = os.path.join(path, file)
        
        if os.path.isfile(file_path):
            
            input = open(file_path, 'rb')
            
            print >> sys.stderr, file_path
            
            if re_contracts.match(file):
                parseFile(input, out_contracts, FPDS_FIELDS)
            else:
                parseFile(input, out_grants, FAADS_FIELDS)
                
            input.close()
        
    out_grants.close()
    out_contracts.close()
    

parseDirectory('/tmp/data/')
