from usaspending import *
from faads.models import *


        
class FAADSSearch(USASpendingSearchBase):
    
    DJANGO_MODEL = Record
    FIELD_TO_SUM = 'federal_funding_amount'
    DEFAULT_AGGREGATION_FIELD = 'fiscal_year'

    ACTION_TYPE_FK_LOOKUP = {}
    ASSISTANCE_TYPE_FK_LOOKUP = {}
    RECIPIENT_TYPE_FK_LOOKUP = {}
    RECORD_TYPE_FK_LOOKUP = {}
                        
            
    def __init__(self, *argv):
        USASpendingSearchBase.__init__(self, *argv)

        # preload fk lookup tables
        for a in ActionType.objects.all():
            self.ACTION_TYPE_FK_LOOKUP[a.code] = a.id

        for a in AssistanceType.objects.all():
            self.ASSISTANCE_TYPE_FK_LOOKUP[a.code] = a.id    
        
        for r in RecipientType.objects.all():
            self.RECIPIENT_TYPE_FK_LOOKUP[r.code] = r.id
        
        for r in RecordType.objects.all():
            self.RECORD_TYPE_FK_LOOKUP[r.code] = r.id
    
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
            'mysql_field': 'cfda_program', 
            'solr_field': 'cfda_program', 
            'aggregate': True
        },
                
        'action_type': {
            'type': 'fk',
            'mysql_field': 'action_type', 
            'solr_field': 'action_type',
            'aggregate': True
        },
        
        'recipient_type': {
            'type': 'fk',
            'mysql_field': 'recipient_type', 
            'solr_field': 'recipient_type', 
            'aggregate': True
        },
        
        'record_type': {
            'type': 'fk',
            'mysql_field': 'record_type', 
            'solr_field': 'record_type', 
            'mysql_transformation': lambda x: self.RECORD_TYPE_FK_LOOKUP.get(int(x), None),
            'solr_transformation': lambda x: self.RECORD_TYPE_FK_LOOKUP.get(int(x), None),
            'aggregate': True
        },

        'assistance_type': {
            'type': 'fk',
            'mysql_field': 'assistance_type',
            'solr_field': 'assistance_type',
            'aggregate': True
        },

        'fiscal_year': {
            'type': 'fk',
            'mysql_field': 'fiscal_year',
            'solr_field': 'fiscal_year',
            'aggregate': True
        },

        'obligation_action_date': {
            'type': 'range',
            'mysql_field': 'obligation_action_date',
            'solr_field': 'obligation_date',
            'solr_transformation': lambda x: str(x) + 'T00:00:00Z'
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
            'solr_field': 'total_amount',        
        },
        
        'all_text': {
            'type': 'text',
            'solr_field': 'all_text',
        },
        
        # duplicate of preceding
        'text': {
            'type': 'text',
            'solr_field': 'all_text',
        },
        
        'recipient': {
            'type': 'text',
            'solr_field': 'recipient'
        },
        
        'recipient_state': {
            'type': 'fk',
            'mysql_field': 'recipient_state', 
            'solr_field': 'recipient_state', 
            'aggregate': True
        },
        
        'recipient_county': {
            'type': 'fk',
            'mysql_field': 'recipient_county', 
            'solr_field': 'recipient_county', 
            'aggregate': True
        },
        
        'principal_place_state': {
            'type': 'fk',
            'mysql_field': 'principal_place_state', 
            'solr_field': 'principal_place_state', 
            'aggregate': True
        },
        
        'principal_place_county': {
            'type': 'fk',
            'mysql_field': 'principal_place_county', 
            'solr_field': 'principal_place_county', 
            'aggregate': True
        },
        
        'all_states': {
            'type': 'fk',
            'mysql_field': ('principal_place_state', 'recipient_state'),
            'solr_field': 'all_states',
        },
        
        'sectors': {
            'mysql_field': 'sector_hash',
            'solr_field': 'sectors'
        }
    }
    
    
    def get_summary_statistics(self):
        """ Generate summary statistics by-program and by-state for the specified query """
        CACHE_KEY_STATE = 'summary_statistics_state'
        CACHE_KEY_PROGRAM = 'summary_statistics_program'

        result_state = {}
        result_program = {}
        
        # check for cached result
        if self.cache:
            cached_result_state = cache.get(self.get_query_cache_key(aggregate_by=CACHE_KEY_STATE))
            cached_result_program = cache.get(self.get_query_cache_key(aggregate_by=CACHE_KEY_PROGRAM))            
            if cached_result_state is not None and cached_result_program is not None:
                return {'program': cached_result_program, 'state': cached_result_state}
    
        # handling full-text aggregation with solr/python hack
        if self.use_solr:
            
            solr = Solr(settings.HAYSTACK_SOLR_URL)

            if self.SOLR_USE_STATS_MODULE:
                result_state_temp = {}
                result_program_temp = {}
                
                year_range = self.get_year_range()
                for year in year_range:
                    result_state_temp[year] = self.filter('fiscal_year', str(year)).aggregate('principal_place_state')                
                    result_program_temp[year] = self.filter('fiscal_year', str(year)).aggregate('cfda_program')
                
                # invert the array
                for year in result_state_temp:
                    for state in result_state_temp[year]:
                        if not result_state.has_key(state):
                            result_state[state] = {}
                        result_state[state][year] = result_state_temp[year][state]
                        
                    for program in result_program_temp[year]:
                        if not result_program.has_key(program):
                            result_program[program] = {}
                        result_program[program][year] = result_program_temp[year][program]
                
            else:

                query = self._build_solr_query()
                solr_result = solr.search(q=query, rows=FAADSSearch.SOLR_MAX_RECORDS, fl='%s,fiscal_year,principal_place_state,cfda_program' % self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field'])            
            
                # aggregate by state/year, program/year
                TO_PROCESS = { 'principal_place_state': result_state, 'cfda_program': result_program }

                for doc in solr_result.docs:
                    if doc.has_key(self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']) and doc.has_key('fiscal_year'):
                        for (key, result) in TO_PROCESS.items():                        
                            if doc.has_key(key):
                                if not result.has_key(doc[key]):
                                    result[doc[key]] = {}
                                if not result[doc[key]].has_key(doc['fiscal_year']):
                                    result[doc[key]][doc['fiscal_year']] = Decimal(0)
                                result[doc[key]][doc['fiscal_year']] += Decimal(str(doc[self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']]))
                                    
        
        # handling key based aggregation with db group by/sum
        else:
            
            from django.db import connection
            cursor = connection.cursor()                
            
            sql, sql_parameters = self._build_mysql_query(aggregation_override='principal_place_state_id,cfda_program_id,fiscal_year')                                
                        
            cursor.execute(sql, sql_parameters)
            
            TO_PROCESS = { 0: result_state, 1: result_program }
            for row in cursor.fetchall():
                for (index, result) in TO_PROCESS.items():
                    if not result.has_key(row[index]):
                        result[row[index]] = {}
                    if not result[row[index]].has_key(row[2]):
                        result[row[index]][row[2]] = Decimal(0)
                    result[row[index]][row[2]] += Decimal(str(row[3]))
                                          
    
        cache.set(self.get_query_cache_key(aggregate_by=CACHE_KEY_STATE), result_state)
        cache.set(self.get_query_cache_key(aggregate_by=CACHE_KEY_PROGRAM), result_program)

        return {'program': result_program, 'state': result_state}
        

    
# from pysolr import Solr
# from django.db import models
# from decimal import Decimal
# from faads.models import *
# from haystack.query import SearchQuerySet
# import cfda.models
# import django.db.models.fields
# from django.core.cache import cache
# from hashlib import md5 
# import settings
# import zlib
# import base64
# import urllib
# import pickle    
#     
#     
# class FAADSSearch():
#     
#     SOLR_MAX_RECORDS = 1000000
#     
#     FIELD_MAPPINGS = {
# 
#         'budget_function': {
#             'type': None, # NOT YET IMPLEMENTED
#             'mysql_field': 'budget_function',
#             'solr_field': 'budget_function',
#         },
#         
#         'funding_type': {
#             'type': None, # NOT YET IMPLEMENTED IN MODEL            
#             'mysql_field': 'funding_type',
#             'solr_field': 'funding_type'
#         },
#          
#         'cfda_program': {
#             'type': 'fk',
#             'mysql_field': 'cfda_program', 
#             'solr_field': 'cfda_program', 
#             'aggregate': True
#         },
#                 
#         'action_type': {
#             'type': 'fk',
#             'mysql_field': 'action_type', 
#             'solr_field': 'action_type',
#             'aggregate': True
#         },
#         
#         'recipient_type': {
#             'type': 'fk',
#             'mysql_field': 'recipient_type', 
#             'solr_field': 'recipient_type', 
#             'aggregate': True
#         },
#         
#         'record_type': {
#             'type': 'fk',
#             'mysql_field': 'record_type', 
#             'solr_field': 'record_type', 
#             'mysql_transformation': lambda x: RECORD_TYPE_FK_LOOKUP.get(int(x), None),
#             'solr_transformation': lambda x: RECORD_TYPE_FK_LOOKUP.get(int(x), None),
#             'aggregate': True
#         },
# 
#         'assistance_type': {
#             'type': 'fk',
#             'mysql_field': 'assistance_type',
#             'solr_field': 'assistance_type',
#             'aggregate': True
#         },
# 
#         'fiscal_year': {
#             'type': 'range',
#             'mysql_field': 'fiscal_year',
#             'solr_field': 'fiscal_year',
#             'aggregate': True
#         },
# 
#         'obligation_action_date': {
#             'type': 'range',
#             'mysql_field': 'obligation_action_date',
#             'solr_field': 'obligation_date',
#             'solr_transformation': lambda x: str(x) + 'T00:00:00Z'
#         },
# 
#         'non_federal_funding_amount': {
#             'type': 'range',
#             'mysql_field': 'non_federal_funding_amount',
#             'solr_field': 'non_federal_amount'
#         },
#         
#         'federal_funding_amount': {
#             'type': 'range',
#             'mysql_field': 'federal_funding_amount',
#             'solr_field': 'federal_amount'            
#         },
#         
#         'total_funding_amount': {
#             'type': 'range',
#             'mysql_field': 'total_funding_amount',
#             'solr_field': 'total_amount',        
#         },
#         
#         'all_text': {
#             'type': 'text',
#             'solr_field': 'all_text',
#         },
#         
#         # duplicate of preceding
#         'text': {
#             'type': 'text',
#             'solr_field': 'all_text',
#         },
#         
#         'recipient': {
#             'type': 'text',
#             'solr_field': 'recipient'
#         },
#         
#         'recipient_state': {
#             'type': 'fk',
#             'mysql_field': 'recipient_state', 
#             'solr_field': 'recipient_state', 
#             'aggregate': True
#         },
#         
#         'recipient_county': {
#             'type': 'fk',
#             'mysql_field': 'recipient_county', 
#             'solr_field': 'recipient_county', 
#             'aggregate': True
#         },
#         
#         'principal_place_state': {
#             'type': 'fk',
#             'mysql_field': 'principal_place_state', 
#             'solr_field': 'principal_place_state', 
#             'aggregate': True
#         },
#         
#         'principal_place_county': {
#             'type': 'fk',
#             'mysql_field': 'principal_place_county', 
#             'solr_field': 'principal_place_county', 
#             'aggregate': True
#         },
#         
#         'all_states': {
#             'type': 'fk',
#             'mysql_field': ('principal_place_state', 'recipient_state'),
#             'solr_field': 'all_states',
#         },
#     }
#     
#     FIELD_TO_SUM = FIELD_MAPPINGS['federal_funding_amount']
#     
#     CONJUNCTION_AND = {'solr': 'AND', 'mysql': 'AND'}
#     CONJUNCTION_OR = {'solr': 'OR', 'mysql': 'OR'}
#     
#     
#     def __init__(self, query_string=None):
#         
#         self.filters = []
#          
#         self.aggregate_by = None
#         self.use_solr = False
#         self.order_by = None
#         self.cache = True
#         self.SearchQuerySet = None
#         
#         self.field_objects = {}
#         for field in Record._meta.fields:
#             self.field_objects[field.name] = field
#             
# 
#     def __len__(self):
#         return self.count()
# 
#     
#     # clone function to enable chainable filtering (blatantly stolen from haystack (which presumably stole it from Django))
#     def _clone(self, klass=None):
# 
#         if klass is None:
#             klass = self.__class__
# 
#         clone = klass()
#         clone.aggregate_by = self.aggregate_by
#         clone.use_solr = self.use_solr
#         clone.order_by = self.order_by
#         clone.cache = self.cache
#         clone.field_objects = self.field_objects.copy()
#         clone.filters = self.filters[:]
#         if self.SearchQuerySet is not None:
#             clone.SearchQuerySet = self.SearchQuerySet._clone()
#         
#         return clone
#         
#     def use_cache(self, u=True):
#         clone = self._clone()
#         clone.cache = u
#         return clone
#             
#     def get_query_cache_key(self, aggregate_by=''):
#         fs = "%s;" % self.__module__
#         for i,f in enumerate(self.filters):
#             fs += "%d:{%s|%s|%s}" % (i, str(f[0]), str(f[1]), str(f[2]))
#         fs += aggregate_by
#         h = md5(fs).hexdigest() # avoid key length problems
#         return str(h)
#                     
#     def filter(self, filter_by, filter_value, filter_conjunction=CONJUNCTION_AND):  
# 
#         field_lookup = FAADSSearch.FIELD_MAPPINGS.get(filter_by,None)
#         if field_lookup is None:
#             raise Exception("'%s' is not a valid filter field" % filter_by)
#         elif len(filter_value)==0:
#             if field_lookup['type']=='fk':
#                 filter_value = (-1,) # plan to return an empty result set if this criteria is an empty query on an FK field
#             else:
#                 raise Exception("Cannot process a zero-length value for filter '%s'" % filter_by)            
#         elif field_lookup['type']=='range' and ((type(filter_value) not in (list, tuple)) or (len(filter_value)!=2)):
#             raise Exception("'%s' is a ranged field. Please pass a tuple or list of length 2 (None==wildcard)")
# 
#         clone = self._clone()
# 
#         # invalidate existing queryset, if any
#         self.SearchQuerySet = None        
# 
#         clone.filters.append( (filter_by, filter_value, filter_conjunction) )
#         if not clone.use_solr and (clone.FIELD_MAPPINGS[filter_by]['type']=='text'):
#             clone.use_solr = True
#             
#         return clone
#     
#     def _build_solr_query(self):
#         query = ''
#         for i,f in enumerate(self.filters):
#             filter_field = f[0]
#             filter_value = f[1]
#             filter_conjunction = f[2]
#             
#             if i>0:
#                 query += " %s " % filter_conjunction['solr'] 
# 
# 
#             # deal with queries against foreign key fields
#             if FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='fk':
#                 fk_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x)
# 
#                 if type(filter_value) not in (list, tuple):
#                     filter_value = (filter_value,)
#                 
#                 fk_values = []
#                 for value in filter_value:
#                     fk_value = fk_transformation(value)                    
#                     if fk_value is not None:
#                         fk_values.append(str(fk_value))
#                 
#                 if len(fk_values):                
#                     query += '(%s:(%s))' % (FAADSSearch.FIELD_MAPPINGS[filter_field]['solr_field'], ' OR '.join(fk_values))
# 
# 
#             # deal with range-type queries 
#             elif FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='range':
#                 clause_parts = []
#                 range_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x) # putting this in place to allow for varying formatting of dates for solr & mysql
#                 
#                 for range_specifier in filter_value:
#                     if range_specifier is None:
#                         clause_parts.append('*')
#                     else:
#                         clause_parts.append(str(range_transformation(range_specifier)))
#                         
#                 query += '(%s:[%s])' % (FAADSSearch.FIELD_MAPPINGS[filter_field]['solr_field'], ' TO '.join(clause_parts))
# 
#             # text queries (all of which get sent to solr)
#             elif FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='text':
#                 query += '(%s:"%s")' % (FAADSSearch.FIELD_MAPPINGS[filter_field]['solr_field'], filter_value)
# 
#         return query
# 
#         
#     def _build_mysql_query(self, aggregation_override=False):
#         
#         if not aggregation_override:      
#             if self.aggregate_by is None:
#                 raise Exception("Must specify an aggregate field prior to MySQL query construction")
# 
#             if self.aggregate_by == FAADSSearch.FIELD_MAPPINGS['fiscal_year']:
#                 # an exception to the field naming rule...
#                 aggregate_field = self.aggregate_by['mysql_field']
#             else:
#                 # otherwise append id to all foreign key fields to match db schema
#                 aggregate_field = self.aggregate_by['mysql_field'] + '_id'
# 
#         sql_parameters = [] # uses proper django.db SQL-escaping, in case we ever introduce nonnumeric database queries for some reason
#         
#         sql = " SELECT %s as field, sum(%s) as value FROM faads_record " % (self.FIELD_TO_SUM['mysql_field'], aggregation_override and aggregation_override or aggregate_field)
#         
#         if len(self.filters) > 0:
#             
#             sql += " WHERE "
#         
#             for i,f in enumerate(self.filters):
#                 
#                 filter_field = f[0]
#                 filter_value = f[1]
#                 filter_conjunction = f[2]
#     
#                 # add conjunction if this isn't the first part of the clause
#                 if i>0:
#                     sql += " %s " % filter_conjunction['mysql']
#                 
#                 # deal with queries against foreign key fields (there are many of them!)
#                 if FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='fk':
#                     
#                     # build list of the foreign keys
#                     fk_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('mysql_transformation', lambda x: x)
#     
#                     if type(filter_value) not in (list, tuple):
#                         filter_value = (filter_value,)
#                     
#                     fk_values = []
#                     for value in filter_value:
#                         fk_value = fk_transformation(value)
#                         if fk_value is not None:
#                             fk_values.append(str(fk_value))
#                     
#                     # is this query examining a field that's an aggregation of two fields in solr? if so, it doesn't exist in mysql. build
#                     # an OR clause instead
#                     mysql_field = FAADSSearch.FIELD_MAPPINGS[filter_field]['mysql_field']               
#                     if type(mysql_field) not in (list, tuple):
#                         mysql_field = (mysql_field,)            
#                     
#                     clauses = []
#                     for mf in mysql_field:
#                         clauses.append(' (%s_id IN (%s)) ' % (mf, ','.join(fk_values)))                        
#                     
#                     sql += '(' + ' OR '.join(clauses) + ')'
#                    
#                 # deal with range-type queries 
#                 elif FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='range':
#                     # okay, I admit this may be too cute for its own good. the goal is just to build '( date>%s AND date<%s )' with options for leaving either off via None
#                     clause_parts = []
#                     range_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('mysql_transformation', lambda x: x) # putting this in place to allow for varying formatting of dates for solr & mysql
#                     range_comparators = ('>=', '<=')
#                     for j, range_specifier in enumerate(filter_value):
#                         if range_specifier is not None:
#                             clause_parts.append(FAADSSearch.FIELD_MAPPINGS[filter_field]['mysql_field'] + range_comparators[j] + "%s")
#                             sql_parameters.append(range_transformation(range_specifier))
#                     sql += ' ( %s ) ' % (' AND '.join(clause_parts))
# 
#         sql += " GROUP BY %s " % (aggregation_override and aggregation_override or aggregate_field)
# 
#         return (sql, sql_parameters)
#         
#     
#     def aggregate(self, aggregate_by):
#         
#         # ensure that aggregation is to be performed along an acceptable dimension
#         self.aggregate_by = self.FIELD_MAPPINGS.get(aggregate_by, None)
#         if self.aggregate_by is None:
#             raise Exception("Cannot aggregate by %s - not a valid field" % aggregate_by)
#         elif not self.aggregate_by.get('aggregate', False):
#             raise Exception("Cannot aggregate by %s - incompatible field type" % aggregate_by)
#         
#         # check for cached result
#         if self.cache:
#             cached_result = cache.get(self.get_query_cache_key(aggregate_by=aggregate_by))            
#             if cached_result is not None:
#                 return cached_result
#     
#         # handling full-text aggregation with solr/python hack
#         if self.use_solr:                        
#             
#             solr = Solr(settings.HAYSTACK_SOLR_URL)
#             query = self._build_solr_query()
#             solr_result = solr.search(q=query, rows=FAADSSearch.SOLR_MAX_RECORDS, fl='%s,%s' % (self.FIELD_TO_SUM['solr_field'], self.aggregate_by['solr_field']))            
#             result = {}
#             
#             # aggregation
#             for doc in solr_result.docs:
#                 if doc.has_key(self.aggregate_by['solr_field']) and doc.has_key(self.FIELD_TO_SUM['solr_field']):
#                     key = int(doc[self.aggregate_by['solr_field']])                
#                     if not result.has_key(key):
#                         result[key] = Decimal(0)                
#                     result[key] += Decimal(str(doc[self.FIELD_TO_SUM['solr_field']])) 
#                 
#             
#         
#         # handling key based aggregation with db group by/sum
#         else:
#             
#             from django.db import connection
#             cursor = connection.cursor()                
#             
#             sql, sql_parameters = self._build_mysql_query()                                
#                         
#             cursor.execute(sql, sql_parameters)
#             
#             result = {}            
#             for row in cursor.fetchall():
#                 result[row[0]] = row[1]
#     
#         cache.set(self.get_query_cache_key(aggregate_by=aggregate_by), result)
#     
#         return result    
#     
#     def get_summary_statistics(self):
#         """ Generate summary statistics by-program and by-state for the specified query """
#         CACHE_KEY_STATE = 'summary_statistics_state'
#         CACHE_KEY_PROGRAM = 'summary_statistics_program'
# 
#         result_state = {}
#         result_program = {}
#         
#         # check for cached result
#         if self.cache:
#             cached_result_state = cache.get(self.get_query_cache_key(aggregate_by=CACHE_KEY_STATE))
#             cached_result_program = cache.get(self.get_query_cache_key(aggregate_by=CACHE_KEY_PROGRAM))            
#             if cached_result_state is not None and cached_result_program is not None:
#                 return {'program': cached_result_program, 'state': cached_result_state}
#     
#         # handling full-text aggregation with solr/python hack
#         if self.use_solr:                        
#             
#             solr = Solr(settings.HAYSTACK_SOLR_URL)
#             query = self._build_solr_query()
#             solr_result = solr.search(q=query, rows=FAADSSearch.SOLR_MAX_RECORDS, fl='%s,fiscal_year,principal_place_state,cfda_program' % self.FIELD_TO_SUM['solr_field'])            
#             
#             # aggregate by state/year, program/year
#             TO_PROCESS = { 'principal_place_state': result_state, 'cfda_program': result_program }
# 
#             for doc in solr_result.docs:
#                 if doc.has_key(self.FIELD_TO_SUM['solr_field']) and doc.has_key('fiscal_year'):
#                     for (key, result) in TO_PROCESS.items():                        
#                         if doc.has_key(key):
#                             if not result.has_key(doc[key]):
#                                 result[doc[key]] = {}
#                             if not result[doc[key]].has_key(doc['fiscal_year']):
#                                 result[doc[key]][doc['fiscal_year']] = Decimal(0)
#                             result[doc[key]][doc['fiscal_year']] += Decimal(str(doc[self.FIELD_TO_SUM['solr_field']]))
#                                     
#         
#         # handling key based aggregation with db group by/sum
#         else:
#             
#             from django.db import connection
#             cursor = connection.cursor()                
#             
#             sql, sql_parameters = self._build_mysql_query(aggregation_override='principal_place_state_id,cfda_program_id,fiscal_year')                                
#                         
#             cursor.execute(sql, sql_parameters)
#             
#             TO_PROCESS = { 0: result_state, 1: result_program }
#             for row in cursor.fetchall():
#                 for (index, result) in TO_PROCESS.items():
#                     if not result.has_key(row[index]):
#                         result[row[index]] = {}
#                     if not result[row[index]].has_key(row[2]):
#                         result[row[index]][row[2]] = Decimal(0)
#                     result[row[index]][row[2]] += Decimal(str(row[3]))
#                                   
#     
#         cache.set(self.get_query_cache_key(aggregate_by=CACHE_KEY_STATE), result_state)
#         cache.set(self.get_query_cache_key(aggregate_by=CACHE_KEY_PROGRAM), result_program)
# 
#         return {'program': result_program, 'state': result_state}
# 
#     
#     def get_year_range(self):
#         """ return the range of years present in the database (useful for generating the summary statistics table) """
#         YEAR_RANGE_CACHE_KEY = 'faads.search.get_year_range'
#         
#         cached_year_range = cache.get(YEAR_RANGE_CACHE_KEY)
#         if cached_year_range is not None:
#             return cached_year_range        
#         
#         from django.db import connection
#         cursor = connection.cursor()
#         cursor.execute('SELECT MIN(fiscal_year), MAX(fiscal_year) FROM faads_record LIMIT 1')
#         for row in cursor.fetchall():
#             r = range(int(row[0]), int(row[1]))
# 
#         cache.set(YEAR_RANGE_CACHE_KEY,r)
#         
#         return r
# 
#     
#     def _run_solr_query_if_necessary(self):
#         # run raw solr query
#         if self.SearchQuerySet is None:
#             query = self._build_solr_query()            
#             self.SearchQuerySet = SearchQuerySetWrapper().raw_search(query, rows=50)
#     
#     def results(self):
#         self._run_solr_query_if_necessary()
#         return self.SearchQuerySet
#                     
#     def count(self):
#         self._run_solr_query_if_necessary()
#         return self.SearchQuerySet.__len__()
# 
#     def get_haystack_queryset(self, order_by='-obligation_date'):
#         """ Returns a Haystack QuerySet object with the appropriate filters """
# 
#         # order AND filters first, then OR filters
#         and_filters = {}
#         or_filters = {}
#         for f in self.filters:
#             filter_field = f[0]
#             filter_value = f[1]
#             filter_conjunction = f[2]
# 
#             # select appropriate target list
#             target_filter_list = and_filters
#             if f[2]==FAADSSearch.CONJUNCTION_OR:
#                 target_filter_list = or_filters
#                         
#             # deal with fk
#             if FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='fk':
#         
#                 field_operator = filter_field + '__in'
#                 fk_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x)
#         
#                 if type(filter_value) not in (list, tuple):
#                     filter_value = (filter_value,)
#         
#                 fk_values = []
#                 for value in filter_value:
#                     fk_value = fk_transformation(value)
#                     if fk_value is not None:
#                         fk_values.append(str(fk_value))                                        
# 
#                 target_filter_list[field_operator] = fk_values                
#     
#             # deal with range
#             if FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='range':
#                 clause_parts = []
#                 range_transformation = FAADSSearch.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x) # putting this in place
#                 filter_operators = ('__gte', '__lte')
#                 
#                 for i, range_specifier in enumerate(filter_value):
#                     if range_specifier is not None:
#                         target_filter_list[FAADSSearch.FIELD_MAPPINGS[filter_field]['solr_field'] + filter_operators[i]] = range_specifier                
# 
#             # deal with text
#             elif FAADSSearch.FIELD_MAPPINGS[filter_field]['type']=='text':
#                 target_filter_list[filter_field] = filter_value
#             
#     
#         s = SearchQuerySet().models(Record)
#         
#         if len(or_filters):
#             s = s.filter_or(**or_filters)
# 
#         if len(and_filters):
#             s = s.filter_and(**and_filters)
#         
#         s = s.order_by(order_by)
#         
#         return s
#         
# 
# 
#     
# class SearchQuerySetWrapper(SearchQuerySet):
#     """ overrides the __len__() function to provide a correct hit count for raw searches """
#     def __init__(self, *args, **kwargs):
#         super(SearchQuerySetWrapper, self).__init__(*args, **kwargs)    
# 
#     def count(self):
#         try:
#             return int(self.query._hit_count)
#         except Exception, e:
#             return 0
#         
#     