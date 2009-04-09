from models import Morsel

from django.contrib import admin

class MorselAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'locked')
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('locked',)
        }),
    )

admin.site.register(Morsel, MorselAdmin)
