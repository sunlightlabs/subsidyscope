# Create your views here.
from project_updates.models import ProjectUpdate
from django.shortcuts import render_to_response, get_object_or_404

def entry(request, entry_year, entry_month, entry_day, entry_slug):
    update = get_object_or_404(ProjectUpdate.objects.all().filter(date__year=int(entry_year)).filter(date__month=int(entry_month)).filter(date__day=int(entry_day)), slug=entry_slug)    
    return render_to_response('project_updates/update.html', {'item': update })
