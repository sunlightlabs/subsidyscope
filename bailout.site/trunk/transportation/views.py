#Create your views here

from inflation.models import InflationIndex
from highways.models import StateFunding
from helpers.helpers import JSONHttpResponse


def get_state_highway_funding_by_source(request, state_id):

    data = StateFunding.objects.getFundingBySource(state_id)
    
    return JSONHttpResponse(data)
     



def get_state_highway_funding_by_govt(request, state_id):
    
    data = StateFunding.objects.getFundingByGovt(state_id)
    
#    cci = InflationIndex.objects.get(name='CCI')
#    
#    cci_data = cci.getConversionTable(2007, 1995, 2007)
#    
#    chart_data = {}
#    
#    for year in range(1995, 2008):
#        
#        data[year][]
    
    
    
    
    return JSONHttpResponse(data)


