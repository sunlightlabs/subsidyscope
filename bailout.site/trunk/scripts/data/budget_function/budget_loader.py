import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from budget_accounts.models import TreasuryAccount, BudgetAuthorityHistory, BudgetOutlayHistory

census_file = open('OUTLAYS_FY2010.txt', 'r')

lines = census_file.readlines()

header = lines[0].strip().split('\t')

account_objects = {}

for account in TreasuryAccount.objects.all():
    
    if not account_objects.has_key(account.agency.code):
        account_objects[account.agency.code] = {}
    
    account_objects[account.agency.code][account.account] = account
    

#for year_idx in range(13,45):# - for budget_auth table

for year_idx in range(28,60):
    
    year = int(header[year_idx])
    print year

    account_totals = {}
    account_names = {}
    
    for line in lines[1:]:
        
        line_parts = line.strip().split('\t')
    
        try:
            agency_code = int(line_parts[6])
            account_code = int(line_parts[4][0:4])
            
            
            if not account_totals.has_key(agency_code):
                account_totals[agency_code] = {}
                account_names[agency_code] = {}
            
            if not account_totals[agency_code].has_key(account_code):
                account_totals[agency_code][account_code] = 0
                
            account_totals[agency_code][account_code] += (int(line_parts[year_idx]) * 1000)
            account_names[agency_code][account_code] = line_parts[8]
            
        except:
            pass
    
    
    for agency_code in account_totals:
        for account_code in account_totals[agency_code]:
            
            if agency_code > 0 and account_code > 0:
        
                if account_objects.has_key(agency_code) and account_objects[agency_code].has_key(account_code):
                    account = account_objects[agency_code][account_code]
                else:
                    account_name = account_names[agency_code][account_code]
                    
                    account = TreasuryAccount.objects.createTreasuryAccount(agency_code, account_code, account_name)
                    if not account_objects.has_key(agency_code):
                        account_objects[agency_code] = {}
                    account_objects[agency_code][account_code] = account
                    
                    print 'created account: %dx%d' % (agency_code, account_code)
                    
                BudgetOutlayHistory.objects.create(treasury_account=account, fiscal_year=year, outlay=account_totals[agency_code][account_code])
                
            
                
    
    
    