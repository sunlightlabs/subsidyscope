from django.template import Library, Node
from django.template.loader import render_to_string
from project_updates.models import ProjectUpdate

import logging

register = Library()

class ProjectUpdateNode(Node):
    def __init__(self, sector):
        self.sector = sector
    def render(self, context):
        if int(self.sector) == 0:
            project_updates = ProjectUpdate.objects.filter(published=True).order_by('-date')      
        else:
            sector = int(self.sector) 
            project_updates = ProjectUpdate.objects.filter(published=True, sectors=sector).order_by('-date')
            
        if project_updates.count() > 8:
            more_updates = True 
        else:
            more_updates = False
            
        return render_to_string('project_updates/updates.html', {'items': project_updates[:8], 'more_updates':more_updates})

# this could be done more easily with the @register.simple_tag decorator, it turns out
def project_updates(parser, token):
    tag_name, sector = token.split_contents()
    return ProjectUpdateNode(sector)

project_updates = register.tag(project_updates)

@register.inclusion_tag('project_updates/subsector_sidebar.html')
def project_updates_subsector_sidebar(subsector_id):
    
    updates = ProjectUpdate.objects.filter(subsector__pk=int(subsector_id)).exclude(link='')
    
    return {'updates':updates}


