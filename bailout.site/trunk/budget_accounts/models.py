from django.db import models

class Agency(models.Model):
    
    code = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    

class BudgetFunction(models.Model):
    
    parent = models.ForeignKey('self', null=True)
    
    code = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()

class BudgetAccountManager(models.Manager):
    
    def createBudgetAccount(self, account):
    
        account_parts = account.split('-')
        
        if len(account_parts) == 5:
            
            account, created = self.get_or_create(account_string=account)
            
            if created:
            
                account.agency, created = Agency.objects.get_or_create(code=int(account_parts[0]))
                
                account.account = account_parts[1]
                
                account.transmittal_code = int(account_parts[2])
                
                account.fund_code = int(account_parts[3])
                
                if len(account_parts[4]) == 3:
                    
                    try:
                        budget_function = BudgetFunction.objects.get(code=int(account_parts[4]))
                    
                        account.budget_function = budget_function
                    except: 
                        print 'unknown budget function: %s' % (int(account_parts[4]))
                        
                account.save()
             
            return account
        else:
            return None


class BudgetAccount(models.Model):
    
    account_string = models.CharField(max_length=255)
    
    agency = models.ForeignKey(Agency, null=True, blank=True)
    
    account = models.IntegerField(null=True, blank=True)
    
    budget_function = models.ForeignKey(BudgetFunction, null=True, blank=True)
    
    TRANSMITTAL_REGULAR = 0
    TRANSMITTAL_SUPPLEMENTAL = 1
    TRANSMITTAL_LEGISLATIVE = 2
    TRANSMITTAL_APPROPRIATIONS = 3
    TRANSMITTAL_PAYGO = 4
    TRANSMITTAL_RECISSION = 5
    TRANSMITTAL_RESERVED = 9
    
    TRANSMITTAL_OPTIONS = (
           (TRANSMITTAL_REGULAR, 'Regular budget schedules'),
           (TRANSMITTAL_SUPPLEMENTAL, 'Supplemental proposals'),
           (TRANSMITTAL_LEGISLATIVE, 'Legislative proposals requiring authorizing legislation that are not subject to pay-as-you-go (PAYGO)'),
           (TRANSMITTAL_APPROPRIATIONS, 'Appropriations language to be transmitted later; used when language for a significant policy proposal cannot be transmitted in the budget'),
           (TRANSMITTAL_PAYGO, 'Legislative proposals requiring authorizing legislation that have a PAYGO effect'),
           (TRANSMITTAL_RECISSION, 'Rescission proposal'),
           (TRANSMITTAL_RESERVED, 'Reserved for OMB use'))

    transmittal_code = models.IntegerField(choices=TRANSMITTAL_OPTIONS, null=True, blank=True)

    
    FUND_GENERAL = 1  
    FUND_SPECIAL = 2 
    FUND_PUBLIC  = 3 
    FUND_INTRAGOVERNMENTAL = 4 
    FUND_TRUST = 7 
    FUND_REVOLVING = 8  
    
    FUND_OPTIONS = (
            (FUND_GENERAL, 'General fund'),
            (FUND_SPECIAL, 'Special fund'),
            (FUND_PUBLIC, 'Public enterprise revolving fund'),
            (FUND_INTRAGOVERNMENTAL, 'Intragovernmental revolving or management fund'),
            (FUND_TRUST, 'Trust non-revolving fund'),
            (FUND_REVOLVING, 'Trust revolving fund'))

    fund_code = models.IntegerField(choices=FUND_OPTIONS, null=True, blank=True)

    objects = BudgetAccountManager()

