#Create your views here

from highways.models import StateFunding
from helpers.helpers import JSONHttpResponse


def get_state_highway_funding_by_source(request, state_id):

    data = StateFunding.manager.getFundingBySource(state_id)
    
    return JSONHttpResponse(data)
     



def get_state_highway_funding_by_govt(request, state_id):
    
    data = StateFunding.manager.getFundingByGovt(state_id)
    
    return JSONHttpResponse(data)


