from fdic_bank_failures.models import BankFailure, QBPSnapshot
from django.shortcuts import render_to_response
from django.http import HttpResponse
import csv
import string

def fdic_bank_failures_xml(request):
    bank_failure_list = BankFailure.objects.all().order_by('closing_date')    
    return render_to_response('bailout/fdic/fdic_bank_failures.xml', { 'bank_failure_list': bank_failure_list }, mimetype='text/xml')

def fdic_bank_failures_csv(request):
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subsidyscope-tarp.csv'

    writer = csv.writer(response)

    field_name_substitutions = {
        'name': 'Failed Institution',
        'closing_date': 'Date of Bank Closure',
        'exact_amount': 'Estimated Loss to the Deposit Insurance Fund (exact)',
        'range_low': 'Estimated Loss to the Deposit Insurance Fund (lower range)',
        'range_high': 'Estimated Loss to the Deposit Insurance Fund (upper range)'
    }    
    columns_to_exclude = ['id', 'updated_date']
    currency_columns = ['exact_amount', 'range_high', 'range_low']

    headers = []
    for field in BankFailure._meta.fields:
        if field.name not in columns_to_exclude:
            if field.name in field_name_substitutions:
                headers.append(field_name_substitutions[field.name])
            else:
                headers.append(string.capwords(field.name))
    writer.writerow(headers)

    failures = BankFailure.objects.all().order_by('closing_date')
    for failure in failures:

        record = []
        for field in BankFailure._meta.fields:
            if field.name not in columns_to_exclude:
                value = getattr(failure, field.name, None)
                if field.name in currency_columns and value is not None:
                    value = int(value) * 1000000                
                record.append(value)

        writer.writerow(record)

    return response
    
def fdic_qbpsnapshot_xml(request):
    qbp_snapshots = QBPSnapshot.objects.all().order_by('date')
    return render_to_response('bailout/fdic/qbp_snapshots.xml', { 'qbp_snapshots': qbp_snapshots }, mimetype='text/xml')