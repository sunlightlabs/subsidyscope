from models import Item
from django.core.urlresolvers import reverse
from utils.msub import msub_first
from utils.msub import msub_global


def glossarize(plain):
    """
    Converts a string into a hyperlinked string.

    Notes:
    * Only the first occurence for each term is replaced.
    * It looks at one glossary item at a time.
    * Longer glossary items match first.
    """
    base_url = reverse("glossary")
    items = Item.objects.order_by('-term_length')

    def link(item):
        return """<a href="%s#%s">%s</a>""" % (base_url, item.slug, item.term)

    mapping = [(item.term, link(item)) for item in items]
    return msub_first(plain, mapping)
