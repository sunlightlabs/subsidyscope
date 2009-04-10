from fed_h41.models import H41Snapshot, FedNewsEvent
from django.shortcuts import render_to_response
from django.http import HttpResponse
import csv
import datetime
import string

def h41_xml(request):    
    
    snapshots = H41Snapshot.objects.all().filter(date__gte=datetime.datetime(2007, 1, 1)).order_by('date')
    
    fields_to_exclude = ['id', 'reserve_bank_credit']
    
    labels = []
    if len(snapshots)>0:
        for field in snapshots[0]._meta.fields:
            if field.name not in fields_to_exclude:
                labels.append( (field.name, field.verbose_name) )
            
    object_list = []
    for snapshot in snapshots:
        row = []
        for fieldtuple in labels:
        #for field in snapshot._meta.fields:
            fieldname = fieldtuple[0]
            value = str(getattr(snapshot, fieldname, None))         
            if value==None:
                row.append( (fieldname, '' ) )
            else:
                row.append( (fieldname,  value) )
        object_list.append(row)
    
    return render_to_response('bailout/federal_reserve/generic.xml', { 'labels': labels, 'object_list': object_list }, mimetype='text/xml')


def fed_news_xml(request):
    news = FedNewsEvent.objects.all().order_by('date')
    return render_to_response('bailout/federal_reserve/news.xml', { 'news': news }, mimetype='text/xml')
    

def h41_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subsidyscope-fed-h41-snapshots.csv'

    writer = csv.writer(response)

    field_name_substitutions = {       
    }    
    columns_to_exclude = ['id']
    currency_columns = [
        'reserve_bank_credit',
        'repurchase_agreements',
        'primary_credit',
        'secondary_credit',
        'seasonal_credit',
        'other_credit_extensions',
        'mortgage_backed_securities',
        'term_auction_credit',
        'primary_dealer_and_other_broker_dealer_credit',
        'asset_backed_commercial_paper_money_market',
        'credit_extended_to_aig',
        'commercial_paper_funding_facility',
        'money_market_investor_funding_facility',
        'maiden_lane_i',
        'maiden_lane_ii',
        'maiden_lane_iii',
        'federal_agency_debt_securities',
        'term_facility',
        'talf',
        'other_federal_reserve_assets',
        'central_bank_liquidity_swaps',
        'us_treasury_securities'
    ]

    headers = []
    for field in H41Snapshot._meta.fields:
        if field.name not in columns_to_exclude:
            if field.name in field_name_substitutions:
                headers.append(field_name_substitutions[field.name])
            else:
                headers.append(field.verbose_name)
    writer.writerow(headers)

    snapshots = H41Snapshot.objects.all().order_by('date')
    for snapshot in snapshots:

        record = []
        for field in H41Snapshot._meta.fields:
            if field.name not in columns_to_exclude:
                value = getattr(snapshot, field.name, None)
                if field.name in currency_columns and value is not None:
                    value = int(value) * 1000000                
                record.append(value)

        writer.writerow(record)

    return response