from fdic_bank_failures.models import BankFailure, QBPSnapshot
from django.shortcuts import render_to_response
from django.http import HttpResponse
import csv

def fdic_bank_failures_xml(request):
    bank_failure_list = BankFailure.objects.all().order_by('closing_date')    
    return render_to_response('bailout/fdic/fdic_bank_failures.xml', { 'bank_failure_list': bank_failure_list }, mimetype='text/xml')

def fdic_bank_failures_csv(request):
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subsidyscope-tarp.csv'

    writer = csv.writer(response)

    headers = []
    for field in BankFailure._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)

    failures = BankFailure.objects.all().order_by('closing_date')
    for failure in failures:

        record = []
        for field in BankFailure._meta.fields:
            record.append(getattr(failure, field.name, None))

        writer.writerow(record)

    return response
    
def fdic_qbpsnapshot_xml(request):
    qbp_snapshots = QBPSnapshot.objects.all().order_by('date')
    return render_to_response('bailout/fdic/qbp_snapshots.xml', { 'qbp_snapshots': qbp_snapshots }, mimetype='text/xml')