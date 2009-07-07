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

        'budget_function': {
            'type': None, # NOT YET IMPLEMENTED
            'mysql_field': 'budget_function',
            'solr_field': 'budget_function',
        },
        
        'funding_type': {
            'type': None, # NOT YET IMPLEMENTED IN MODEL            
            'mysql_field': 'funding_type',
            'solr_field': 'funding_type'
        },
         
        'cfda_program': {
            'type': 'fk',
            'mysql_fieldname': 'cfda_program', 
            'solr_fieldname': 'cfda_program', 
            'fk_transformation': lambda x: CFDA_PROGRAM_FK_LOOKUP.get(str(x).strip(), None) 
        },
                
        'action_type': {
            'type': 'fk',
            'mysql_fieldname': 'action_type', 
            'solr_fieldname': 'action_type',
            'fk_transformation': lambda x: ACTION_TYPE_FK_LOOKUP.get(x, None) 
        },
        
        'recipient_type': {
            'type': 'fk',
            'mysql_fieldname': 'recipient_type', 
            'solr_fieldname': 'recipient_type', 
            'fk_transformation': lambda x: RECIPIENT_TYPE_FK_LOOKUP.get(x, None) 
        },
        
        'record_type': {
            'type': 'fk',
            'mysql_fieldname': 'record_type', 
            'solr_fieldname': 'record_type', 
            'fk_transformation': lambda x: RECORD_TYPE_FK_LOOKUP.get(x, None) 
        },

        'assistance_type': {
            'type': 'fk',
            'mysql_fieldname': 'assistance_type',
            'solr_fieldname': 'assistance_type',
            'fk_transformation': lambda x: ASSISTANCE_TYPE_FK_LOOKUP.get(x, None)
        },

        'fiscal_year': {
            'type': 'range',
            'mysql_field': 'fiscal_year',
            'solr_field': 'fiscal_year'    
        },

        'obligation_action_date': {
            'type': 'range',
            'mysql_field': 'obligation_action_date',
            'solr_field': 'obligation_date'
        },

        'non_federal_funding_amount': {
            'type': 'range',
            'mysql_field': 'non_federal_funding_amount',
            'solr_field': 'non_federal_amount'
        },
        
        'federal_funding_amount': {
            'type': 'range',
            'mysql_field': 'federal_funding_amount',
            'solr_field': 'federal_amount'            
        },
        
        'total_funding_amount': {
            'type': 'range',
            'mysql_field': 'total_funding_amount',
            'solr_field': 'total_amount'            
        },
        
        'text': {
            'type': 'text',
            'solr_field': 'text',
        },
        
        'recipient': {
            'type': 'text',
            'solr_field': 'recipient'
        }


        # 'FIELD_RECIPIENT_COUNTY': 'recipient_county',
        # 'FIELD_RECIPIENT_STATE': 'recipient_state',
        # 'FIELD_PRINCIPAL_PLACE_STATE': 'principal_place_state',
        # 'FIELD_PRINCIPAL_PLACE_COUNTY': 'principal_place_county'
    }
    
    CONJUNCTION_AND = {'solr': 'AND', 'mysql': 'AND'}
    CONJUNCTION_OR = {'solr': 'OR', 'mysql': 'OR'}
    
    
    def __init__(self):
        
        self.filters = []
         
        self.aggregate_by = None
        self.use_solr = False
        self.order_by = None
        self.cache = True
        
        self.field_objects = {}
        for field in Record._meta.fields:
            self.field_objects[field.name] = field
    
    # clone function (to enable chainable filtering) blatantly stolen from haystack (which presumably stole it from Django)
    def _clone(self, klass=None):

        if klass is None:
            klass = self.__class__

        clone = klass()
        clone.aggregate_by = self.aggregate_by
        clone.use_solr = self.use_solr
        clone.order_by = self.order_by
        clone.cache = self.cache
        clone.field_objects = self.field_objects.copy()
        clone.filters = self.filters[:]
        
        return clone
    
    def use_cache(self, u=True):
        clone = self._clone()
        clone.cache = u
        return clone
            
    def get_query_cache_key(self):
        fs = ''
        for i,f in enumerate(self.filters):
            fs += "%d:{%s|%s|%s}" % (i, str(f[0]), str(f[1]), str(f[2]))
        return md5(fs).hexdigest() # avoid key length problems...
           
                    
    def filter(self, filter_by, filter_value, filter_conjunction=CONJUNCTION_AND):   

        field_lookup = FAADSSearch.FIELD_MAPPINGS.get(filter_by,None)
        if field_lookup is None:
            raise Exception("'%s' is not a valid filter field" % filter_by)
        elif field_lookup['type']=='range' and ((type(filter_value) not in (list, tuple)) or (len(filter_value)!=2)):
            raise Exception("'%s' is a ranged field. Please pass a tuple or list of length 2 (None==wildcard)")

        clone = self._clone()
        
        clone.filters.append( (filter_by, filter_value, filter_conjunction) )
        if not clone.use_solr and (clone.FIELD_MAPPINGS[filter_by]['type']=='text'):
            clone.use_solr = True
            
        return clone
    
    
    def aggregate(self, aggregate_by):
        
        self.aggregate_by = self.FIELD_MAPPINGS.get(aggregate_by, None)
        if self.aggregate_by is None:
            raise Exception("Cannot aggregate by %s - not a valid field" % aggregate_by)

        # check for cached result
        if self.cache:
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
            
            
            # TODO: determine if this is necessary -- IDs will be consistent, after all... may be that rewriting the codes on output is more appropriate
            if self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['fiscal_year']:
                # an exception to the field naming rule...
                aggregate_field = self.aggregate_by['mysql_field']
            else:
                # otherwise append id to all foreign key fields to match db schema
                aggregate_field = self.aggregate_by['mysql_field'] + '_id'
            
            # TODO: figure out what this block is supposed to do
            # # budget_function or funding_type fields require join through budget_account model
            #             # ick! punting on this for now...
            #             if self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['FIELD_BUDGET_FUNCTION'] or self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['FIELD_FUNDING_TYPE']:
            #                 raise Exception('Currently not handling many-to-many joins on MySQL queries.')
            
            # # check to ensure we're not aggregating in an unsupported manner
            #             filter_fields = map(lambda x: x[0], self.filters)
            #             if FAADSSearch.FIELD_MAPPINGS['FIELD_BUDGET_FUNCTION'] in filter_fields or FAADSSearch.FIELD_MAPPINGS['FIELD_FUNDING_TYPE'] in filter_fields:
            #                 raise Exception('Currently not handling many-to-many joins on MySQL queries.')

            sql_parameters = [] # uses proper django.db SQL-escaping, in case we ever introduce nonnumeric database queries for some reason
            sql = " SELECT %s as field, sum(total_funding_amount) as value FROM faads_record WHERE " % aggregate_field
            
            for i,f in enumerate(self.filters):
                
                filter_field = f[0]
                filter_value = f[1]
                filter_conjunction = f[2]

                # add conjunction if this isn't the first part of the clause
                if i>0:
                    sql += " %s " % filter_conjunction['mysql']
                
                # deal with queries against foreign key fields (there are many of them!)
                if FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='fk':
                    successfully_mapped_fk_field = False
                    fk_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('mysql_fk_transformation', FAADSSearch.FIELD_MAPPINGS[filter_field].get('fk_transformation', lambda x: x))

                    if type(filter_value) not in (list, tuple):
                        filter_value = (filter_value,)
                    
                    fk_values = []
                    for value in filter_value:
                        fk_value = fk_transformation(value)
                        if fk_value is not None:
                            fk_values.append(str(fk_value))
                    
                    sql += ' ( %s_id IN (%s) ) ' % (filter_field, ','.join(fk_values))
                   
                # deal with range-type queries 
                elif FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='range':
                    # okay, I admit this may be too cute for its own good. the goal is just to build '( date>%s AND date<%s )' with options for leaving either off via None
                    clause_parts = []
                    range_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('mysql_range_transformation', lambda x: x) # putting this in place to allow for varying formatting of dates for solr & mysql
                    range_comparators = ('>=', '<=')
                    for j, range_specifier in enumerate(filter_value):
                        if range_specifier is not None:
                            clause_parts.append(FAADSSearch.FIELD_MAPPINGS[filter_field]['mysql_field'] + range_comparators[j] + "%s")
                            sql_parameters.append(range_transformation(range_specifier))
                    sql += ' ( %s ) ' % (' AND '.join(clause_parts))
                
                
            sql += " GROUP BY %s " % aggregate_field
            
            print sql
            print sql_parameters
            
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
    print FAADSSearch().use_cache(False).filter('cfda_program','20.205').aggregate('fiscal_year')
    # faads.search.FAADSSearch().filter('cfda_program','97.090').aggregate('fiscal_year')

    