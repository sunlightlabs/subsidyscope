import re
from datetime import datetime
import csv

from django.db import models
from sectors.models import Sector, Subsector
from budget_accounts.models import BudgetAccount
from django.utils.encoding import smart_unicode
import helpers.unicode as un


class ProgramDescriptionManager(models.Manager):
    
    FIELD_MAPPINGS = [
        'program_title',
        'program_number',
        'popular_name',
        'federal_agency',
        'authorization',
        'objectives',
        'types_of_assistance',
        'uses_and_use_restrictions',
        'applicant_eligibility',
        'beneficiary_eligibility',
        'credentials_documentation',
        'preapplication_coordination',
        'application_procedure',    
        'award_procedure',
        'deadlines',
        'range_of_approval_disapproval_time',
        'appeals',
        'renewals',
        'formula_and_matching_requirements',
        'length_and_time_phasing_of_assistance',
        'reports',
        'audits',
        'records',
        'account_identification',
        'obligations',
        'range_and_average_of_financial_assistance',
        'program_accomplishments',
        'regulations_guidelines_and_literature',
        'regional_or_local_office',
        'headquarters_office',
        'web_site_address',
        'related_programs',
        'examples_of_funded_projects',
        'criteria_for_selecting_proposals',
        'published_date',
        'parent_shortname',
        'url',
        'recovery'
        'load_date'
    ]

    def import_programs(self, file):
        date = datetime.today()
        new_program_count = 0
        f = open(file, 'rU')
        this_version = int(file[-9:-4]) #pull the date off of the programs csv file


        reader = csv.reader(f)
        reader.next() # skip headers
        while True:
            try:
                row = reader.next()
            except:
                break

            if not row:
                break
            
            if len(row) == 0 or len(row) < 10:
                continue 

            program_number = row[1].strip()
            matching_programs = ProgramDescription.objects.filter(program_number=program_number)
           
            if len(matching_programs)==0:
                matching_program = ProgramDescription()
                new_program_count += 1
                print "new program: %s" % (program_number)
                
            else:
                matching_program = matching_programs[0]
    
        
            for (i,s) in enumerate(self.FIELD_MAPPINGS):
                
                try:
                    prepared_string = smart_unicode(un.kill_gremlins(row[i]))
                    setattr(matching_program, s, prepared_string)
                    if i == 1:
                        #we have the program vitals, save so we can use as foreign key for other attributes
                        matching_program.save()
                    
                except Exception, e:
                    continue

            matching_program.save()
        f.close()

        print "Run complete. \n%s new programs were added" % new_program_count
        
    

    def parseBudgetAccounts(self):
        
        import haystack
        haystack.sites.site.unregister(ProgramDescription)
        
        for program in self.all():
            if program.program_number == '10.001':
                print '10.001'
                
            program.parseBudgetAccounts()
     

class CFDATag(models.Model):
    def __unicode__(self):
        return self.tag_name
    class Meta:
        verbose_name = 'CFDA Program Tag'
    
    tag_name = models.CharField(max_length=255)
    search_default_enabled = models.BooleanField("Enabled for searches by default?")


class ProgramDescription(models.Model):

    def __unicode__(self):
        return "%s %s" % (self.program_number, self.program_title)
    class Meta:
        verbose_name = 'CFDA Program Description'
        ordering = ['program_number']

    program_number = models.CharField("Program number", max_length=7)
    program_title = models.CharField("Program title", max_length=255)
    sectors = models.ManyToManyField(Sector, blank=True)
    subsectors = models.ManyToManyField(Subsector, blank=True)
    program_note = models.TextField("Program note", default="", blank=True)
    federal_agency = models.TextField("Federal agency", blank=True, default="")
    major_agency = models.TextField("Major agency",blank=True,default="")
    minor_agency = models.TextField("Minor agency",blank=True,default="")
    authorization = models.TextField("Authorization",blank=True,default="")
    objectives = models.TextField("Objectives",blank=True,default="")
    types_of_assistance = models.TextField("Types of assistance",blank=True,default="")
    uses_and_use_restrictions = models.TextField("Uses and use restrictions",blank=True,default="")
    applicant_eligibility = models.TextField("Applicant eligibility",blank=True,default="")
    beneficiary_eligibility = models.TextField("Beneficiary eligibility",blank=True,default="")
    credentials_documentation = models.TextField("Credentials / documentation",blank=True,default="")
    preapplication_coordination = models.TextField("Preapplication coordination",blank=True,default="")
    application_procedure = models.TextField("Application procedure",blank=True,default="")
    award_procedure = models.TextField("Award procedure",blank=True,default="")
    deadlines = models.TextField("Deadlines",blank=True,default="")
    range_of_approval_disapproval_time = models.TextField("Range of approval / disapproval time",blank=True,default="")
    appeals = models.TextField("Appeals",blank=True,default="")
    renewals = models.TextField("Renewals",blank=True,default="")
    formula_and_matching_requirements = models.TextField("Formula and matching requirements",blank=True,default="")
    length_and_time_phasing_of_assistance = models.TextField("Length and time phasing of assistance",blank=True,default="")
    reports = models.TextField("Reports",blank=True,default="")
    audits = models.TextField("Audits",blank=True,default="")
    records = models.TextField("Records",blank=True,default="")
    account_identification = models.TextField("Account identification",blank=True,default="")
    obligations = models.TextField("Obligations",blank=True,default="")
    range_and_average_of_financial_assistance = models.TextField("Range and average of financial assistance",blank=True,default="")
    program_accomplishments = models.TextField("Program accomplishments",blank=True,default="")
    regulations_guidelines_and_literature = models.TextField("Regulations guidelines and literature",blank=True,default="")
    regional_or_local_office = models.TextField("Regional or local office",blank=True,default="")
    headquarters_office = models.TextField("Headquarters office",blank=True,default="")
    web_site_address = models.TextField("Web site address",blank=True,default="")
    related_programs = models.TextField("Related programs",blank=True,default="")
    examples_of_funded_projects = models.TextField("Examples of funded projects",blank=True,default="")
    criteria_for_selecting_proposals = models.TextField("Criteria for selecting proposals",blank=True,default="")

    recipient_type = models.ForeignKey('faads.RecipientType', blank=True, null=True)
    action_type = models.ForeignKey('faads.ActionType', blank=True, null=True)
    record_type = models.ForeignKey('faads.RecordType', blank=True, null=True)
    assistance_type = models.ForeignKey('faads.AssistanceType', blank=True, null=True)

    cfda_edition = models.IntegerField("CFDA Edition", blank=True, null=True)
    load_date = models.DateTimeField("Load Date", auto_now=True)    

    budget_accounts = models.ManyToManyField(BudgetAccount, blank=True, null=True)
    primary_tag = models.ForeignKey(CFDATag, blank=True, null=True, related_name='primary_tag')
    secondary_tags = models.ManyToManyField(CFDATag, blank=True, null=True, related_name='secondary_tags')

    objects = ProgramDescriptionManager()   
    

    def parseBudgetAccounts(self):
        
        accounts = re.findall('([0-9]{2,2}-[0-9]{4,4}-[0-9]{1,1}-[0-9]{1,1}-[0-9]{3,3})', self.account_identification)
        
        if accounts:
            for account_number in accounts:
                
                account = BudgetAccount.objects.createBudgetAccount(account_number.strip('.').strip())
                self.budget_accounts.add(account)
                self.save()
                account = None
        

    def short_description(self):
        
        if len(self.objectives) < 200:
            return self.objectives
        else:
            return self.objectives[:200] + '...'

        

class ProgramBudgetEstimateDescription(models.Model):
    
    program = models.ForeignKey(ProgramDescription)
    
    DATA_TYPE_AUTHORIZATION = 1
    DATA_TYPE_APPROPRIATION = 2
    DATA_TYPE_OBLIGATION = 3
    DATA_TYPE_ALLOCATION_APPORTIONMENT = 4
    DATA_TYPE_OTHER = 5
    
    DATA_TYPE_CHOICES = (
        (DATA_TYPE_AUTHORIZATION, 'Authorization'),
        (DATA_TYPE_APPROPRIATION, 'Appropriation'),
        (DATA_TYPE_OBLIGATION, 'Obligations'),
        (DATA_TYPE_ALLOCATION_APPORTIONMENT, 'Allocation/Apportionment'),
        (DATA_TYPE_OTHER, 'Other'))

    data_type = models.IntegerField("Data type", choices=DATA_TYPE_CHOICES)
    
    DATA_SOURCE_AGENCY = 1
    DATA_SOURCE_LEGISLATION = 2
    DATA_SOURCE_APPORTIONMENT_NOTICE = 3
    DATA_SOURCE_CFDA = 4
    DATA_SOURCE_OTHER = 5
    
    DATA_SOURCE_CHOICES = (
        (DATA_SOURCE_AGENCY, 'Agency'),
        (DATA_SOURCE_LEGISLATION, 'Legislation'),
        (DATA_SOURCE_APPORTIONMENT_NOTICE, 'Apportionment Notice'),
        (DATA_SOURCE_CFDA, 'CFDA'),
        (DATA_SOURCE_OTHER, 'Other'))
    
    data_source = models.IntegerField("Data source", choices=DATA_SOURCE_CHOICES)
    
    notes = models.TextField("Notes", blank=True,default="")
    
    citation = models.CharField("Citation URL", max_length=255, blank=True,default="")
    
 
    
class ProgramBudgetAnnualEstimate(models.Model):

    budget_estimate = models.ForeignKey(ProgramBudgetEstimateDescription)
    
    fiscal_year = models.IntegerField("Fiscal Year")
    
    annual_amount = models.DecimalField("Annual Amount", max_digits=15, decimal_places=2)
    
    
