from django.template import Library, Node
from django.template.loader import render_to_string
from carousel.models import CarouselEntry
import settings

register = Library()

@register.inclusion_tag('carousel/index.html')
def carousel_entries_all():
    entries =  CarouselEntry.objects.filter(published=True).order_by('weight')[:3]
    return { 'entries': entries }

@register.inclusion_tag('carousel/sector.html')
def carousel_entries(sector_id):
    
    entries = CarouselEntry.objects.filter(published=True).order_by('weight')
    if sector_id:
        entries = entries.filter(sector=sector_id)
    return { 'entries': entries }



