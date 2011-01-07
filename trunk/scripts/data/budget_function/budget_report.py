import os, re, sys

sys.path.append('/root/subsidyscope/bailout.site/trunk/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from budget_accounts.models import BudgetAccount, BudgetAuthorityHistory, BudgetOutlayHistory
from cfda.models import ProgramDescription

from django.db import connection

for account in BudgetAccount.objects.filter(budget_function__parent__id=37):
    
    budget_authority = []
    budget_outlay = []
    
    for year in account.budgetauthorityhistory_set.filter(fiscal_year__gte=2000):
        budget_authority.append(str(year.authority))
    
    for year in account.budgetoutlayhistory_set.filter(fiscal_year__gte=2000):
        budget_outlay.append(str(year.outlay))
        
    print account.account_string
    print '\tAuthority\t%s' % ('\t'.join(budget_authority))
    print '\tOutlay\t%s' % ('\t'.join(budget_outlay))
    
    for cfda_program in account.programdescription_set.all():
    
        cursor = connection.cursor()     
        
        faads = {}
        
        for year in range(2000, 2008):
            faads[year] = 0
        
        cursor.execute('SELECT fiscal_year, sum(federal_funding_amount) FROM faads_record WHERE fiscal_year >= 2000 AND fiscal_year <= 2008 AND cfda_program_id = %d GROUP BY fiscal_year ORDER BY fiscal_year' % (cfda_program.id))           
        for row in cursor.fetchall():
            faads[row[0]] = str(row[1])
         
        print '\t%s\t%s' % (cfda_program.program_number, '\t'.join(faads))
        