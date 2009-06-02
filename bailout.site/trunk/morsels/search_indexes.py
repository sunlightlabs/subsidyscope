import datetime
from haystack import indexes
from haystack.sites import site
from morsels.models import Morsel, Page


class PageIndex(indexes.SearchIndex):
    
    type = 'site'
    
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    url = indexes.CharField(model_attr='url')
    
    def get_query_set(self):
        "Used when the entire index for model is updated."
        return Page.objects.all()


site.register(Page, PageIndex)
