import os

county_amounts = {}
county_loans = {}

raw_data = open('2007_hmda.csv', 'r')

while True:
    
    lines = raw_data.readlines(1000)
    
    if not lines:
        break
    
    current_institution = None
    institution_file = None
    
    for line in lines:
        
        line_parts = line.split(',')
        
        institution = line_parts[1]
        amount = line_parts[7]
        action = line_parts[9]
        state = line_parts[11]
        county = line_parts[12]
        
        # only extracting geo-located loans originated by reporter
        if state != 'NA' and county != 'NA' and action == '1':
            
            if current_institution != institution or institution_file == None:
                current_institution = institution
                
                if institution_file != None:
                    institution_file.close()
                
                institution_file = open('inst/%s' % (current_institution), 'wa')
                    
            institution_file.write('%s,%s,%s\n' % (amount, state, county))
            
            county = '%s,%s' % (state, county)
            
            if not county_amounts.has_key(county):
                county_amounts[county] = 0
                
            if not county_loans.has_key(county):
                county_loans[county] = 0
                
            county_amounts[county] += int(amount)
            county_loans[county] += 1
                
    if institution_file != None:
        institution_file.close()

county_file = open('counties', 'wa')

for county in county_loans.keys():
    county_file.write('%s,%d,%d\n' % (county, county_loans[county], county_amounts[county]))