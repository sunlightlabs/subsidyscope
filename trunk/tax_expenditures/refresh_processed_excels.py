from tax_expenditures.models import Group, GroupSummary, Expenditure, Estimate, TE_YEARS
from django.db.models import Max, Min, Q
import csv, re, sys

SOURCES = ('', 'JCT', 'Treasury')
MAX_COLUMNS = 11

header_summary = ['Indent', 'Category', 'Source', 'report', '2000 Corp','2001 Corp','2002 Corp','2003 Corp','2004 Corp','2005 Corp','2006 Corp','2007 Corp','2008 Corp','2009 Corp','2010 Corp','2011 Corp','2012 Corp','2013 Corp','2014 Corp','2015 Corp', '2016 Corp','2000 Indv','2001 Indv','2002 Indv','2003 Indv','2004 Indv','2005 Indv','2006 Indv','2007 Indv','2008 Indv','2009 Indv','2010 Indv','2011 Indv','2012 Indv','2013 Indv','2014 Indv','2015 Indv', '2016 Indv', 'Description/Expenditure Name', 'Notes']

def save_description(year, id, paragraphs):
    
    final_text = ''
    
    for paragraph in paragraphs:
        final_text += '<p>%s</p>' % (paragraph)
    
    try:
        
        expenditure = Expenditure.objects.get(source=Expenditure.SOURCE_TREASURY, analysis_year=year, item_number=id)
        
        print 'Loading item %d: %s' % (id, expenditure.name)
        
        expenditure.group.description = final_text
        expenditure.group.save()
    except:
        print "Item %d not found" % (id)
    

def load_descriptions(filename, year):
    
    for expenditure in Expenditure.objects.filter(source=Expenditure.SOURCE_TREASURY, analysis_year=year):
        expenditure.description = ''
        expenditure.save()

    file = open (filename, 'r')
    
    line_id = 1
    description = '' 
    paragraphs = []
    
    for line in file.readlines():
        line = unicode(line.decode("utf-8"))
        line = line.strip().replace(u'\x96', '-').replace(u'\u20ac', '-').replace(u'\u2013', '-').replace(u'\u2014', '&mdash;').replace(u'\u201c','"').replace(u'\u201d','"').replace(u'\xc2-15', '-').replace(u'\u2019', "'")
        line_regex = re.compile('^%d\. ' % (line_id))
        
        if not line:
            if not description == '': 
                paragraphs.append(description)
                description = ''
            
            continue
                
            
        if line_regex.match(line):
            
            if not description == '': 
                paragraphs.append(description)
                description = ''
            
            if len(paragraphs):
                save_description(year, line_id - 1, paragraphs)
                description = ''
                paragraphs = []
        
            line = line_part = line_regex.sub('', line)
                
            line_id += 1
        
        if line[-1] == '-':
            line = line[:-1]
        else:
            line += ' '
            
        description += line
    
    save_description(year, line_id - 1, paragraphs)
        

def load_footnotes(filename):
    
    file = open (filename, 'r')
    
    for line in file.readlines():
        line = line.strip()
        line_parts = line.split('\t')
        
        id = int(line_parts[0])
        year = int(line_parts[1])
         
        try:
            expenditure = Expenditure.objects.get(source=Expenditure.SOURCE_TREASURY, analysis_year=year, item_number=id)
        
            expenditure.notes = line_parts[2]
        
            expenditure.save()
        
            print year, id
        
        except:
            
            print 'Not found: ', year, id
        
 
def recurse_category(parent, writer, indent, budget_function):

    header_row = [indent, parent.name]
    for i in range(2,38):
        header_row.append('')
    header_row.append(parent.description.encode('ascii', 'ignore'))
    header_row.append(parent.notes.encode('ascii', 'ignore'))     
    writer.writerow(header_row)

    first = True 
    for source in (1, 2):
#            row.append(parent.name)
#            row.append(parent.get_source_display())
        
    
        for expenditure in parent.expenditure_set.filter(source=source).order_by('analysis_year'):
            
            row = []
            corp_estimates = {}
            indv_estimates = {}
            total_estimates = {}

            row.append(indent + '+')
            if source == 2:
                row.append(expenditure.item_number)
            else:
                row.append('')
            row.append(SOURCES[source])
            row.append(expenditure.analysis_year)
#                row.append(parent.notes)
#                first = False

            for estimate in expenditure.estimate_set.all().order_by('estimate_year'):
                if estimate.corporations_amount or estimate.individuals_amount:
                    total_estimates[estimate.estimate_year] = None
                
                if estimate.corporations_notes == Estimate.NOTE_POSITIVE:
                    total_estimates[estimate.estimate_year] = 0
                    corp_estimates[estimate.estimate_year] = '<50'
                elif estimate.corporations_notes == Estimate.NOTE_NEGATIVE:
                    total_estimates[estimate.estimate_year] = 0
                    corp_estimates[estimate.estimate_year] = '>-50'
                else:
                    if estimate.corporations_amount >= 0:
                        corp_estimates[estimate.estimate_year] = estimate.corporations_amount
                        total_estimates[estimate.estimate_year] = estimate.corporations_amount
                
                if estimate.individuals_notes == Estimate.NOTE_POSITIVE:
                    
                    if total_estimates.get(estimate.estimate_year) and not total_estimates[estimate.estimate_year]:
                        total_estimates[estimate.estimate_year] = 0
                        
                    indv_estimates[estimate.estimate_year] = '<50'
                    
                elif estimate.individuals_notes == Estimate.NOTE_NEGATIVE:
                    
                    if not total_estimates[estimate.estimate_year]:
                        total_estimates[estimate.estimate_year] = 0
                    
                    indv_estimates[estimate.estimate_year] = '>-50'
                    
                else:
                    if estimate.individuals_amount >= 0:
                        indv_estimates[estimate.estimate_year] = estimate.individuals_amount
                        
#                        if total_estimates[estimate.estimate_year]:
 #                           total_estimates[estimate.estimate_year] += estimate.individuals_amount
                   
#else:
 #                           total_estimates[estimate.estimate_year] = estimate.individuals_amount
            
        
                
            for year in TE_YEARS:
                if corp_estimates.has_key(year):
                    row.append(corp_estimates[year])
                else:
                    row.append('')
                    
            for year in TE_YEARS:                
                if indv_estimates.has_key(year):
                    row.append(indv_estimates[year])
                else:
                    row.append('')    

            row.append(expenditure.name.encode('ascii', 'ignore'))
            row.append(expenditure.notes.encode('ascii', 'ignore'))           

            writer.writerow(row)                  
                
    indent = '#' + indent
    
    for subgroup in Group.objects.filter(parent=parent):
        
        recurse_category(subgroup, writer, indent, budget_function)
                    

def data_check_definitions():
    groups = Group.objects.exclude(parent=None)
    selected = []
    for g in groups:
        exp = Expenditure.objects.filter(source=2, group=g).order_by('-analysis_year')
        if len(exp) > 0 and exp[0].analysis_year < 2011:
            print "%s -- %s" % (exp[0].analysis_year, g.name)


def data_check_matches(left_source, right_source, filename, no_match_filename, left_header, right_header):
    writer = csv.writer(open("datachecks/%s.csv" % filename, 'w'))
    no_match_writer = csv.writer(open("datachecks/%s.csv" % no_match_filename, 'w'))
    left_total = {}
    right_total = {}
    writer.writerow(("%s Title" % left_header, "%s Title(s)" % right_header, "Budget Function", "%s Estimate Year Range" % left_header, "%s Estimate Year Range" % right_header, "Description"))
    no_match_writer.writerow(("%s Title" % left_header, "Budget Function", "%s Estimate Year Range" % left_header, "Description"))

    functions = Group.objects.filter(parent=None)
    for f in functions:
        groups = Group.objects.filter(parent=f)
        for g in groups:
            left_summary = GroupSummary.objects.filter(group=g, estimate=3, source=left_source).order_by('estimate_year')
            budget_function = f.name
            if left_summary.count() > 0:
                
                left_min_year = left_summary.filter(Q(amount__isnull=False) | Q(notes=1)).aggregate(Min('estimate_year'))['estimate_year__min']
                left_max_year = left_summary.filter(Q(amount__isnull=False) | Q(notes=1)).aggregate(Max('estimate_year'))['estimate_year__max']
                left_exp = Expenditure.objects.filter(source=left_source, group=g).order_by('-analysis_year')
                if left_exp.count() > 0:
                   left_title = left_exp[0].name
                else:
                    print "%s - %s - %s" % (g.id, g.name, f.name)
                    left_title = g.name
                left_desc = g.description

                right_summary = GroupSummary.objects.filter(source=right_source, group=g, estimate=3).order_by('estimate_year')
                if right_summary.count() > 0:
                    right_min_year = right_summary.filter(amount__isnull=False).aggregate(Min('estimate_year'))['estimate_year__min']
                    right_max_year = right_summary.filter(amount__isnull=False).aggregate(Max('estimate_year'))['estimate_year__max']
                    right_exp = Expenditure.objects.filter(source=right_source, group=g).order_by('-analysis_year')
                    if right_exp.count() > 0:
                        names = right_exp[0].name
                    else:
                        names = ''
                    child_groups = Group.objects.filter(parent=g)
                    for cg in child_groups:
                        gs = GroupSummary.objects.filter(group=cg, source=right_source)
                        for cs in gs: 
                            names += cg.name + ', '
                    writer.writerow((left_title.encode('ascii', 'ignore'), names.encode('ascii', 'ignore'), budget_function, "%s-%s" % (left_min_year, left_max_year), "%s-%s" % (right_min_year, right_max_year), left_desc.encode('ascii', 'ignore')))


                    #calculate aggregates for matched items
                    for ls in left_summary:
                        if ls.amount:
                            if left_total.has_key(ls.estimate_year): 
                                temp = left_total[ls.estimate_year] + ls.amount
                                left_total[ls.estimate_year] = temp

                            else: left_total[ls.estimate_year] = ls.amount

                    for rs in right_summary:
                        if rs.amount:
                            if right_total.has_key(rs.estimate_year): 
                                temp = right_total[rs.estimate_year] + rs.amount
                                right_total[rs.estimate_year] = temp
                            else: right_total[rs.estimate_year] = rs.amount 


                else:
                    no_match_writer.writerow((left_title.encode('ascii', 'ignore'), budget_function, "%s-%s" % (left_min_year, left_max_year), left_desc.encode('ascii', 'ignore')))

    print left_header + " Aggregates for Matched Items"
    for k in sorted(left_total.keys()):
        print "%s, %d" % (k, left_total[k])
    print right_header + "Aggregates for Matched Items"
    for k in sorted(right_total.keys()):
        print "%s, %d" % (k, right_total[k])


arg_options = ["load_footnotes", "load_descriptions", "postprocess_tes", "everything"]

if len(sys.argv) > 1:
    op = sys.argv[1]
    if op == "load_footnotes" or op == 'everything':
        load_footnotes('/home/kaitlin/envs/subsidyscope/trunk/scripts/data/tax_expenditures/data/omb_ap/ap_footnotes.txt')
    if op == "load_descriptions" or op == 'everything':
        load_descriptions('/home/kaitlin/envs/subsidyscope/trunk/scripts/data/tax_expenditures/data/omb_ap/spec2011_descriptions.txt', 2011)
        load_descriptions('/home/kaitlin/envs/subsidyscope/trunk/scripts/data/tax_expenditures/data/omb_ap/spec2012_descriptions.txt', 2012)
    if op == "postprocess_tes" or op == 'everything':
        top_level_groups = Group.objects.filter(parent=None)
        for group in top_level_groups:
            name = group.name
            writer = csv.writer(open("postprocessed/%s_postprocessed.csv" % name, 'w'))
            writer.writerow(header_summary)
            writer.writerow(['', group.name])
            
            for subgroup in Group.objects.filter(parent=group):
                recurse_category(subgroup, writer, '#', name)

    elif op == 'data_check_definitions':
        data_check_definitions()

    elif op == 'data_check_treasury_matches':
        data_check_matches(2, 1, "treasury_tes_with_matches", "treasury_tes_withOUT_matches", "Treasury", "JCT")
    elif op == 'data_check_jct_matches':
        data_check_matches(1, 2, "jct_tes_with_matches", "jct_tes_withOUT_matches", "JCT", "Treasury")

else:
    print "give me an argument please, your options are:"
    for i in arg_options:
        print "-- %s" % i

