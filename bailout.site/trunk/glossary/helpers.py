from models import Item
from django.core.urlresolvers import reverse
from utils.multiple_sub import multiple_sub


def glossarize(plain):
    """
    Converts a string into a hyperlinked string.

    It looks at one glossary item at a time.
    Longer glossary items match first.
    """
    base_url = reverse("glossary")
    items = Item.objects.order_by('-term_length')

    def link(item):
        return """<a href="%s#%s">%s</a>""" % (base_url, item.slug, item.term)

    mapping = [(item.term, link(item)) for item in items]
    return multiple_sub(plain, mapping)
