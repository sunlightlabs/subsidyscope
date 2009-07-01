from pysolr import Solr
from django.db import models
from decimal import Decimal

import settings

"""

Examples for use:

basic aggregation query using db :

>> from faads.search import *
>> search = FAADSSearch()
>> search.filter(FAADSSearch.FIELD_ACTION_TYPE, 5)
>> search.aggregate(aggregate_by=FAADSSearch.FIELD_FISCAL_YEAR)

{2000: Decimal("43771085.00"),
 2001: Decimal("103478574.00"),
 2002: Decimal("62141644.00"),
 2003: Decimal("94885104.00"),
 2004: Decimal("-29431942.00")}



aggregation using solr:

>> search.filter(FAADSSearch.FIELD_TEXT, 'road')
>> search.aggregate(aggregate_by=FAADSSearch.FIELD_RECIPIENT_STATE)

{1: Decimal("-14059"),
 2: Decimal("3554590"),
 3: Decimal("-33194"),
 4: Decimal("593589"),
 5: Decimal("15900915")}



"""
class FAADSSearch():
    
    SOLR_MAX_RECORDS = 1000000
    
    FIELD_CFDA_PROGRAM = 'cfda_program'
    FIELD_BUDGET_FUNCTION = 'budget_function'
    FIELD_FUNDING_TYPE = 'funding_type'
    
    FIELD_ACTION_TYPE = 'action_type'
    FIELD_RECIPIENT_TYPE = 'recipient_type'
    FIELD_RECORD_TYPE = 'record_type'
    FIELD_ASSISTANCE_TYPE = 'assistance_type'
    
    FIELD_FISCAL_YEAR = 'fiscal_year'
    
    FIELD_NON_FEDERAL_AMOUNT = 'non_federal_amount'
    FIELD_FEDERAL_AMOUNT = 'federal_amount'
    FIELD_TOTAL_AMOUNT = 'total_amount'
    
    FIELD_TEXT = 'text'
    FIELD_RECIPIENT = 'recipient'
    
    FIELD_RECIPIENT_COUNTY = 'recipient_county'
    FIELD_RECIPIENT_STATE = 'recipient_state'
    FIELD_PRINCIPAL_PLACE_STATE = 'principal_place_state'
    FIELD_PRINCIPAL_PLACE_COUNTY = 'principal_place_county'
    
    
    def __init__(self):
        
        self.filter_by = None
        self.filter_value = None 
         
        self.aggregate_by = None
        self.order_by = None 
        
    def filter(self, filter_by, filter_value):
            
        self.filter_by = filter_by 
        self.filter_value = filter_value 
    
    
    def aggregate(self, aggregate_by):
        
        self.aggregate_by = aggregate_by
    
        # handling full-text aggregation with solr/python hack
        if self.filter_by == FAADSSearch.FIELD_TEXT or self.filter_by == FAADSSearch.FIELD_RECIPIENT:
            
            solr = Solr(settings.HAYSTACK_SOLR_URL)
            
            solr_result = solr.search(q='%s: %s' % (self.filter_by, self.filter_value), 
                        rows=FAADSSearch.SOLR_MAX_RECORDS,
                        fl='total_amount,%s' % (self.aggregate_by))
            
            result = {}
            
            for doc in solr_result.docs:
                
                key = int(doc[self.aggregate_by])
                
                if not result.has_key(key):
                    result[key] = Decimal(0)
                
                result[key] += Decimal(str(doc['total_amount'])) 
            
            return result
            
        # handling key based aggregation with db group by/sum
        else:
            
            from django.db import connection
            cursor = connection.cursor()    
            
            if self.aggregate_by == FAADSSearch.FIELD_FISCAL_YEAR:
                # an exception to the field naming rule...
                aggregate_field = self.aggregate_by
            else:
                # otherwise append id to all foreign key fields to match db schema
                aggregate_field = self.aggregate_by + '_id'
            
            # budget_function or funding_type fields require join through budget_account model
            # ick! punting on this for now...
            if self.aggregate_by == FAADSSearch.FIELD_BUDGET_FUNCTION or self.aggregate_by == FAADSSearch.FIELD_FUNDING_TYPE:
                raise Exception('Currently not handling many-to-many joins on MySQL queries.')
            
            sql = 'SELECT  %s as field, sum(total_funding_amount) as value FROM faads_record ' % (aggregate_field) 
            
            if self.filter_by != None:
                
                if self.filter_by == FAADSSearch.FIELD_BUDGET_FUNCTION or self.filter_by == FAADSSearch.FIELD_FUNDING_TYPE:
                    raise Exception('Currently not handling many-to-many joins on MySQL queries.')
                
                filter_field = self.filter_by + '_id'
                
                # filter value must cast to int for type queries
                value = int(self.filter_value)
                 
                sql += ' WHERE %s = %d ' % (filter_field, value)
        
            sql += ' GROUP BY %s ' % (aggregate_field)
            
            print sql
            
            cursor.execute(sql)
            
            result = {}
            
            for row in cursor.fetchall():
                result[row[0]] = row[1]
    
            return result
    
    def results(start=0, limit=100):

        # can get results using Haystack... 
            
        pass 
    
    def count(self):
        
        pass
    