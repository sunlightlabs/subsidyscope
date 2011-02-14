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
            'mysql_field': 'cfda_program_id', 
            'solr_field': 'cfda_program', 
            'aggregate': True
        },
                
        'action_type': {
            'type': 'fk',
            'mysql_field': 'action_type_id', 
            'solr_field': 'action_type',
            'aggregate': True
        },
        
        'recipient_type': {
            'type': 'fk',
            'mysql_field': 'recipient_type_id', 
            'solr_field': 'recipient_type', 
            'aggregate': True
        },
        
        'record_type': {
            'type': 'fk',
            'mysql_field': 'record_type_id', 
            'solr_field': 'record_type', 
            'mysql_transformation': lambda x: self.RECORD_TYPE_FK_LOOKUP.get(int(x), None),
            'solr_transformation': lambda x: self.RECORD_TYPE_FK_LOOKUP.get(int(x), None),
            'aggregate': True
        },

        'assistance_type': {
            'type': 'fk',
            'mysql_field': 'assistance_type_id',
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
            'mysql_field': 'recipient_state_id', 
            'solr_field': 'recipient_state', 
            'aggregate': True
        },
        
        'recipient_county': {
            'type': 'fk',
            'mysql_field': 'recipient_county_id', 
            'solr_field': 'recipient_county', 
            'aggregate': True
        },
        
        'principal_place_state': {
            'type': 'fk',
            'mysql_field': 'principal_place_state_id', 
            'solr_field': 'principal_place_state', 
            'aggregate': True
        },
        
        'principal_place_county': {
            'type': 'fk',
            'mysql_field': 'principal_place_county_id', 
            'solr_field': 'principal_place_county', 
            'aggregate': True
        },
        
        'all_states': {
            'type': 'fk',
            'mysql_field': ('principal_place_state_id', 'recipient_state_id'),
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
        