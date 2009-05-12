import os

county_amounts = {}
county_loans = {}

for institution in Institution.objects.exclude(fed_number__is=None)

for institution in institutions.readlines():
    
    raw_data = open('inst/%s' % (institution), 'r')
    
    while True:
        
        lines = raw_data.readlines(1000)
        
        if not lines:
            break
        
        current_institution = None
        institution_file = None
        
        for line in lines:
            
            line_parts = line.split(',')
            amount = line_parts[0]
            state = line_parts[1]
            county = line_parts[2]
        
            county = '%s,%s' % (state, county)
            
            if not county_amounts.has_key(county):
                county_amounts[county] = 0
                
            if not county_loans.has_key(county):
                county_loans[county] = 0
                
            county_amounts[county] += int(amount)
            county_loans[county] += 1
                
    
    raw_data.close()
    
    
county_file = open('%s_counties' % institution_name, 'wa')
    
for county in county_loans.keys():
    county_file.write('%s,%d,%d\n' % (county, county_loans[county], county_amounts[county]))