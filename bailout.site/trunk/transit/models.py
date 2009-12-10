from django.db import models

from geo.models import State

from django import forms

def get_mode(mode_abbrev):
    
    MODE_HASH = {'AG':'Automated Gateway', 'AR':'Alaska Railroad', 'MB':'Bus', 'CC':'Cable Car', 'CR':'Commuter Rail', 'DR':'Demand Response', 'FB':'Ferry Boat', 'HR':'Heavy Rail', 'IP':'Inclined Plane', 'JT':'Jitney', 'LR':'Light Rail', 'MO':'Monorail', 'PB':'Publico', 'TB':'Trolley Bus', 'TR': 'Aerial Tramway', 'VP':'Vanpool'}
    try:
        return MODE_HASH[mode_abbrev]
    except KeyError:
        return ""

class UrbanizedArea(models.Model):
    
    fta_id = models.IntegerField()
    
    fips_id = models.IntegerField(null=True)
    
    state = models.ManyToManyField(State, null=True)
    
    name = models.CharField(max_length=255, null=True, blank=True)    

    population = models.IntegerField(null=True)
    area = models.IntegerField(null=True)


class TransitSystem(models.Model):
    
    trs_id = models.IntegerField()
    
    state = models.ForeignKey(State, null=True)
    
    city = models.CharField(max_length=255, null=True, blank=True)
    
    urbanized_area =  models.ForeignKey(UrbanizedArea, null=True)
    
    name = models.CharField(max_length=255, null=True, blank=True)
   
    def total_expense_ridership_by_mode(self):
        operating = OperationStats.objects.filter(transit_system=self).order_by('mode')
        current_mode = operating[0].mode
        current_obj = operating[0]
        totals = []
        current_total = 0
        current_operating_total = 0
        current_capital_total = 0
        revenue_hours = 0
        revenue_miles = 0
        pmt = 0 #passenger miles travelled
        upt = 0 #unlinked passenger trips
        for o in operating:
            if o.mode != current_mode:
                totals.append(((current_obj.get_mode_display(), current_total, current_operating_total, current_capital_total), (revenue_hours, revenue_miles, pmt, upt, (current_operating_total/(pmt or 1)))))
                current_total = 0
                current_capital_total = 0
                current_operating_total = 0
                revenue_miles = 0
                revenue_hours = 0
                pmt = 0
                upt = 0
                current_mode = o.mode
                current_obj = o

            else:
                current_obj = o
                current_total += sum(filter(None, [o.capital_expense, o.operating_expense]))
                if o.fares: 
                    current_total -= o.fares
                    current_operating_total -= o.fares
                if o.operating_expense: current_operating_total += o.operating_expense
                if o.capital_expense: current_capital_total += o.capital_expense
                if o.vehicle_revenue_hours: revenue_hours += o.vehicle_revenue_hours
                if o.vehicle_revenue_miles: revenue_miles += o.vehicle_revenue_miles
                if o.passenger_miles_traveled: pmt += o.passenger_miles_traveled
                if o.unlinked_passenger_trips: upt += o.unlinked_passenger_trips

        return totals


class FundingStats(models.Model):
    
    transit_system = models.ForeignKey(TransitSystem)
    
    year = models.IntegerField()
    
    capital_federal = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    capital_state = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    capital_local = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    capital_other = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    operating_fares = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_federal = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_state = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_local = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_other = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_reconciliation = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    def total_funding(self, type=None):
        total = 0
        if type == 'capital': funding = [self.capital_federal, self.capital_state, self.capital_local, self.capital_other]
        elif type == 'operating': funding = [self.operating_federal, self.operating_state, self.operating_local, self.operating_other, self.operating_reconciliation]
        else: funding = [self.capital_federal, self.capital_state, self.capital_local, self.capital_other, self.operating_federal, self.operating_state, self.operating_local, self.operating_other, self.operating_reconciliation]

        for f in funding:
            if f:
                total += float(f)
        
        return total

    def total_funding_by_type(self, type):
        total = 0
        if type == 'federal': funding = [self.capital_federal, self.operating_federal]
        elif type == 'state': funding = [self.capital_state, self.operating_state]
        elif type == 'local': funding = [self.capital_local, self.operating_local]
        else: funding = [self.capital_other, self.operating_other]

        for f in funding:
            if f:
                total += float(f)

        return total
        

class OperationStats(models.Model):
    
    transit_system = models.ForeignKey(TransitSystem)
    
    year = models.IntegerField()
    
    MODE_AUTOMATED_GUIDEWAY = 'AG'
    MODE_ALASKA_RAILROAD = 'AR'
    MODE_BUS = 'MB'
    MODE_CABLE_CAR = 'CC'
    MODE_COMMUTER_RAIL = 'CR'
    MODE_DEMAND_RESPONSE = 'DR'
    MODE_FERRY_BOAT = 'FB'
    MODE_HEAVY_RAIL = 'HR'
    MODE_INCLINED_PLANE = 'IP'
    MODE_JITNEY = 'JT'
    MODE_LIGHT_RAIL = 'LR'
    MODE_MONORAIL = 'MO'
    MODE_PUBLICO = 'PB'
    MODE_TROLLEY = 'TB'
    MODE_TRAMWAY = 'TR'
    MODE_VANPOOL = 'VP'
    
    MODE_CHOICES = ((MODE_AUTOMATED_GUIDEWAY, 'Automated Guideway'),
    (MODE_ALASKA_RAILROAD, 'Alaska Railroad'),
    (MODE_BUS, 'Bus'),
    (MODE_CABLE_CAR, 'Cable Car'),
    (MODE_COMMUTER_RAIL, 'Commuter Rail'),
    (MODE_DEMAND_RESPONSE, 'Demand Response'),
    (MODE_FERRY_BOAT, 'Ferry Boat'),
    (MODE_HEAVY_RAIL, 'Heavy Rail'),
    (MODE_INCLINED_PLANE, 'Inclined Plane'),
    (MODE_JITNEY, 'Jitney'),
    (MODE_LIGHT_RAIL, 'Light Rail'),
    (MODE_MONORAIL, 'Monorail'),
    (MODE_PUBLICO, 'Publico'),
    (MODE_TROLLEY, 'Trolley Bus'),
    (MODE_TRAMWAY, 'Aerial Tramway'),
    (MODE_VANPOOL, 'Vanpool'))
    
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    
    operating_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    capital_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    fares = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    vehicle_revenue_miles = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    vehicle_revenue_hours = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    directional_route_miles = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    unlinked_passenger_trips = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    passenger_miles_traveled = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    
class TransitQuery(forms.Form):

    system_name = forms.CharField(max_length=200, required=False)
    modes_selected = forms.MultipleChoiceField(OperationStats.MODE_CHOICES, required=False)
    size_select = forms.ChoiceField((('on', 'Both'), ("rural", "Rural"),("urban", "Urban"),("both", "Both")),required=False)
    state_select = forms.ChoiceField([('','')] + [(st.abbreviation, st.name) for st in State.objects.all()], required=False)
    uza_select = forms.ChoiceField([('', '')] + [(u.id, u.name) for u in UrbanizedArea.objects.all()], required=False)
    ofppm_start = forms.DecimalField(required=False)
    ofppm_end = forms.DecimalField(required=False)
    cfppm_start = forms.DecimalField(required=False)
    cfppm_end = forms.DecimalField(required=False)
    ofpupt_start = forms.DecimalField(required=False)
    ofpupt_end = forms.DecimalField(required=False)
    cfpupt_start = forms.DecimalField(required=False)
    cfpupt_end = forms.DecimalField(required=False)
       
    
    
    
    
    
    
