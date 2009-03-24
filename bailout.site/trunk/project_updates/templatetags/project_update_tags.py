from django.template import Library, Node
from django.template.loader import render_to_string
from project_updates.models import ProjectUpdate

register = Library()

class ProjectUpdateNode(Node):
    def render(self, context):
        project_updates = ProjectUpdate.objects.filter(published=True).order_by('-date')
        return render_to_string('project_updates/updates.html', {'items': project_updates})

# this could be done more easily with the @register.simple_tag decorator, it turns out
def project_updates(parser, token):
    return ProjectUpdateNode()
    
project_updates = register.tag(project_updates)
