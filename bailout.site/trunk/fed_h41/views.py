from fed_h41.models import H41Snapshot, FedNewsEvent
from django.shortcuts import render_to_response
from django.http import HttpResponse
import csv
import datetime

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
    
        