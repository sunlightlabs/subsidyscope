from pysolr import Solr
from django.db import models
from decimal import Decimal
from faads.models import *
import cfda.models
import django.db.models.fields
from django.core.cache import cache
from md5 import md5
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

# preload fk lookup tables

CFDA_PROGRAM_FK_LOOKUP = {}
for c in cfda.models.ProgramDescription.objects.all():
    CFDA_PROGRAM_FK_LOOKUP[str(c.program_number)] = c.id

ACTION_TYPE_FK_LOOKUP = {}
for a in ActionType.objects.all():
    ACTION_TYPE_FK_LOOKUP[a.code] = a.id
    
ASSISTANCE_TYPE_FK_LOOKUP = {}
for a in AssistanceType.objects.all():
    ASSISTANCE_TYPE_FK_LOOKUP[a.code] = a.id    

RECIPIENT_TYPE_FK_LOOKUP = {}
for r in RecipientType.objects.all():
    RECIPIENT_TYPE_FK_LOOKUP[r.code] = r.id

RECORD_TYPE_FK_LOOKUP = {}
for r in RecordType.objects.all():
    RECORD_TYPE_FK_LOOKUP[r.code] = r.id
    

class FAADSSearch():
    
    SOLR_MAX_RECORDS = 1000000
    
    FIELD_MAPPINGS = {

        'FIELD_BUDGET_FUNCTION': 'budget_function', # NOT YET IMPLEMENTED IN MODEL
        'FIELD_FUNDING_TYPE': 'funding_type', # NOT YET IMPLEMENTED IN MODEL

        'FIELD_CFDA_PROGRAM': {'fieldname': 'cfda_program', 'fk_transformation': lambda x: CFDA_PROGRAM_FK_LOOKUP.get(str(x).strip(), None) },
        'FIELD_ACTION_TYPE': {'fieldname': 'action_type', 'fk_transformation': lambda x: ACTION_TYPE_FK_LOOKUP.get(x, None) },
        'FIELD_RECIPIENT_TYPE': {'fieldname': 'recipient_type', 'fk_transformation': lambda x: RECIPIENT_TYPE_FK_LOOKUP.get(x, None) },
        'FIELD_RECORD_TYPE': {'fieldname': 'record_type', 'fk_transformation': lambda x: RECORD_TYPE_FK_LOOKUP.get(x, None) },
        'FIELD_ASSISTANCE_TYPE': {'fieldname': 'assistance_type', 'fk_transformation': lambda x: ASSISTANCE_TYPE_FK_LOOKUP.get(x, None) },

        'FIELD_FISCAL_YEAR': 'fiscal_year',

        'FIELD_NON_FEDERAL_AMOUNT': 'non_federal_amount',
        'FIELD_FEDERAL_AMOUNT': 'federal_amount',
        'FIELD_TOTAL_AMOUNT': 'total_amount',

        'FIELD_TEXT': 'text',
        'FIELD_RECIPIENT': 'recipient',

        'FIELD_RECIPIENT_COUNTY': 'recipient_county',
        'FIELD_RECIPIENT_STATE': 'recipient_state',
        'FIELD_PRINCIPAL_PLACE_STATE': 'principal_place_state',
        'FIELD_PRINCIPAL_PLACE_COUNTY': 'principal_place_county'
    }
    
    CONJUNCTION_AND = {'solr': 'AND', 'mysql': 'AND'}
    CONJUNCTION_OR = {'solr': 'OR', 'mysql': 'OR'}
    
    
    def __init__(self):
        
        self.filters = []
         
        self.aggregate_by = None
        self.use_solr = False
        self.order_by = None 
        
        self.field_objects = {}
        for field in Record._meta.fields:
            self.field_objects[field.name] = field
     
    def get_query_cache_key(self):
        fs = ''
        for i,f in enumerate(self.filters):
            fs += "%d:{%s|%s|%s}" % (i, f[0], f[1], f[2])
        return md5(fs).hexdigest() # avoid key length problems...
           
                    
    def filter(self, filter_by, filter_value, filter_conjunction=CONJUNCTION_AND):        
        self.filters.append( (filter_by, filter_value, filter_conjunction))
        if not self.use_solr and (filter_by in (self.FIELD_MAPPINGS['FIELD_TEXT'], self.FIELD_MAPPINGS['FIELD_RECIPIENT'])):
            self.use_solr = True
        return self
    
    
    def aggregate(self, aggregate_by):
        
        self.aggregate_by = aggregate_by

        # check for cached result
        cached_result = cache.get(self.get_query_cache_key())
        if cached_result is not None:
            return cached_result
    
        # handling full-text aggregation with solr/python hack
        if self.use_solr:                        
            
            solr = Solr(settings.HAYSTACK_SOLR_URL)

            query = ''
            for i,f in enumerate(self.filters):
                filter_field = f[0]
                filter_value = f[1]
                filter_conjunction = f[2]
                
                if i>0:
                    query += " %s " % filter_conjunction['solr'] 

                query += filter_field + ": %d " % filter_value


            solr_result = solr.search(q=query % (self.filter_by, self.filter_value), 
                        rows=FAADSSearch.SOLR_MAX_RECORDS,
                        fl='total_amount,%s' % (self.aggregate_by))
            
            result = {}
            
            # aggregation
            for doc in solr_result.docs:
                
                key = int(doc[self.aggregate_by])
                
                if not result.has_key(key):
                    result[key] = Decimal(0)
                
                result[key] += Decimal(str(doc['total_amount'])) 
            
            cache.set(self.get_query_cache_key(), result)
            
            return result
            
        # handling key based aggregation with db group by/sum
        else:
            
            from django.db import connection
            cursor = connection.cursor()    
            
            if self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['FIELD_FISCAL_YEAR']:
                # an exception to the field naming rule...
                aggregate_field = self.aggregate_by
            else:
                # otherwise append id to all foreign key fields to match db schema
                aggregate_field = self.aggregate_by + '_id'
            
            # budget_function or funding_type fields require join through budget_account model
            # ick! punting on this for now...
            if self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['FIELD_BUDGET_FUNCTION'] or self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['FIELD_FUNDING_TYPE']:
                raise Exception('Currently not handling many-to-many joins on MySQL queries.')
            
            # check to ensure we're not aggregating in an unsupported manner
            filter_fields = map(lambda x: x[0], self.filters)
            if FAADSSearch.FIELD_MAPPINGS['FIELD_BUDGET_FUNCTION'] in filter_fields or FAADSSearch.FIELD_MAPPINGS['FIELD_FUNDING_TYPE'] in filter_fields:
                raise Exception('Currently not handling many-to-many joins on MySQL queries.')

            sql_parameters = [] # uses proper django.db SQL-escaping, in case we ever introduce nonnumeric queries for some reason
            sql = " SELECT  %s as field, sum(total_funding_amount) as value FROM faads_record WHERE " % aggregate_field
            
            for i,f in enumerate(self.filters):
                
                filter_field = f[0]
                filter_value = f[1]
                filter_conjunction = f[2]


                # filter value must cast to int for type queries
                if self.field_objects[filter_field].db_type==django.db.models.fields.CharField:
                    value = int(self.filter_value)
                elif self.field_objects[filter_field].db_type==django.db.models.fields.DecimalField:
                    value = Decimal(self.filter_value)

                # handle fk fields
                elif type(self.field_objects[filter_field])==django.db.models.fields.related.ForeignKey:
                    successfully_mapped_fk_field = False
                    for k in FAADSSearch.FIELD_MAPPINGS.values():                      
                            
                        if type(k)==dict and k.get('fieldname')==filter_field and k.has_key('fk_transformation'):
                            fk_transformation = k.get('fk_transformation')
                            filter_value = fk_transformation(filter_value)
                                                        
                            # there's no such foreign key value. create an impossible logical clause
                            if filter_value is None:
                                filter_field = ' 1 '
                                filter_value = ' 2 '
                            else:
                                filter_field += '_id'
                                
                            successfully_mapped_fk_field = True
                            break

                    if not successfully_mapped_fk_field:
                        continue
                    
                
                if i>0:
                    sql += " %s " % filter_conjunction['mysql'] 

                sql += filter_field + "= %s "
                sql_parameters.append(int(filter_value))

                
            sql += " GROUP BY %s " % aggregate_field
            
            print sql
            
            cursor.execute(sql, sql_parameters)
            
            result = {}
            
            for row in cursor.fetchall():
                result[row[0]] = row[1]
    
            cache.set(self.get_query_cache_key(), result)
    
            return result
    
    def results(start=0, limit=100):

        # can get results using Haystack... 
            
        pass 
    
    def count(self):
        
        pass
        
def test():
    fs = FAADSSearch()
    print fs.filter('cfda_program', '20.205').aggregate('fiscal_year')
    