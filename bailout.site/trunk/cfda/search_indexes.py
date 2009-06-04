import datetime
from haystack import indexes
from haystack.sites import site
from cfda.models import ProgramDescription


class ProgramDescriptionIndex(indexes.SearchIndex):
    
    type = 'cfda'
    
    text = indexes.CharField(document=True, use_template=True)
    
    title = indexes.CharField(model_attr='program_title')
    description = indexes.CharField(model_attr='program_note')
    
    def get_query_set(self):
        "Used when the entire index for model is updated."
        return ProgramDescription.objects.all()
    

#site.register(ProgramDescription, ProgramDescriptionIndex)