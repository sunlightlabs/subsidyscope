from django.db import models

class BudgetFunction(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    code = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
