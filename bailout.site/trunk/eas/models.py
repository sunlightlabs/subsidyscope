from django.db import models
from django.db.models import Q

class Airport(models.Model):
    
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    eas = models.BooleanField()
    
    NON_HUB = 0 
    LARGE_HUB = 1
    MEDIUM_HUB = 2
    SMALL_HUB = 3
    
    HUB_CHOICES = (
        (NON_HUB,'Non-Hub'),
        (LARGE_HUB,'Large Hub'),
        (MEDIUM_HUB,'Medium Hub'), 
        (SMALL_HUB,'Small Hub')
    )
    
    hub = models.IntegerField(choices=HUB_CHOICES)

    class Meta():
        ordering = ['location']


    def __unicode__(self):
        return '%s (%s)' % (self.location, self.code)


class Carrier(models.Model):
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    
    eas_participant = models.BooleanField()
    
    class Meta():
        ordering = ['name']
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)
    

class EASRoute(models.Model):
    
    carrier = models.ForeignKey(Carrier)
    
    eas_airport = models.ForeignKey(Airport, related_name='eas_airport')
    hub_airport = models.ManyToManyField(Airport, related_name='hub_airport')
    
    intermediate_airport = models.ManyToManyField(Airport, related_name='intermediate_airport', blank=True)
    
    eas_start_date = models.DateField(null=True, blank=True)
    eas_end_date = models.DateField(null=True, blank=True)
    
    eas_flight_subsidy = models.IntegerField(null=True, blank=True)
    eas_annual_subsidy = models.IntegerField(null=True, blank=True)
    
    eas_weekly_flights = models.IntegerField(null=True, blank=True)
    
    dot_order = models.CharField(max_length=255)
    dot_order_link = models.URLField()
    
        
    class Meta():
        ordering = ['dot_order']
    
    def __unicode__(self):
        return '%s (%s): %s' % (self.eas_airport.location, self.eas_airport.code, self.dot_order)
    
    def calculateSubsidy(self):
    
        route_list = []
        
        for hub in self.hub_airport.all():
            route_list.append(RouteStatistics.objects.filter(origin_airport=self.eas_airport, destination_airport=hub))
            route_list.append(RouteStatistics.objects.filter(destination_airport=self.eas_airport, origin_airport=hub))
        
        routes = set()
                
        for route in route_list:
            
            routes_tmp = routes
            data_tmp = set()
            
            for data in route:
                data_tmp.add(data)
            
            routes = routes_tmp.union(data_tmp)
                
        
        print len(routes)
        
    
class RouteStatistics(models.Model):
    
    carrier = models.ForeignKey(Carrier)
    
    origin_airport = models.ForeignKey(Airport, related_name='origin_airport')
    destination_airport = models.ForeignKey(Airport, related_name='destination_airport')
    
    distance = models.IntegerField()
    
    year = models.IntegerField()
    month = models.IntegerField()
    
    departures_scheduled = models.IntegerField()
    departures_performed = models.IntegerField()
    seats = models.IntegerField()
    payload = models.IntegerField()
    passengers = models.IntegerField()
    freight = models.IntegerField()
    mail = models.IntegerField()
    
    ramp_time = models.IntegerField()
    flight_time = models.IntegerField()
    
    