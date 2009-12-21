from usaspending import *
from fpds.models import *

class FPDSSearch(USASpendingSearchBase):

    DJANGO_MODEL = FPDSRecord
    FIELD_TO_SUM = 'obligated_amount'
    DEFAULT_AGGREGATION_FIELD = 'fiscal_year'

    FIELD_MAPPINGS = {

        'fiscal_year': {
            'type': 'range',
            'mysql_field': 'fiscal_year',
            'solr_field': 'fiscal_year',
            'aggregate': True
        },

        'obligation_action_date': {
            'type': 'range',
            'mysql_field': 'effective_date',
            'solr_field': 'obligation_date',
            'solr_transformation': lambda x: str(x) + 'T00:00:00Z'
        },

        'naics_code': { 
            'type': 'fk',
            'solr_field': 'principal_naicscode',
            'mysql_field': 'principal_naicscode',
            'aggregate': True
        },

        'psc_code': {
            'type': 'fk',
            'solr_field': 'product_or_service_code',
            'mysql_field': 'product_or_service_code',
            'aggregate': True
        },

        'text': {
            'type': 'text',
            'solr_field': 'text',
        },

        'all_text': {
            'type': 'text',
            'solr_field': 'all_text'
        },

        'recipient': {
            'type': 'text',
            'solr_field': 'recipient'
        },

        'recipient_state': {
            'type': 'fk',
            'mysql_field': 'state', 
            'solr_field': 'recipient_state', 
            'aggregate': True
        },

        'principal_place_state': {
            'type': 'fk',
            'mysql_field': 'place_of_performance_state', 
            'solr_field': 'principal_place_state', 
            'aggregate': True
        },

        'all_states': {
            'type': 'fk',
            'mysql_field': ('place_of_performance_state', 'state'),
            'solr_field': 'all_states',
        },

        'obligated_amount': {
            'type': 'range',
            'mysql_field': 'obligated_amount',
            'solr_field': 'obligated_amount',        
        },
        
        'sectors': {
            'mysql_field': 'sector_hash',
            'solr_field': 'sectors'
        }
    }
    
    # TODO: update to use stats module
    # TODO: abstract out those 'fl' fields so they aren't hardcoded (if possible)
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
            query = self._build_solr_query()
            solr_result = solr.search(q=query, rows=self.SOLR_MAX_RECORDS, fl='obligated_amount,fiscal_year,principal_place_state')            
            
            # aggregate by state/year
            TO_PROCESS = { 'principal_place_state': result_state }

            for doc in solr_result.docs:
                if doc.has_key('obligated_amount') and doc.has_key('fiscal_year'):
                    for (key, result) in TO_PROCESS.items():                        
                        if doc.has_key(key):
                            if not result.has_key(doc[key]):
                                result[doc[key]] = {}
                            if not result[doc[key]].has_key(doc['fiscal_year']):
                                result[doc[key]][doc['fiscal_year']] = Decimal(0)
                            result[doc[key]][doc['fiscal_year']] += Decimal(str(doc['obligated_amount']))
                                    
        
        # handling key based aggregation with db group by/sum
        else:
            
            from django.db import connection
            cursor = connection.cursor()                
            
            sql, sql_parameters = self._build_mysql_query(aggregation_override='principal_place_state_id,fiscal_year')                                
                        
            cursor.execute(sql, sql_parameters)
            
            TO_PROCESS = { 0: result_state }
            for row in cursor.fetchall():
                for (index, result) in TO_PROCESS.items():
                    if not result.has_key(row[index]):
                        result[row[index]] = {}
                    if not result[row[index]].has_key(row[2]):
                        result[row[index]][row[2]] = Decimal(0)
                    result[row[index]][row[2]] += Decimal(str(row[3]))
                                  
    
        cache.set(self.get_query_cache_key(aggregate_by=CACHE_KEY_STATE), result_state)

        return { 'state': result_state }    
        

    
