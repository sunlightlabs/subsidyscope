from eas.models import *
from django.contrib import admin


class EASRouteInline(admin.TabularInline):
    model = EASRoute

    fk_name = 'eas_airport'
    
    
class AirportAdmin(admin.ModelAdmin):
   
    inlines = [EASRouteInline]
    
    search_fields = ['name', 'location','code']
    


admin.site.register(EASRoute)
admin.site.register(Airport, AirportAdmin)
