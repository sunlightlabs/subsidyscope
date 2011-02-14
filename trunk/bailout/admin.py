from bailout.models import *
from django.contrib import admin


class TransactionInline(admin.TabularInline):
    model = Transaction
    
class InstitutionAssetHistoryInline(admin.TabularInline):
    model = InstitutionAssetHistory

class InstitutionAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
        InstitutionAssetHistoryInline
    ]
    
    search_fields = ['name', 'fdic_number', 'ots_number']
    
    fieldsets = [
        (None, {'fields': ['name','display_name','institution_type','city','state','stock_symbol','logo']}),
        ('FDIC/OTS', {'fields': ['type_of_institution', 'fdic_number', 'ots_number','total_deposits','total_assets','percentage_return_on_assets','regulator','regulator_other']}),        
        ('Metadata', {'fields': ['datarun']})
    ]

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Transaction)
admin.site.register(SubsidyEstimate)
