from haystack import indexes
from haystack.sites import site
from tax_expenditures.models import Group

class GroupIndex(indexes.SearchIndex):
    type = 'tax-expenditure-group'
    group_name = indexes.CharField(model_attr='name')
    group_description = indexes.CharField(model_attr='description')
    group_id = indexes.IntegerField(model_attr='id')
    text = indexes.CharField(document=True, model_attr='description')

    def get_queryset(self):
        return Group.objects.filter(parent__isnull=False)

    def prepare_text(self, object):
        return (object.name + ' ' + object.description).encode('ascii', 'ignore')

site.register(Group, GroupIndex)
