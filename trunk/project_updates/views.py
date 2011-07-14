# Create your views here.
from project_updates.models import ProjectUpdate
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def entry(request, entry_year, entry_month, entry_day, entry_slug):
    update = get_object_or_404(ProjectUpdate.objects.all().filter(date__year=int(entry_year)).filter(date__month=int(entry_month)).filter(date__day=int(entry_day)), slug=entry_slug)    
    return render_to_response('project_updates/update.html', {'item': update },
                              context_instance=RequestContext(request))

def archive(request, page):
    
    page = int(page)
    
    page_size = 5
    
    start_pos = page_size * (page - 1)
    end_pos = (page_size * page)
    
    total_updates = ProjectUpdate.objects.all().count()
    
    if (end_pos - 1) < ProjectUpdate.objects.all().count():
        updates = ProjectUpdate.objects.all().order_by('-date')[start_pos:end_pos]
        next_page = page + 1
    else:
        updates = ProjectUpdate.objects.all().order_by('-date')[start_pos:]
        next_page = False

    if page > 1:
        previous_page = page - 1
    else:
        previous_page = False
        

    return render_to_response('project_updates/archive.html', {'updates': updates, 'next_page':next_page, 'previous_page':previous_page })
