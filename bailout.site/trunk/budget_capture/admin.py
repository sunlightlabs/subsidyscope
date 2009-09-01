from budget_capture.models import *
from django.contrib import admin


class BudgetDataFiscalYearInline(admin.TabularInline):
    model = BudgetDataFiscalYear
    
    extra = 10
    max_num = 10
    
class BudgetDataAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    
    inlines = [
        BudgetDataFiscalYearInline
    ]
    
    
admin.site.register(Task)
admin.site.register(Item)
admin.site.register(BudgetData, BudgetDataAdmin)
