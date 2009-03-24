from django.contrib import admin
from fdic_bank_failures.models import *

admin.site.register(BankFailure)
admin.site.register(QBPSnapshot)