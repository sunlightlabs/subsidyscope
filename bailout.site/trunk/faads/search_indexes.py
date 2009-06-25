import datetime
from haystack import indexes
from haystack.sites import site
from faads.models import Record


class RecordIndex(indexes.SearchIndex):
    
    type = 'site'
    
    cfda_program = indexes.CharField(model_attr='cfda_program')
    
    fiscal_year = indexes.IntegerField(model_attr='fiscal_year')
#    obligation_date = indexes.DateField(model_attr='obligation_action_date')
    
    non_federal_amount = indexes.IntegerField(model_attr='non_federal_funding_amount')
    federal_amount = indexes.IntegerField(model_attr='federal_funding_amount')
    total_amount = indexes.IntegerField(model_attr='total_funding_amount')
    
    description = indexes.CharField(document=True, model_attr='project_description')
    
    recipient = indexes.CharField(model_attr='recipient_name')
    recipient_location = indexes.CharField(model_attr='recipient_name')
    
    url = indexes.CharField(model_attr='url')
    
    def prepare_cfda_program(self, object):
        
        return '%s' % (object.cfda_program.program_number)
    
    def prepare_recipient_location(self, object):
        
        return '%s, %s' % (object.recipient_city_name, object.recipient_county_name)
    
    def prepare_federal_amount(self, object):
        
        return int(object.federal_funding_amount)
    
    def prepare_non_federal_amount(self, object):
        
        return int(object.non_federal_funding_amount)
    
    def prepare_total_amount(self, object):
        
        return int(object.total_funding_amount)
    
    
    
    def get_query_set(self):
        "Used when the entire index for model is updated."
        return Record.objects.all()


site.register(Record, RecordIndex)
