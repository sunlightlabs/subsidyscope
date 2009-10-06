from django.template import Library, Node
from django.template.loader import render_to_string
import faads.views

register = Library()

class QuickSearchNode(Node):
    def __init__(self, sector=None):
        self.sector = sector
        print sector
    
    def render(self, context):
        form_class = faads.views.MakeFAADSSearchFormClass(sector=self.sector)
        form = form_class()
        return render_to_string('faads/search/quick_search.html', {'form': form, 'sector_name': getattr(self.sector, 'name', False)})

@register.tag
def faads_quick_search(parser, token):
    tokens = token.split_contents()

    sector = None
    try:
        sector = faads.views.get_sector_by_name(tokens[1])
    except (ValueError, IndexError):
        pass        

    return QuickSearchNode(sector)
