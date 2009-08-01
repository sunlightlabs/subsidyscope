import datetime
from haystack import indexes
from haystack.sites import site
from faads.models import Record


class RecordIndex(indexes.SearchIndex):
    
    type = 'faads'
    
    cfda_program = indexes.IntegerField(model_attr='cfda_program__id')
    
    budget_function = indexes.MultiValueField() # many-to-many via cfda program description
    funding_type = indexes.MultiValueField() # many-to-many via cfda program description
    
    sector = indexes.IntegerField() 
    subsector = indexes.IntegerField()
    
    action_type = indexes.IntegerField(model_attr='action_type__id')
    recipient_type = indexes.IntegerField(model_attr='recipient_type__id')
    record_type = indexes.IntegerField(model_attr='record_type__id')
    assistance_type = indexes.IntegerField(model_attr='assistance_type__id')
    
    fiscal_year = indexes.IntegerField(model_attr='fiscal_year')
    obligation_date = indexes.DateField(model_attr='obligation_action_date')
    
    non_federal_amount = indexes.IntegerField(model_attr='non_federal_funding_amount')
    federal_amount = indexes.IntegerField(model_attr='federal_funding_amount')
    total_amount = indexes.IntegerField(model_attr='total_funding_amount')
    
    text = indexes.CharField(document=True, model_attr='project_description')
    
    recipient = indexes.CharField(model_attr='recipient_name')
    recipient_county = indexes.IntegerField(model_attr='recipient_county__id')
    recipient_state = indexes.IntegerField(model_attr='recipient_state__id')
    
    principal_place_state = indexes.IntegerField(model_attr='principal_place_state__id')
    principal_place_county = indexes.IntegerField(model_attr='principal_place_county__id')
    
    
    def prepare_cfda_program(self, object):
        
        return '%s' % (object.cfda_program.id)
    
    def prepare_budget_function(self, object):
        
        budget_functions = []
        
        for budget_account in object.cfda_program.budget_accounts.all():
            budget_functions.append(budget_account.budget_function.id)
        
        return budget_functions
    
    def prepare_funding_type(self, object):
        
        funding_types = []
        
        for budget_account in object.cfda_program.budget_accounts.all():
            funding_types.append(budget_account.fund_code)
        
        return funding_types
    
    
    def prepare_action_type(self, object):
               
        if object.action_type != None:
            return object.action_type.id
        else:
            return None
    
    def prepare_recipient_type(self, object):
        
        if object.recipient_type != None:
            return object.recipient_type.id
        else:
            return None
    
    def prepare_record_type(self, object):
        
        if object.record_type != None:
            return object.record_type.id
        else:
            return None
    
    def prepare_assistance_type(self, object):
        
        if object.assistance_type != None:
            return object.assistance_type.id
        else:
            return None
    
    
    def prepare_fiscal_year(self, object):
        
        if object.fiscal_year != None:
            return int(object.fiscal_year)
        else:
            return None
        
    def prepare_obligation_date(self, object):
        
        if object.obligation_action_date != None:
            return object.obligation_action_date
        else:
            return None       
    
    def prepare_federal_amount(self, object):
        
        if object.federal_funding_amount:
            return int(object.federal_funding_amount)
        else:
            return None
    
    def prepare_non_federal_amount(self, object):
        
        if object.non_federal_funding_amount:
            return int(object.non_federal_funding_amount)
        else:
            return None
    
    def prepare_total_amount(self, object):
    
        if object.total_funding_amount:
            return int(object.total_funding_amount)
        else:
            return None
    

    def prepare_recipient(self, object):
        
        return '%s' % (object.recipient_name)
    
    
    
    def prepare_recipient_county(self, object):
        
        if object.recipient_county:
            return object.recipient_county.id
        else:
            return None
    
    def prepare_recipient_state(self, object):
        
        if object.recipient_state:
            return object.recipient_state.id
        else:
            return None
        
        
    def prepare_principal_place_county(self, object):
        
        if object.principal_place_county:
            return object.principal_place_county.id
        else:
            return None
    
    def prepare_principal_place_state(self, object):
        
        if object.principal_place_state:
            return object.principal_place_state.id
        else:
            return None
    
    
    def get_query_set(self):
        "Used when the entire index for model is updated."
        return Record.objects.all()


site.register(Record, RecordIndex)
