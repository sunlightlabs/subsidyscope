from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('term', 'acronym', 'slug', 'synonym', )
    fieldsets = (
            (None, {
                'fields': ('term', 'acronym', 'slug', 'synonym', 'definition', 'sectors')
            }),
        )

admin.site.register(Item, ItemAdmin)