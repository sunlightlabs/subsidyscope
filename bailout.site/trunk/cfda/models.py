from django.db import models
import sectors.models

class ProgramDescription(models.Model):

    def __unicode__(self):
        return "%s %s" % (self.program_number, self.program_title)
    class Meta:
        verbose_name = 'CFDA Program Description'
        ordering = ['program_number']

    program_number = models.DecimalField("Program number", max_digits=7, decimal_places=3)
    program_title = models.CharField("Program title", max_length=255)
    sectors = models.ManyToManyField(sectors.models.Sector, blank=True)
    program_note = models.TextField("Program note", default="", blank=True)
    federal_agency = models.TextField("Federal agency", blank=True, default="")
    major_agency = models.TextField("Major agency",blank=True,default="")
    minor_agency = models.TextField("Minor agency",blank=True,default="")
    authorization = models.TextField("Authorization",blank=True,default="")
    objectives = models.TextField("Objectives",blank=True,default="")
    types_of_assistance = models.CharField("Types of assistance",blank=True,default="", max_length=300)
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
    cfda_edition = models.IntegerField("CFDA Edition")

    def short_description(self):
        
        if len(self.objectives) < 200:
            return self.objectives
        else:
            return self.objectives[:200] + '...'
        
    