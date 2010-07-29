from models import Morsel, Page

from django import forms
from django.contrib import admin

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
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'rows':50, 'cols':100})}}

admin.site.register(Page)
admin.site.register(Morsel, MorselModelAdmin)