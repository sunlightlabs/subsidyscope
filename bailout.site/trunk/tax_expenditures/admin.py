from models import TaxExpenditure, TaxExpenditureEstimate

from django.contrib import admin


class TaxExpenditureEstimateInline(admin.TabularInline):
    model = TaxExpenditureEstimate

class TaxExpenditureAdmin(admin.ModelAdmin):
   
    inlines = [TaxExpenditureEstimateInline]

admin.site.register(TaxExpenditure, TaxExpenditureAdmin)
admin.site.register(TaxExpenditureEstimate)