from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify


class Item(models.Model):
    slug        = models.SlugField(db_index=True, unique=True)
    term        = models.CharField(max_length=255, unique=True, db_index=True)
    term_length = models.IntegerField(db_index=True)
    acronym     = models.CharField(max_length=32, db_index=True)
    synonym     = models.CharField(max_length=255, db_index=True)
    definition  = models.TextField()

    def __unicode__(self):
        return u"%s" % self.term

    def save(self):
        self.update_term_length()
        self.autogenerate_slug_if_blank()
        super(Item, self).save()

    def update_term_length(self):
        self.term_length = len(self.term) if self.term else 0

    def autogenerate_slug_if_blank(self):
        if self.term and not self.slug:
            self.slug = slugify(self.term)

admin.site.register(Item)
