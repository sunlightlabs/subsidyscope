from django.core.management.base import NoArgsCommand
from faads.models import *
from faads.search import FAADSSearch

class Command(NoArgsCommand):
    help = "Generates report-creating SQL for FAADS for each sector"

    def handle_noargs(self, **options):        
        import imp
        from django.conf import settings
        sql_selection_clauses = []
        self.sector_sql_mapping = {}
        
        AGGREGATION_FIELD_1 = FAADSSearch.FIELD_MAPPINGS[FAADSSearch.DEFAULT_AGGREGATION_FIELD]['mysql_field']
        AGGREGATION_FIELD_2 = 'cfda_program_num';
        FIELD_TO_SUM = 'fed_funding_amount';
        
        for app in settings.INSTALLED_APPS:
            try:
                app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
            except AttributeError:
                continue

            try:
                imp.find_module('usaspending', app_path)
            except ImportError:
                continue

            m = __import__("%s.usaspending" % app)            
            f = getattr(getattr(m, 'usaspending', 'None'), 'faads', False)
            if f:
                print "%s:" % app
                print "SELECT %s, %s, SUM(%s) FROM %s WHERE %s GROUP BY %s, %s;" % (AGGREGATION_FIELD_1, AGGREGATION_FIELD_2, FIELD_TO_SUM, getattr(settings,'FAADS_IMPORT_MYSQL_SETTINGS',{}).get('source_table', 'faads_main_sf'), f()['sector'].values()[0].strip(), AGGREGATION_FIELD_1, AGGREGATION_FIELD_2)
                print ""