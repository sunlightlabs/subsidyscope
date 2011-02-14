#!/usr/bin/env python
import os
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from bailout.models import * 

from etl.models import *
from django.core.exceptions import ObjectDoesNotExist

from BeautifulSoup import BeautifulSoup
import re, os

report_date = date(2008, 12, 31)
crawl_date = date(2009, 3, 17)

nonnumeric = re.compile('[^0-9]')


for institution in Institution.objects.exclude(ots_number=''):
    
    if institution.institutionassethistory_set.all().count() == 0 and institution.transaction_set.all().count() > 0:
        
        url = 'http://www.ots.treas.gov/?p=InstitutionSearch&hid=%s' % (institution.ots_number)
        data = urllib.urlopen(url)
        
        soup = BeautifulSoup(data.read()) 
        
        print institution.ots_number
        
        institutionProfile = soup.findAll("table", attrs={"class":"institutionProfile"})
        
        if len(institutionProfile) > 0:
            assets = nonnumeric.sub('', institutionProfile[0].findAll("td")[4].string.strip())
            
            print assets
            
            InstitutionAssetHistory.objects.create(institution=institution,
                                               report_date=report_date,
                                               crawl_date=crawl_date,
                                               total_deposits=None,
                                               total_assets=assets)   