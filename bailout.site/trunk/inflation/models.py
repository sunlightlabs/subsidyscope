from django.db import models


"""
Example:
    
from inflation.models import InflationIndex

cpi = InflationIndex.objects.get(name="CPI")

cpi.convertValue(100, 2008, 1990)  # converts from 1990 dollars to 2008 dollars
>> Decimal("164.72")

table = cpi.getConversionTable(2008, 1980, 2008) # builds table for converting values into 2008 dollars

new_value = old_value * table[1985]  # converts old value in 1985 dollars into 2008 dollars

"""

class InflationIndex(models.Model):
    
    name = models.CharField(max_length=25)
    
    description = models.TextField()
    
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    
    
    def getConversionTable(self, target_year, conversion_start_year=-1, conversion_end_year=-1):
        
        if conversion_start_year == -1:
            conversion_start_year = self.start_year
        if conversion_end_year == -1:
            conversion_end_year = self.end_year
        
        target = IndexDataPoint.objects.get(index=self, year=target_year)
            
        index_data = IndexDataPoint.objects.filter(index=self, year__gte=conversion_start_year, year__lte=conversion_end_year)

        conversation_table = {}

        for item in index_data:
        
            conversation_table[item.year] = target.value / item.value 
            
        return conversation_table 
    
    
    def convertValue(self, value, target_year, origin_year):
        
        target = IndexDataPoint.objects.get(index=self, year=target_year)
        
        origin = IndexDataPoint.objects.get(index=self, year=origin_year)
        
        return value * (target.value / origin.value)
        
        
    
class IndexDataPoint(models.Model):
    
    index = models.ForeignKey(InflationIndex)
    
    year = models.IntegerField(db_index=True)
    
    value = models.DecimalField(max_digits=15, decimal_places=5) 