from models import Item
from django.core.urlresolvers import reverse


def glossarize(plain):
    """
    Converts a string into a hyperlinked string.

    It looks at one glossary item at a time.
    Longer glossary items match first.
    """
    out = plain
    base_url = reverse("glossary")
    for item in Item.objects.order_by('-term_length'):
        link = """<a href="%s#%s">%s</a>""" % (base_url, item.slug, item.term)
        out = out.replace(item.term, link)
    return out
