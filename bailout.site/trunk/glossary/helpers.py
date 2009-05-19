from models import Item
from django.core.urlresolvers import reverse
from utils.msub import msub_first
from utils.msub import msub_global
from utils.pluralize import pluralize

def glossarize(plain):
    """
    Converts a string into a hyperlinked string.

    Notes:
    * Only the first occurence for each term is replaced.
    * It looks at one glossary item at a time.
    * Longer glossary items match first.
    """
    base_url = reverse("glossary")

    # Do an initial sort
    items = Item.objects.order_by('-term_length')

    def link(item):
        # Note that the asterisk (*) has special meaning for msub_first and
        # msub_global.
        return """<a href="%s#%s">*</a>""" % (base_url, item.slug)

    mapping = []
    for item in items:
        hyperlink = link(item)
        term = item.term
        mapping.extend([
            (r"\b%s\b" % term, hyperlink),
            (r"\b%s\b" % pluralize(term), hyperlink)])
        acronym = item.acronym
        if acronym:
            mapping.append((r"\b%s\b" % acronym, hyperlink))
        synonym = item.synonym
        if synonym:
            mapping.extend([
                (r"\b%s\b" % synonym, hyperlink),
                (r"\b%s\b" % pluralize(synonym), hyperlink)])
    
    # Do final sort: longer strings towards the front
    mapping.sort(cmp=lambda x, y: len(y[0]) - len(x[0]))

    return msub_first(plain, mapping)
