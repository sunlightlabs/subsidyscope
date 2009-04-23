#!/usr/bin/python

import os
import sys
from BeautifulSoup import BeautifulSoup
import csv
import re

FIELDS = (
    'PROGRAM NUMBER',
    'PROGRAM TITLE',
    'FEDERAL AGENCY',
    'MAJOR AGENCY',
    'MINOR AGENCY',
    'AUTHORIZATION',
    'OBJECTIVES',
    'TYPES OF ASSISTANCE',
    'USES AND USE RESTRICTIONS',
    'APPLICANT ELIGIBILITY',
    'BENEFICIARY ELIGIBILITY',
    'CREDENTIALS/DOCUMENTATION',
    'PREAPPLICATION COORDINATION',
    'APPLICATION PROCEDURE',
    'AWARD PROCEDURE',
    'DEADLINES',
    'RANGE OF APPROVAL/DISAPPROVAL TIME',
    'APPEALS',
    'RENEWALS',
    'FORMULA AND MATCHING REQUIREMENTS',
    'LENGTH AND TIME PHASING OF ASSISTANCE',
    'REPORTS',
    'AUDITS',
    'RECORDS',
    'ACCOUNT IDENTIFICATION',
    'OBLIGATIONS',
    'RANGE AND AVERAGE OF FINANCIAL ASSISTANCE',
    'PROGRAM ACCOMPLISHMENTS',
    'REGULATIONS, GUIDELINES, AND LITERATURE',
    'REGIONAL OR LOCAL OFFICE',
    'HEADQUARTERS OFFICE',
    'WEB SITE ADDRESS',
    'RELATED PROGRAMS',
    'EXAMPLES OF FUNDED PROJECTS',
    'CRITERIA FOR SELECTING PROPOSALS'
)

def main(filename):

    re_cfda_program_number = re.compile(r'(\d{2,3}\.\d{3})')

    sys.stderr.write("parsing %s\n" % filename)

    f = open(filename, 'r')
    b = BeautifulSoup(''.join(f.readlines()))
    f.close()

    record = {}
    tables = b.findAll('table')
    for table in tables[2:-1]:                
        key = False
        value = ''
        rows = table.findAll('tr')
        for row in rows:
            row_contents = ''
            cells = row.findAll('td')
            for cell in cells:
                if len(cell.contents)>0:
                    try:
                        row_contents = row_contents + ''.join(cell.contents).strip()
                    except:
                        row_contents = row_contents + str(cell.contents[0])
                        pass
            
            if row_contents>0:
                if key:
                    value = value + row_contents
                else:
                    key = row_contents.upper()
                
        
        if len(key) and len(value):
            record[key] = value
            # if key=='WEB SITE ADDRESS':                
            #                 print '%s: %s' % (key, value)
        elif len(key):
            m = re_cfda_program_number.search(key)
            if m:
                record['PROGRAM NUMBER'] = m.group(1)
                record['PROGRAM TITLE'] = key.replace(record['PROGRAM NUMBER'],'').strip()                

    if record['FEDERAL AGENCY']:
        agency_parts = record['FEDERAL AGENCY'].split(',')
        record['MAJOR AGENCY'] = agency_parts[-1].strip()
        record['MINOR AGENCY'] = ','.join(agency_parts[:-1]).strip()
    
    writer = csv.writer(sys.stdout)
    row = []
    for f in FIELDS:
        row.append(record.get(f,''))
    writer.writerow(row)

    # for f in FIELDS:
    #         if not f in record:
    #             print 'missing field in file %s: %s' % (filename, f)
            

if __name__ == '__main__':
    main(sys.argv[1])