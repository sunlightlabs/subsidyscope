from django.db import models

from geo.models import State

    
class UrbanizedArea(models.Model):
    
    fta_id = models.IntegerField()
    
    fips_id = models.IntegerField(null=True)
    
    state = models.ManyToManyField(State)
    
    name = models.CharField(max_length=255, null=True, blank=True)    

    population = models.IntegerField(null=True)
    area = models.IntegerField(null=True)


class TransitSystem(models.Model):
    
    trs_id = models.IntegerField()
    
    state = models.ForeignKey(State)
    
    city = models.CharField(max_length=255, null=True, blank=True)
    
    urbanized_area =  models.ForeignKey(UrbanizedArea)
    
    name = models.CharField(max_length=255, null=True, blank=True)
    

class FundingStats(models.Model):
    
    transit_system = models.ForeignKey(TransitSystem)
    
    year = models.IntegerField()
    
    capital_federal = models.IntegerField(null=True)
    capital_state = models.IntegerField(null=True)
    capital_local = models.IntegerField(null=True)
    capital_other = models.IntegerField(null=True)
    
    operating_fares = models.IntegerField(null=True)
    operating_federal = models.IntegerField(null=True)
    operating_state = models.IntegerField(null=True)
    operating_local = models.IntegerField(null=True)
    operating_other = models.IntegerField(null=True)
    operating_reconciliation = models.IntegerField(null=True)
    
    
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
    
    TOS_DIRECTLY_OPERATED = 'DO'
    TOS_PURCHASED = 'PT'
    
    TOS_CHOICES = ((TOS_DIRECTLY_OPERATED, 'Directly Operated'),
                   (TOS_PURCHASED, 'Purchased Transit'))
    
    
    type_of_service = models.CharField(max_length=2, choices=TOS_CHOICES)
    
    fares = models.IntegerField(null=True)
    
    vehicle_revenue_miles = models.IntegerField(null=True)
    vehicle_revenue_hours = models.IntegerField(null=True)
    directional_route_miles = models.IntegerField(null=True)
    unlinked_passenger_trips = models.IntegerField(null=True)
    passenger_miles_traveled = models.IntegerField(null=True)
    
    
    
    
    
    
    
    
    
    