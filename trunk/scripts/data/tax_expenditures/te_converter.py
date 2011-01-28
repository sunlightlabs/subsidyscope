#!/usr/bin/env python

import os, re
import urllib
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from sectors.models import Sector, Subsector

from tax_expenditures.models import TaxExpenditure, TaxExpenditureEstimate, OMBExpenditureEstimate

# converts tax expenditures, as imported from the OMB/AP documents into generic tax expenditure model for the site.
# takes only the most recent estimate for any given analysis year.
# also groups multiple tax_expenditure categories from the OMB data into a single item

te_ids = [61]
te_name = 'Deferral of tax on shipping companies'

sector = Sector.objects.get(pk=2)
subsector = Subsector.objects.get(pk=1)
expenditure = TaxExpenditure.objects.create(name=te_name, sector=sector, subsector=subsector)

estimate_years = {}

for estimate in OMBExpenditureEstimate.objects.filter(expenditure__pk__in=te_ids):
    
    if not estimate_years.has_key(estimate.estimate_year):
        
        estimate_years[estimate.estimate_year] = {}
    
    estimate_years[estimate.estimate_year][estimate.analysis_year] = estimate


for estimate_year in estimate_years:
    
    analysis_years = estimate_years[estimate_year].keys()
    
    most_recent_analysis_year = max(analysis_years)
    
    estimate = estimate_years[estimate_year][most_recent_analysis_year]
    
    convereted_estimate = TaxExpenditureEstimate.objects.create(expenditure=expenditure, 
                                                                analysis_year=estimate.analysis_year, 
                                                                estimate_year=estimate.estimate_year,
                                                                corporations_amount=estimate.corporations_amount, 
                                                                individuals_amount=estimate.individuals_amount)
    
        
        
        
