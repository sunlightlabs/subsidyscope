from django.core.management.base import NoArgsCommand
from fpds.models import *
from fpds.search import FPDSSearch
import settings

class Command(NoArgsCommand):
    help = "Generates report-creating SQL for FPDS for each sector"

    def handle_noargs(self, **options):        
        import imp
        from django.conf import settings
        sql_selection_clauses = []
        self.sector_sql_mapping = {}
        
        AGGREGATION_FIELD = FPDSSearch.FIELD_MAPPINGS[FPDSSearch.DEFAULT_AGGREGATION_FIELD]['mysql_field']
        FIELD_TO_SUM = 'obligatedAmount'
        
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
            f = getattr(getattr(m, 'usaspending', 'None'), 'fpds', False)
            if f:
                print "%s:" % app
                r = f()
                if r is not None:
                    print "SELECT %s, SUM(%s) FROM %s WHERE %s GROUP BY %s;" % (AGGREGATION_FIELD, FIELD_TO_SUM, getattr(settings,'FPDS_IMPORT_MYSQL_SETTINGS',{}).get('source_table', 'fpds_award3_sf'), f()['sector'].values()[0].strip(), AGGREGATION_FIELD)
                else:
                    print "-- Not defined"
                print ""
                
