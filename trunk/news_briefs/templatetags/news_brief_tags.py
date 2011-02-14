from django.template import Library, Node
from django.template.loader import render_to_string
from news_briefs.models import NewsBrief

register = Library()

class NewsBriefNode(Node):
    def render(self, context):
        news_briefs = NewsBrief.objects.all().order_by('-date')[:5]
        return render_to_string('news_briefs/newsbriefs.html', {'items': news_briefs})

def news_briefs(parser, token):
    return NewsBriefNode()
    
news_briefs = register.tag(news_briefs)
