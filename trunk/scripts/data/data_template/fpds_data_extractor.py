import os, re, sys, csv
import MySQLdb
from datetime import date

sys.path.append('/home/kaitlin/envs/subsidyscope/trunk')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings

from sectors.models import Sector  


def extract_data():
    
    sector = Sector.objects.get(pk=5)
    
    naics_list_nonreporiting = {}
    naics_list = []
    
    for naics in sector.naicscode_set.all():
        naics_list.append(str(naics.code))
        naics_list_nonreporiting[str(naics.code)] = True
    
    psc_list_nonreporiting = {}   
    psc_list = []
    
    for psc in sector.productorservicecode_set.all():
        psc_list.append(psc.code)
        psc_list_nonreporiting[psc.code] = True
               
    naics_list_string = ', '.join(naics_list)
    psc_list_string = '\'' + '\', \''.join(psc_list) + '\''
    
    sql_totals = "SELECT fiscal_year, SUM(obligatedAmount) as annual_amount FROM %s WHERE TRIM(UPPER(extentCompeted)) IN ('B', 'C', 'D', 'E', 'G', 'NDO') AND ((TRIM(UPPER(principalNAICSCode)) IN (%s)) OR ((TRIM(principalNAICSCode)='') AND (TRIM(UPPER(productOrServiceCode)) IN (%s)))) GROUP BY fiscal_year;" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'], naics_list_string, psc_list_string) 
    
    conn = MySQLdb.connect(host=settings.FPDS_IMPORT_MYSQL_SETTINGS['host'], user=settings.FPDS_IMPORT_MYSQL_SETTINGS['user'], passwd=settings.FPDS_IMPORT_MYSQL_SETTINGS['password'], db=settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], port=settings.FPDS_IMPORT_MYSQL_SETTINGS['port'], cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    
    print "Querying FPDS from %s.%s" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'])
    print sql_totals
    
#    try:
    cursor.execute(sql_totals)
 #   except:
  #      pass
    
    totals = {}
    
    while True:
        
        row = cursor.fetchone()
        if row is None:
            break
        
        totals[row['fiscal_year']] = row['annual_amount']
    
        
    sql_naics = "SELECT principalNAICSCode, fiscal_year, SUM(obligatedAmount) as annual_amount FROM %s WHERE TRIM(UPPER(extentCompeted)) IN ('B', 'C', 'D', 'E', 'G', 'NDO') AND TRIM(UPPER(principalNAICSCode)) IN (%s)  GROUP BY principalNAICSCode, fiscal_year;" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'], naics_list_string) 
    
    conn = MySQLdb.connect(host=settings.FPDS_IMPORT_MYSQL_SETTINGS['host'], user=settings.FPDS_IMPORT_MYSQL_SETTINGS['user'], passwd=settings.FPDS_IMPORT_MYSQL_SETTINGS['password'], db=settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], port=settings.FPDS_IMPORT_MYSQL_SETTINGS['port'], cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    
    print "Querying FPDS NAICS from %s.%s" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'])
    print sql_naics
    
    try:
        cursor.execute(sql_naics)
    except:
        pass
    
    naics_totals = {}
    
    while True:
        
        row = cursor.fetchone()
        
        if row is None:
            break
        
        naics_list_nonreporiting[row['principalNAICSCode']] = False
        
        if not naics_totals.has_key(row['principalNAICSCode']):
            naics_totals[row['principalNAICSCode']] = {}
                
        naics_totals[row['principalNAICSCode']][row['fiscal_year']] = row['annual_amount']
        
    
    
    sql_psc = "SELECT productOrServiceCode, fiscal_year, SUM(obligatedAmount) as annual_amount FROM %s WHERE TRIM(UPPER(extentCompeted)) IN ('B', 'C', 'D', 'E', 'G', 'NDO') AND ((TRIM(principalNAICSCode)='') AND (TRIM(UPPER(productOrServiceCode)) IN (%s)))  GROUP BY productOrServiceCode, fiscal_year;" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'], psc_list_string) 
    
    conn = MySQLdb.connect(host=settings.FPDS_IMPORT_MYSQL_SETTINGS['host'], user=settings.FPDS_IMPORT_MYSQL_SETTINGS['user'], passwd=settings.FPDS_IMPORT_MYSQL_SETTINGS['password'], db=settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], port=settings.FPDS_IMPORT_MYSQL_SETTINGS['port'], cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    
    print "Querying FPDS PSC from %s.%s" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'])
    print sql_psc
    
    try:
        cursor.execute(sql_psc)
    except:
        pass
    
    psc_totals = {}
    
    while True:
        
        row = cursor.fetchone()
        
        if row is None:
            break
        
        psc_list_nonreporiting[row['productOrServiceCode']] = False
        
        if not psc_totals.has_key(row['productOrServiceCode']):
            psc_totals[row['productOrServiceCode']] = {}
                
        psc_totals[row['productOrServiceCode']][row['fiscal_year']] = row['annual_amount']
        
        
    fiscal_year_range = range(2000, 2011)
    
    final_data = []
    
    final_data.append(["Querying %s.%s" % (settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], settings.FPDS_IMPORT_MYSQL_SETTINGS['source_table'])])
    final_data.append(["Run %s" % (date.today().strftime("%Y-%m-%d"))])                   
    
    final_data.append([])
    final_data.append([])
    
    annual_totals_row = []
    
    annual_totals_row.append('Total')
    
    for year in fiscal_year_range:
        if totals.has_key(year):
            annual_totals_row.append(totals[year])
        else:
            annual_totals_row.append('')
 
    final_data.append(annual_totals_row)
    final_data.append([])
    final_data.append([])
    
    final_data.append(['NAICS Totals'])
    
    for naics in naics_totals:
        
        row = []
        row.append(naics)
        
        for year in fiscal_year_range:
            if naics_totals[naics].has_key(year):
                row.append(naics_totals[naics][year])
            else:
                row.append('')
        
        final_data.append(row)
    
    final_data.append([])
    final_data.append([])
    
    final_data.append(['PSC Totals'])
    
    for psc in psc_totals:
        
        row = []
        row.append(psc)
        
        for year in fiscal_year_range:
            if psc_totals[psc].has_key(year):
                row.append(psc_totals[psc][year])
            else:
                row.append('')
        
        final_data.append(row)
    
    final_data.append([])
    final_data.append([])
    
    final_data.append(['Non-reporting NAICS'])
    
    for naics in naics_list_nonreporiting:
        if naics_list_nonreporiting[naics]:
            final_data.append([naics])
    
    final_data.append([])
    final_data.append([])
    
    final_data.append(['Non-reporting PSC'])
    
    for psc in psc_list_nonreporiting:
        if psc_list_nonreporiting[psc]:
            final_data.append([psc])
    
    final_data.append([])
    final_data.append([])
    final_data.append([sql_totals])
    
    final_data.append([])
    final_data.append([])
    final_data.append([sql_naics])
    
    final_data.append([])
    final_data.append([])
    final_data.append([sql_psc])
        
    output_csv = csv.writer(open('%s_fpds_%s.csv' % (sector.name, date.today().strftime("%Y%m%d")), 'wb'))
    output_csv.writerows(final_data)  
        
extract_data()    
