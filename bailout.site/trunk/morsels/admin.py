from models import Morsel, Page

from django import forms
from django.contrib import admin
from django.db import models
from rcsfield import fields 


#class MorselAdmin(admin.ModelAdmin):
#    list_display = ('url', 'name', 'locked')
#    fieldsets = (
#        (None, {
#            'fields': ('url', 'title', 'content', 'sites')
#        }),
#        ('Advanced options', {
#            'classes': ('collapse',),
#            'fields': ('locked',)
#        }),
#    )


class MorselModelAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(MorselModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content':
             field.widget.attrs['cols'] = 100 
             field.widget.attrs['rows'] = 50
        return field

#class MorselModelAdmin(admin.ModelAdmin):
#   formfield_overrides = {fields.RcsTextField: {'widget': forms.Textarea(attrs={'rows':50, 'cols':100})}}

admin.site.register(Page)
admin.site.register(Morsel, MorselModelAdmin)
