from django.template import Library, Node
from django.template.loader import render_to_string
from carousel.models import CarouselEntry
import settings

register = Library()

@register.simple_tag
def carousel_entries():
    
    entries = CarouselEntry.objects.filter(published=True).order_by('weight')
    num_entries = entries.count()
    out = ""
    i = 0
    for c in entries:
        out = out + '<div id="tab-%d" class="carousel-tab"><img src="%s" width="415"><h2><a href="%s">%s</a></h2><p class="feature_content"><strong>%s&nbsp;&ndash;&nbsp;</strong>%s</p><ul class="feature_nav tabNavigation feature_circle">' % (i, c.image.url, c.link, c.title, c.date.strftime('%m/%d/%y'), c.text)

        for tab_i in range(0, num_entries):
            selected = 'unselected'
            if i==tab_i:
                selected = 'selected'
            out = out + '<li><a href="#tab-%d"><img src="%simages/front/feature_nav_%s.png"></a></li>' % (tab_i, settings.MEDIA_URL, selected)

        out += '</ul></div>'
        
        i = i + 1

    return out
