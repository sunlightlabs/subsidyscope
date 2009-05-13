from models import Item
from django.template import loader, Context
from django.http import HttpResponse


def list(request):
    items = Item.objects.order_by('term')
    template = loader.get_template("list.html")
    context = Context({'glossary_items': items})
    return HttpResponse(template.render(context))
