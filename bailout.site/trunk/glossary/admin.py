from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('term', 'acronym', 'slug', 'synonym', )
    fieldsets = (
            (None, {
                'fields': ('term', 'acronym', 'slug', 'synonym', 'definition', 'sectors')
            }),
        )
    
    def save_model(self, request, obj, form, change):
         self.update_term_length()
         self.autogenerate_slug_if_blank()
         obj.save()


admin.site.register(Item, ItemAdmin)