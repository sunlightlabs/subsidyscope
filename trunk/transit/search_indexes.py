
from haystack import indexes
from haystack.sites import site
from transit.models import TransitSystem, UrbanizedArea
from geo.models import State

class TransitSystemIndex(indexes.SearchIndex):

    type = "transitsystem"
    text = indexes.CharField(document=True, model_attr='name', null=True)

    def prepare_text(self, object):
        name = getattr(object, 'name')
        city  = getattr(object, 'city')
        abbrev = getattr(object, 'common_name')
        state = getattr(object, 'state')
        if state:
            state_name = state.name
            state_code = state.abbreviation
        else:
            state_name = ''
            state_code =''

        uza = getattr(object, 'urbanized_area')
        if uza: uza_name = uza.name
        else: uza_name = ''

        text = "%s %s %s %s %s %s" % (name, city, abbrev, state_name, state_code, uza_name)
        
        return text
       
    def get_queryset(self):
        return TransitSystem.objects.all()
        

site.register(TransitSystem, TransitSystemIndex) 
