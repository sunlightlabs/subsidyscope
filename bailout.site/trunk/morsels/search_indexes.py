import datetime
from haystack import indexes
from haystack.sites import site
from morsels.models import Morsel, Page


class PageIndex(indexes.SearchIndex):
    
    type = 'site'
    
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    url = indexes.CharField(model_attr='url')
    
    def get_queryset(self):
        "Used when the entire index for model is updated."
        return Page.objects.all()
    
    def should_update(self):
        "Disable update on save - re-index lag is causing problems with timeouts"
        return False


site.register(Page, PageIndex)
