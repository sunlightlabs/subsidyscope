from fpds import *
from faads import *

faads_fields = []

for field in FAADS_FIELDS:
    
    faads_fields.append(field[1])

print 'LOAD DATA INFILE \'file.csv\' INTO TABLE faads FIELDS TERMINATED BY \',\' ENCLOSED BY \'"\' (%s);' % (', '.join(faads_fields))  
    
    
    
    
    