from models import Morsel, Page

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


admin.site.register(Page)
admin.site.register(Morsel)