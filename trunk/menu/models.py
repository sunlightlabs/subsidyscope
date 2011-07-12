from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Menu(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    base_url = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    #the below fields are so the model can be self referential
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    parent_menu_id = models.PositiveIntegerField(null=True, blank=True)
    parent_menu = generic.GenericForeignKey('content_type', 'parent_menu_id')
    css_class = models.CharField(max_length=100, null=True, blank=True)
     
    def __unicode__(self):
        return "%s - %s" % (self.slug, self.name)

    class Admin:

        def __unicode__(self):
            return "%s" % self.name

        def save(self):
            """
            Re-order all items at from 10 upwards, at intervals of 10.
            This makes it easy to insert new items in the middle of 
            existing items without having to manually shuffle 
            them all around.
            """
            super(Menu, self).save()

            current = 10
            for item in MenuItem.objects.filter(menu=self).order_by('order'):
                item.order = current
                item.save()
                current += 10

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)
    order = models.IntegerField()
    link_url = models.CharField(max_length=100, help_text='URL or URI to the content, eg /about/ or http://foo.com/')
    title = models.CharField(max_length=100)
    login_required = models.BooleanField(default=False)
    css_class = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return "%s %s. %s" % (self.menu.slug, self.order, self.title)
