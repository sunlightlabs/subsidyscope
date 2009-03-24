import settings
import csv
import math
from decimal import Decimal, ROUND_HALF_DOWN
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
from bailout.models import Institution, Transaction, InstitutionDailyStockPrice
from django.core.urlresolvers import reverse
from helpers import JSONHttpResponse, compare_by, FileIterWrapper
from tarp_subsidy_graphics.models import SubsidyRecord
from GChartWrapper import GChart

def tarp_visualization_settings():
    return {
        'width': 880, 
        'height': 200, 
        'bar_width': 5, 
        'bar_margin': 1, 
        'bar_color_1': '0000ff',
        'bar_color_2': '8888ff',
        'highlight_color_1': 'ffff00',
        'highlight_color_2': 'ffff88',
        'height': 200,
    }
 
def tarp_index(request):

    transactions = Transaction.objects.select_related().order_by('date')
    
    visualization_settings = tarp_visualization_settings()
    visualization_settings['width'] = len(transactions) * (visualization_settings['bar_width'] + visualization_settings['bar_margin'])
    
    return render_to_response('bailout/tarp.html', {'transaction_list': transactions, 'visualization_settings': visualization_settings})

def tarp_warrants(request):

    transactions = Transaction.objects.filter(warrant_reported_strike_price__isnull=False).order_by('date')
    
    in_money = 0
    out_money = 0
    
    citi_stock = None
    citi_strike = None
    citi_percentage = None
    
    aig_stock = None
    aig_strike = None 
    aig_percentage = None
    
    last_date = transactions[0].getLastPriceUpdateDate()
    
    for transaction in transactions:
        if transaction.isInMoneyReportedStrikePrice():
            in_money += 1
        else:
            out_money += 1
          
        # get citi moneyness for transaction id 3  
        if transaction.id == 3:

            # assumes out of money 
            citi_percentage =  '%d' % int(100 * (1 - abs(transaction.getMoneyPercentage()))) 
            
        # get aig moneyness for transaction id 222  
        if transaction.id == 222:
            
            # assumes out of money 
            aig_percentage =  '%d' % int(100 * (1 - abs(transaction.getMoneyPercentage())))  
    
    total_transactions = in_money + out_money

    out_percentage = '%d%%' % round((out_money / total_transactions) * 100) 
    
    
    
    return render_to_response('bailout/tarp_warrants.html', {'transactions':transactions, 'last_date':last_date, 'in_money':in_money, 'total_transactions':total_transactions, 
                                                             'out_percentage':out_percentage, 'citi_stock':citi_stock, 'citi_strike':citi_strike, 'citi_percentage':citi_percentage,
                                                             'aig_stock':aig_stock, 'aig_strike':aig_strike, 'aig_percentage':aig_percentage })

def tarp_warrants_calculation(request):
    
    return render_to_response('bailout/tarp_warrants_calculation.html')


def _get_scale_bound(data):
    return Decimal(str(math.ceil(max(data) / 10) * 10))    

def _normalize_chart_range(data):
    out = {}
    m = _get_scale_bound(data)
    # m = max(data)
    #     m = Decimal(m) / Decimal(10)
    #     m = math.ceil(m)
    #     m = Decimal(str(m * 10))
    for x in range(0, len(data)):
        out[x] = (data[x] / m) * Decimal(100)
    return out        

def tarp_subsidies(request):
    estimated_subsidies = []
    subsidy_rates = []
    amounts_received = []
    names = []
    colors = []
    for r in SubsidyRecord.objects.all():
        estimated_subsidies.append(r.estimated_subsidy)
        subsidy_rates.append(r.subsidy_rate)
        amounts_received.append(r.amount_received)
        names.append(r.name)
        colors.append(r.color)
    
    # reverse names (API wrapper bug?)
    names.reverse()
    
    # estimated subsidies chart
    estimates_subsidies_normalized = _normalize_chart_range(estimated_subsidies)
    estimated_subsidies_chart = GChart('bhs', estimates_subsidies_normalized.values())  
    estimated_subsidies_chart.size((500,250))
    estimated_subsidies_chart.color('|'.join(colors))
    estimated_subsidies_chart.bar(18,2,0)
    estimated_subsidies_chart.axes.type('xy')
    estimated_subsidies_chart_xlabels = range(0, (_get_scale_bound(estimated_subsidies)+1), 5)
    estimated_subsidies_chart_xlabels = map((lambda x: str(x)), estimated_subsidies_chart_xlabels)
    estimated_subsidies_chart.axes.label(str('|'.join(estimated_subsidies_chart_xlabels)))
    estimated_subsidies_chart.axes.label('|'.join(names))
    estimated_subsidies_chart.axes.style('000000')
    estimated_subsidies_chart.axes.style('000000')    
    i = 0
    for x in estimated_subsidies:
        marker_text = 't $%.1f' % x
        estimated_subsidies_chart.marker(marker_text, '000000', 0, i, 10, -1)
        i = i+1
    
    # subsidy rates chart
    subsidy_rates_normalized = _normalize_chart_range(subsidy_rates)
    subsidy_rate_chart = GChart('bhs', subsidy_rates_normalized.values())  
    subsidy_rate_chart.size((500,250))
    subsidy_rate_chart.color('|'.join(colors))
    subsidy_rate_chart.bar(18,2,0)
    subsidy_rate_chart.axes.type('xy')
    subsidy_rate_chart_xlabels = range(0, (_get_scale_bound(subsidy_rates)+1), 10)
    subsidy_rate_chart_xlabels = map((lambda x: str(x)), subsidy_rate_chart_xlabels)
    subsidy_rate_chart.axes.label(str('|'.join(subsidy_rate_chart_xlabels)))
    subsidy_rate_chart.axes.label('|'.join(names))
    subsidy_rate_chart.axes.style('000000')
    subsidy_rate_chart.axes.style('000000')    
    i = 0
    for x in subsidy_rates:
        marker_text = 't %d%%' % x
        subsidy_rate_chart.marker(marker_text, '000000', 0, i, 10, -1)
        i = i+1
    
    
    # amounts received chart
    amounts_received_normalized = _normalize_chart_range(amounts_received)
    amounts_received_chart = GChart('bhs', amounts_received_normalized.values())  
    amounts_received_chart.size((500,250))
    amounts_received_chart.color('|'.join(colors))
    amounts_received_chart.bar(18,2,0)
    amounts_received_chart.axes.type('xy')
    amounts_received_chart_xlabels = range(0, (_get_scale_bound(amounts_received)+1), 10)
    amounts_received_chart_xlabels = map((lambda x: str(x)), amounts_received_chart_xlabels)
    amounts_received_chart.axes.label(str('|'.join(amounts_received_chart_xlabels)))
    amounts_received_chart.axes.label('|'.join(names))
    amounts_received_chart.axes.style('000000')
    amounts_received_chart.axes.style('000000')    
    i = 0
    for x in amounts_received:
        marker_text = 't $%.1f' % x
        amounts_received_chart.marker(marker_text, '000000', 0, i, 10, -1)
        i = i+1
    
    return render_to_response('bailout/tarp_subsidy_table.html', { 'estimated_subsidies_chart': estimated_subsidies_chart.img(), 'subsidy_rate_chart': subsidy_rate_chart.img(), 'amounts_received_chart': amounts_received_chart.img(), 'estimated_subsidies': estimated_subsidies, 'subsidy_rates': subsidy_rates, 'amounts_received': amounts_received, 'names': ' '.join(names), 'colors': '|'.join(colors)})

def tarp_js(request):

    transactions = Transaction.objects.select_related().order_by('date')

    visualization_settings = tarp_visualization_settings()
    visualization_settings['width'] = visualization_settings['width']

    return render_to_response('bailout/tarp.js', {'transaction_list': transactions, 'visualization_settings': visualization_settings}, mimetype='text/javascript')



def tarp_xml(request):
    transactions = Transaction.objects.select_related().order_by('date')
    return render_to_response('bailout/tarp.xml', { 'transaction_list': transactions }, mimetype='text/xml')


def visualization(request, template='bailout/bailout_visualization.html', mimetype='text/html'):
    visualization_settings = visualization_settings = {
        'sc_color': '#bf5004',
        'sc_color_highlight': '#953931',
        'ftd_color': '#548330',
        'ftd_color_highlight': '#336633',
        'pff_color': '#5875b6',
        'pff_color_highlight': '#2f4867'
    }
    return render_to_response(template, {'visualization_settings': visualization_settings }, mimetype=mimetype)

def agency_landing_page(request, agency):
    return render_to_response(('bailout/%s/index.html' % agency), {})

def visualization_index(request):
    return visualization(request, template='bailout/bailout_visualization.html', mimetype='text/html')

def visualization_css(request):
    return visualization(request, template='bailout/bailout_visualization.css', mimetype='text/css')
    
def visualization_js(request):
    return visualization(request, template='bailout/bailout_visualization.js', mimetype='text/javascript')
    
def redirect_to_bailout(request):
    return HttpResponseRedirect(reverse('Bailout'))
    
def redirect_to_tarp_subsidies(request):
    return HttpResponseRedirect(reverse('tarp-subsidies'))

def fdic_tlgp_csv(request):
    response = HttpResponse(FileIterWrapper(open(settings.STATIC_MEDIA_DIR + '/data/tlgp_opt_in_source_20090131.csv')), mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=FDIC_TLGP_opt-in.csv'
    #open(settings.STATIC_MEDIA_DIR + '/data/tlgp_opt_in_source_20090131.csv')
    #response.write(render_to_string('bailout/fdic/tlgp_opt_in_source_20090131.csv'))
    return response

def tarp_csv(request):
    
    last_date = InstitutionDailyStockPrice.objects.getLastUpdate()

    # array is necessary to preserve order; drag
    field_order = [ 
        'Date',
        'Name',
        'Price Paid',
        'Pricing Mechanism',
        'Description',
        'Transaction Type',
        'FDIC Number',
        'OTS Number',
        'Type of Institution',
        'Total Assets',
        'Regulator',
        'City',
        'State',
        'Stock Symbol',
        'Program',
        'Warrant Strike Price',
        'Warrant Received',
        'Stock Price (as of close %s)' % last_date,
        'In/Out of Money (as of close %s)' % last_date,
        'Subsidy Rate Estimate (percentage)',
        'Subsidy Rate Estimate Date',
        'Subsidy Rate Estimate Source'
    ]
    
    fields = {
        'Date': 'date',
        'Name': 'institution.name',
        'Price Paid': 'price_paid',
        'Pricing Mechanism': 'pricing_mechanism',
        'Description': 'description',
        'Transaction Type': 'transaction_type',
        'FDIC Number': 'institution.fdic_number',
        'OTS Number': 'institution.ots_number',
        'Type of Institution': 'institution.type_of_institution',
        'Total Assets': 'institution.total_assets_fixed',
        'Regulator': 'institution.regulator',
        'City': 'institution.city',
        'State': 'institution.state',
        'Stock Symbol': 'institution.stock_symbol',
        'Program': 'program',
        'Warrant Strike Price': 'warrant_reported_strike_price',
        'Warrant Received': 'warrants_issued',
        'Stock Price (as of close %s)' % last_date: 'getLastClosingPrice',
        'In/Out of Money (as of close %s)' % last_date: 'getMoneyPositionReportedStrikePrice',
        'Subsidy Rate Estimate (percentage)': 'getSubsidyEstimate.subsidy_rate',
        'Subsidy Rate Estimate Date': 'getSubsidyEstimate.date',
        'Subsidy Rate Estimate Source': 'getSubsidyEstimate.source'
    }
    

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subsidyscope-tarp.csv'

    writer = csv.writer(response)
    writer.writerow(field_order)

    transactions = Transaction.objects.select_related().order_by('date')
    for t in transactions:

        record = []
        for f in field_order:
            temp = t
            for p in fields[f].split('.'):
                temp = getattr(temp, p)
                if callable(temp):
                    temp = temp()
                    
            record.append(temp)

        writer.writerow(record)

    return response


def tarp_alt_index(request):
   return render_to_response('bailout/tarp_alt_index.html')


def tarp_alt_bubbles_index(request):
   return render_to_response('bailout/tarp_alt_bubbles_index.html')



def tarp_timeline_visualization_json(request):
    
    transactions = Transaction.objects.select_related().order_by('date')
    
    summary = []
    
    for transaction in transactions:
        #if transaction.institution.state == 'AZ':
        summary.append({'id': transaction.id, 'name':transaction.institution.name, 'state':transaction.institution.state, 'date':str(transaction.date), 'amount':str(transaction.price_paid)})
        #else:
        #    summary.append({'id': transaction.id, 'name':transaction.institution.name, 'state':transaction.institution.state, 'date':str(transaction.date), 'amount':0})
  
    return JSONHttpResponse(summary)

def tarp_institution_visualization_json(request):
    
    transactions = Transaction.objects.select_related().order_by('date')
    
    summary_dict = {}
    assets_dict = {}
    type = {}
    name = {}
    
    total = 0
    
    for transaction in transactions:
        
        if not summary_dict.has_key(transaction.institution.id):
            summary_dict[transaction.institution.id] = 0
        
        type[transaction.institution.id] = transaction.institution.get_type_of_institution_display()
        name[transaction.institution.id] = transaction.institution.name
        summary_dict[transaction.institution.id] += transaction.price_paid
        
        total += transaction.price_paid

    summary = []
    
    for id in summary_dict.keys():
        
        if summary_dict[id] > 0 and summary_dict[id]:
            percent = float(summary_dict[id] / total)
            if percent < 0.001:
                percent = -1
            summary.append({'id':id, 'type':type[id], 'name':name[id], 'amount':int(summary_dict[id]), 'percent':percent})
        
    
    return JSONHttpResponse(summary)


def tarp_institution_filter_json(request):
    
    if request.GET.has_key('q') and request.GET['q'] != '':
        transactions = Transaction.objects.select_related().filter(institution__name__icontains=request.GET['q']).order_by('institution__name')
    else:
        transactions = Transaction.objects.select_related().order_by('institution__name')
    
    
    institution_dict = {}
    transactions_dict = {}
    
    for transaction in transactions[:5]:
        
        institution_dict[transaction.institution.id] = transaction.institution.name
        
        if not transactions_dict.has_key(transaction.institution.id):
            transactions_dict[transaction.institution.id] = str(transaction.id)
        else:
            transactions_dict[transaction.institution.id] += ',' + str(transaction.id)
            
    result = ''
    
    for id in institution_dict.keys():
        
        result += str(institution_dict[id]) + '|' + str(transactions_dict[id]) + '\n'
        

    return HttpResponse(result, mimetype='text/plain')


def bank_search_json(request):
    
    if request.GET.has_key('q') and request.GET['q'] != '':
        
        institutions = Institution.objects.filter(Q(name__icontains=request.GET['q']) 
                                                  | Q(display_name__icontains=request.GET['q'])).order_by('-total_assets')
        
        #if institutions.count() == 0:
        #    institutions = Institution.objects.filter(city__icontains=request.GET['q']).order_by('-total_assets')
            
        #if institutions.count() == 0:
        #    institutions = Institution.objects.filter(state__iexact=request.GET['q']).order_by('-total_assets')
    
    else:
        institutions = Institution.objects.order_by('name')
    
        
    result = ''
    
    for institution in institutions[:5]:
        
        result += '%s (%s, %s)|%d\n' % (str(institution.name).replace(', National Association', ''), institution.city, institution.state, institution.id)
        

    return HttpResponse(result, mimetype='text/plain')


def bank_summary(request, bank_id):
    
    if bank_id != '':
        institution = Institution.objects.select_related().get(id=int(bank_id))
        return render_to_response('bailout/bank_summary.html', {'institution':institution})
        
        
    return HttpResponse()
    
        
            
