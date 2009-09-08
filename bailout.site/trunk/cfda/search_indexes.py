import datetime
from haystack import indexes
from haystack.sites import site
from cfda.models import ProgramDescription


class ProgramDescriptionIndex(indexes.SearchIndex):
    
    type = 'cfda'
    
    text = indexes.CharField(document=True, use_template=True)
    
    title = indexes.CharField(model_attr='program_title')
    
    def prepare_cfda_program(self, object):
        
        return str(object.program_number)
        
    
    def get_queryset(self):
        "Used when the entire index for model is updated."
        
        # limit cfda indexing to programs that are included in a sector
        return ProgramDescription.objects.filter(sectors__isnull=False)
    

site.register(ProgramDescription, ProgramDescriptionIndex)