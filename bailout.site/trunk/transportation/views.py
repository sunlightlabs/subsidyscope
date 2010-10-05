#Create your views here
import math

from inflation.models import InflationIndex
from highways.models import StateFunding, StateRoadJurisdiction
from helpers.helpers import JSONHttpResponse





def get_state_highway_funding_table(request, state_id):

    data = StateFunding.objects.getFundingBySource(state_id, 2007)
    
    return JSONHttpResponse(data)



def get_state_highway_miles_table(request, state_id):

    data = StateRoadJurisdiction.objects.getJurisdictionMiles(state_id)
    
    return JSONHttpResponse(data)
     

def get_state_highway_funding_chart(request, state_id):
    
    data = StateFunding.objects.getFundingBySource(state_id, 2007)

    values = []
    years = []
    
    annual_totals = []
    
    for year in range(1995, 2008):
        year_values = []
    
        # user 
        year_values.append(int(data[year]['state_user'] + data[year]['local_user']))
        
        # non-user
        year_values.append(int(data[year]['state_non_user'] + data[year]['local_non_user']))
    
        # bonds 
        year_values.append(int(data[year]['state_bonds'] + data[year]['local_bonds']))
        
        # federal 
        year_values.append(int(data[year]['federal']))
        
        
        values.append(year_values)
        
        annual_totals.append(sum(year_values))
        
        years.append(str(year))
        
   
    maximum=0
    json= {"elements":[]}
    
        
    json["elements"].append({"type": "bar_stack", "tip":"", "values": values, "colours": ["#336699","#9CA991","#669EB3","#BF5004"], "keys": 
                    [{"colour": "#336699","text": "User Revenue","font-size": 13},
                    {"colour": "#9CA991","text": "Non-user Revenue","font-size": 13},
                    {"colour": "#669EB3","text": "Bonds","font-size": 13},
                    {"colour": "#BF5004","text": "Federal Funds","font-size": 13}]})
    
    
    maximum = max(annual_totals)

        
        
    json["title"] = {"text":""}
    json["bg_colour"] = "#FFFFFF"
    json["x_axis"] = {"3d": 0, "colour":"#909090", "tick-height":20, "labels": {"labels":years}}
    
    mod = 1000
   
    # slightly better scale-definition function
    p = pow(10, (math.floor(math.log(maximum,10)))) * 1.0
    maximum = round((maximum / p) + 0.5) * p

        
    json["y_axis"] = {"colour": "#909090", "min": 0, "max": maximum}
    json["x_legend"] = {"text": "Fiscal Year", "style": "{font-size:12px;}"}
    json["y_legend"] = {"text": "US Dollars (2007)", "style": "{font-size: 13px; margin-right:7px;}"}
    
    
    

    
    return JSONHttpResponse(json)


