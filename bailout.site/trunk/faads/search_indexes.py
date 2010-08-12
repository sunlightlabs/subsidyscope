import datetime
from haystack import indexes
from haystack.sites import site
from faads.models import Record


class RecordIndex(indexes.SearchIndex):
    
    type = 'faads'
    
    # sectors
    sectors = indexes.MultiValueField(null=False)
    subsectors = indexes.MultiValueField(null=True)

    # categories
    cfda_program = indexes.IntegerField(model_attr='cfda_program__id', null=True)    
    
    budget_function = indexes.MultiValueField(null=True) # many-to-many via cfda program description
    funding_type = indexes.MultiValueField(null=True) # many-to-many via cfda program description
    
    action_type = indexes.IntegerField(model_attr='action_type__id', null=True)
    recipient_type = indexes.IntegerField(model_attr='recipient_type__id', null=True)
    record_type = indexes.IntegerField(model_attr='record_type__id', null=True)
    assistance_type = indexes.IntegerField(model_attr='assistance_type__id', null=True)
    
    # chrono
    fiscal_year = indexes.IntegerField(model_attr='fiscal_year', null=True)
    obligation_date = indexes.DateField(model_attr='obligation_action_date', null=True)
    
    # dollars
    non_federal_amount = indexes.IntegerField(model_attr='non_federal_funding_amount', null=True)
    federal_amount = indexes.IntegerField(model_attr='federal_funding_amount', null=True)
    total_amount = indexes.IntegerField(model_attr='total_funding_amount', null=True)
    
    # text
    text = indexes.CharField(document=True, model_attr='project_description', null=True)    
    recipient = indexes.CharField(model_attr='recipient_name', null=True)

    # geo
    recipient_county = indexes.IntegerField(model_attr='recipient_county__id', null=True)
    recipient_state = indexes.IntegerField(model_attr='recipient_state__id', null=True)    
    principal_place_state = indexes.IntegerField(model_attr='principal_place_state__id', null=True)
    principal_place_county = indexes.IntegerField(model_attr='principal_place_county__id', null=True)
    
    # combo
    all_text = indexes.CharField(null=True)
    all_states = indexes.MultiValueField(null=True)
    
    def prepare_all_text(self, object):
        s = "%s %s" % (getattr(object, 'recipient_name', ''), getattr(object, 'project_description', ''))
        return len(s)>0 and s.strip() or None

    def prepare_all_states(self, object):
        r = []
        for f in ('principal_place_state', 'recipient_state'):
            s = getattr(object, f, None)
            if s is not None:
                i = getattr(s, 'id', None)
                if i is not None:
                    r.append(i)
                    
        return len(r)>0 and r or -1
        
    def prepare_cfda_program(self, object):        
        if object.cfda_program is None:
            return None
        return object.cfda_program.id
    
    
    def prepare_budget_function(self, object):
        
        if object.cfda_program is None:
            return None
        
        budget_functions = []
        
        for budget_account in object.cfda_program.budget_accounts.all():
	    if budget_account.budget_function != None:
                budget_functions.append(budget_account.budget_function.id)
        
        return budget_functions
    
    def prepare_funding_type(self, object):
        
        if object.cfda_program is None:
            return None
        
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
        
            
    def obligation_date(self, object):
        try:
            if object.effective_date.year > 1900:
                return object.effective_date
            else:
                return None
        except:
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
            return -1
    
    def prepare_recipient_state(self, object):
        
        if object.recipient_state:
            return object.recipient_state.id
        else:
            return -1
        
        
    def prepare_principal_place_county(self, object):
        
        if object.principal_place_county:
            return object.principal_place_county.id
        else:
            return -1
    
    def prepare_principal_place_state(self, object):
        
        if object.principal_place_state:
            return object.principal_place_state.id
        else:
            return -1
            
    def prepare_sectors(self, object):
        return map(lambda x: x.id, object.sectors.all())
    
    
    def get_queryset(self):
        "Used when the entire index for model is updated."
        return Record.objects.all()


site.register(Record, RecordIndex)
