from django.db import models

from geo.models import State

from django import forms

from django.db.models import Avg, Sum

from decimal import *

from inflation.models import InflationIndex

#for inflation calculations
CURRENT_YEAR = 2008


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
   
module_constants = {'MODE_CONSTANTS': ((MODE_AUTOMATED_GUIDEWAY, 'Automated Guideway'),
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
    (MODE_VANPOOL, 'Vanpool'))}

class BigintField(models.Field):
    def db_type(self):
        return 'BIGINT(20)'

class UrbanizedArea(models.Model):
    
    class Meta:
        ordering = ["name"]
    
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
    
    name = models.CharField(max_length=255, null=True, blank=True
    )
class TransitSystemMode(models.Model):
    
    transit_system = models.ForeignKey(TransitSystem, null=False)
    
    state = models.ForeignKey(State, null=True)
    
    city = models.CharField(max_length=255, null=True, blank=True)
    
    urbanized_area =  models.ForeignKey(UrbanizedArea, null=True)
    
    name = models.CharField(max_length=255, null=True, blank=True)
    
    common_name = models.CharField(max_length=50, null=True, blank=True)
    
    MODE_CHOICES = module_constants['MODE_CONSTANTS']

    mode = models.CharField(max_length=2, choices=MODE_CHOICES)

    total_capital_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    total_operating_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    avg_capital_expenses = models.DecimalField(max_digits = 15, decimal_places=2, null=True, blank=True)

    avg_operating_expenses = models.DecimalField(max_digits = 15, decimal_places=2, null=True, blank=True)

    total_UPT = BigintField(null=True, blank=True)

    total_PMT = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    recovery_ratio = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    avg_operating_PMT = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    avg_capital_PMT = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    avg_operating_UPT = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    avg_capital_UPT = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    total_fares = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    avg_fares = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)



class TransitSystemModeManager(models.Manager):

    def match_common(self):
        data = open("transit/acronyms.txt")
        for line in data.xreadlines():
            params = line.split(",")
            try:
                system = TransitSystem.objects.get(trs_id=int(params[0]))
                sys = TransitSystemMode.objects.filter(transit_system=system)
                for s in sys:
                    s.common_name = params[1]
                    s.save()
            except TransitSystem.DoesNotExist:
                print "%s - %s doesn't exist" %(params[0], params[1])
        data.close()

    def process_raw(self):
       
        for old in TransitSystemMode.objects.all(): old.delete()
        
        systems = TransitSystem.objects.all()

        operations = OperationStats.objects.all()
                
        UPT =  None

        for sys in systems:
            
            modes = []

            for item in OperationStats.objects.filter(transit_system=sys).distinct().values('mode'):
                 modes.append(item['mode'])

            print modes
            for m in modes:
                
                mode_stats = operations.filter(transit_system=sys, mode=m)

                operating_expense = 0
                capital_expense = 0
                fares = 0
                op_yr_count = 0
                cap_yr_count = 0
                avg_operating = 0
                avg_capital  = 0
                cpi = InflationIndex.objects.get(name="CPI")
                 
                for stat in mode_stats:
                    if stat.operating_expense:
                        op_yr_count += 1
                        operating_expense += cpi.convertValue(stat.operating_expense, CURRENT_YEAR, stat.year)
                    if stat.capital_expense:
                        cap_yr_count += 1
                        capital_expense += cpi.convertValue(stat.capital_expense, CURRENT_YEAR, stat.year)
                    if stat.fares:
                        fares += cpi.convertValue(stat.fares, CURRENT_YEAR, stat.year)
                
                if op_yr_count > 0 : avg_operating = operating_expense/op_yr_count
                if cap_yr_count > 0: avg_capital = capital_expense/cap_yr_count
            
                UPT = mode_stats.aggregate(Sum('unlinked_passenger_trips'))['unlinked_passenger_trips__sum']

                PMT = mode_stats.aggregate(Sum('passenger_miles_traveled'))['passenger_miles_traveled__sum']

                if operating_expense and UPT: avg_op_UPT = operating_expense / UPT

                if capital_expense and UPT: avg_cap_UPT = capital_expense / UPT

                if operating_expense and PMT: avg_op_PMT = operating_expense / PMT

                if operating_expense and PMT: avg_cap_PMT = operating_expense / PMT

                if fares and operating_expense: rec_ratio = fares / operating_expense
                
                print "id: %s\n city: %s\n state: %s\n uza: %s\n name:%s\n mode:%s\n capital expenses:%s\n operating expenses:%s\n fares:%s\n UPT:%s\n PMT: %s\n  average operating dollars per UPT:%s\n average operating dollars per PMT:%s\n average capital dollars per UPT:%s\n average capital dollars per PMT: %s\n recovery ratio:%s\n======================" %(sys.trs_id, sys.city, sys.state.name, sys.urbanized_area, sys.name, m, capital_expense, operating_expense, fares, UPT, PMT, avg_op_UPT, avg_op_PMT, avg_cap_UPT, avg_cap_PMT, rec_ratio)

                new_tsm = TransitSystemMode(transit_system=sys)
                new_tsm.state = sys.state
                new_tsm.city=sys.city
                new_tsm.urbanized_area=sys.urbanized_area
                new_tsm.name=sys.name
                new_tsm.mode=m
                new_tsm.total_capital_expenses=capital_expense
                new_tsm.total_operating_expenses=operating_expense
                new_tsm.avg_capital_expenses=avg_capital
                new_tsm.avg_operating_expenses=avg_operating
                new_tsm.total_fares=fares
                new_tsm.total_UPT=UPT
                new_tsm.total_PMT=PMT
                new_tsm.avg_operating_UPT=avg_op_UPT
                new_tsm.avg_operating_PMT=avg_op_PMT
                new_tsm.avg_capital_UPT=avg_cap_UPT
                new_tsm.avg_capital_PMT=avg_cap_PMT
                new_tsm.recovery_ratio=rec_ratio
    
                new_tsm.save()

   
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

    MODE_CHOICES = module_constants['MODE_CONSTANTS']
    
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
    
    size_select = forms.ChoiceField((('50_100', '50,000 - 100,000'), ("100_1mil", "100,000 - 1 million"),("1_10mil", "1 million - 10 million"),("10_20mil", "10 million - 20 million"), ('all', 'All')),required=True)
    
    state_select = forms.ChoiceField([('','')] + [(st.abbreviation, st.name) for st in State.objects.all()], required=False)
    
    uza_select = forms.ChoiceField([('', '')] + [(u.id, u.name) for u in UrbanizedArea.objects.all()], required=False)
    
    metrics_selected = forms.MultipleChoiceField((("cap_expense", "Capital Expense"), ("op_expense", "Operating Expense"), ("PMT", "PMT"), ("UPT", "UPT"), ("recovery_ratio", "Recovery Ratio"), ("op_expense_pmt", "Operating Expense per PMT"), ("cap_expense_pmt", "Capital Expense per PMT"), ("cap_expense_upt", "Capital Expense per UPT"), ("op_expense_upt", "Capital Expense per UPT")), required=False)
    
    sort = forms.CharField(max_length=100, required=False)
    
    order = forms.CharField(max_length=20, required=False)
    
    
    
    
    
    
