import os, re, sys, csv
import MySQLdb
from datetime import date

# sys.path.append('')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings

from cfda.models import ProgramDescription
from sectors.models import Sector  

GRANT_ASSISTANCE = ['02', '03', '04', '05', '06', '10', '2', '3', '4', '5', '6']
LOAN_ASSISTANCE = ['07', '08', '09', '7', '8', '9']




def extract_data(label, aggregate_field, assistance_types):
    sector = Sector.objects.get(pk=5)

    programs = ProgramDescription.objects.filter(sectors=sector)
    
    cfda_numbers = []
    cfda_numbers_found = {}
    
    program_names = {}
    
    fiscal_year_range = range(2000, 2011)


    for program in programs:
        
        cfda_numbers.append("'%s'" % program.program_number)
        cfda_numbers_found[program.program_number] = False
    
        program_names[program.program_number] = program.program_title
    
    cfda_number_string = ', '.join(cfda_numbers)
    
    assistance_type_string = '\'' + '\', \''.join(assistance_types) + '\''
    
    sql = "SELECT fiscal_year, cfda_program_num, SUM(%s) as annual_amount FROM %s WHERE (TRIM(assistance_type) IN (%s)) AND (TRIM(cfda_program_num) IN (%s)) GROUP BY fiscal_year, cfda_program_num;" % (aggregate_field, settings.FAADS_IMPORT_MYSQL_SETTINGS['source_table'], assistance_type_string, cfda_number_string) 
    
    conn = MySQLdb.connect(host=settings.FAADS_IMPORT_MYSQL_SETTINGS['host'], user=settings.FAADS_IMPORT_MYSQL_SETTINGS['user'], passwd=settings.FAADS_IMPORT_MYSQL_SETTINGS['password'], db=settings.FAADS_IMPORT_MYSQL_SETTINGS['database'], port=settings.FAADS_IMPORT_MYSQL_SETTINGS['port'], cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    
    print "Querying %s from %s.%s" % (label, settings.FAADS_IMPORT_MYSQL_SETTINGS['database'], settings.FAADS_IMPORT_MYSQL_SETTINGS['source_table'])
    print sql
    
    try:
        cursor.execute(sql)
    except:
        pass
    
    program_data = {}
    annual_data = {}
        
    while True:
        
        row = cursor.fetchone()
        
        if row is None:
            break
        
        else:    
            if not program_data.has_key(row['cfda_program_num']):
                program_data[row['cfda_program_num']] = {}
                cfda_numbers_found[row['cfda_program_num']] = True
            if not annual_data.has_key(row['fiscal_year']):
                annual_data[row['fiscal_year']] = 0
                
            annual_data[row['fiscal_year']] += row['annual_amount']
            
            program_data[row['cfda_program_num']][row['fiscal_year']] = row['annual_amount']
            
    programs = program_data.keys()
    programs.sort()
    
    final_data = []  
    
    final_data.append(["Querying %s.%s" % (settings.FAADS_IMPORT_MYSQL_SETTINGS['database'], settings.FAADS_IMPORT_MYSQL_SETTINGS['source_table'])])
    final_data.append(["Run %s" % (date.today().strftime("%Y-%m-%d"))])                   
    final_data.append([])
    
    header_row = []
    header_row.append('CFDA Number')
    header_row.append('CFDA Title')
    
    for year in fiscal_year_range:
        header_row.append(year)
    
    final_data.append(header_row)
    
    annual_totals_row = []
    
    annual_totals_row.append('Total')
    annual_totals_row.append('')
    
    for year in fiscal_year_range:
        if annual_data.has_key(year):
            annual_totals_row.append(annual_data[year])
        else:
            annual_totals_row.append('')
    
    final_data.append([])
    
    final_data.append(annual_totals_row)
    
    final_data.append([])
    
    for cfda_number in programs:
        
        final_row = []
        
        final_row.append(cfda_number)
        final_row.append(program_names[cfda_number])
        
        for year in fiscal_year_range:
            
            if program_data[cfda_number].has_key(year):
                final_row.append(str(program_data[cfda_number][year]))
            else:
                final_row.append('')
             
        final_data.append(final_row)
        
    programs = cfda_numbers_found.keys()
    programs.sort()
    
    final_data.append([])
    final_data.append(['Non-reporting Programs'])
    final_data.append([])
    
    for program in programs:
        if not cfda_numbers_found[program]:
            final_data.append([program, program_names[program]])
    
    final_data.append([])
    final_data.append([])
    final_data.append([sql])
            
            
    output_csv = csv.writer(open('%s_faads_%s_%s.csv' % (sector.name, label, date.today().strftime("%Y%m%d")), 'wb'))
    output_csv.writerows(final_data)                   
                        
                        
extract_data('grants', 'fed_funding_amount', GRANT_ASSISTANCE)
extract_data('loans_face', 'face_loan_guran', LOAN_ASSISTANCE)
extract_data('loans_subsidy', 'orig_sub_guran', LOAN_ASSISTANCE)                    
    