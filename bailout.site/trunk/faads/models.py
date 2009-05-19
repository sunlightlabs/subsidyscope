from django.db import models
from decimal import Decimal
from cfda.models import ProgramDescription

class RawFAADSRecord(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'FAADS Record'
        # ordering = ['name'] 

    TYPE_OF_RECIPIENT_CHOICES = (
        (0, "State government"),
        (1, "County government"),
        (2, "City or township government"),
        (4, "Special district government"),
        (5, "Independent school district"),
        (6, "State controlled institution of higher education"),
        (11, "Indian tribe"),
        (12, "Other nonprofit"),
        (20, "Private higher education"),
        (21, "Individual"),
        (22, "Profit organization"),
        (23, "Small business"),
        (25, "All other")
    )
    
    TYPE_OF_ACTION_CHOICES = (
        ("A", "New assistance action"),
        ("B", "Continuation"),
        ("C", "Revision"),
        ("D", "Funding adjustment to completed project")        
    )
    
    TYPE_OF_ASSISTANCE_ACTION_CHOICES = (
        (2, "Block grant (A)"),
        (3, "Formula grant (A)"),
        (4, "Project grant (B)"),
        (5, "Cooperative agreement (B)"),
        (6, "Direct payment for specified use, as a subsidy or other non-reimbursable direct financial aid (C)"),
        (7, "Direct loan (D)"),
        (8, "Guaranteed/insured loan (F)"),
        (9, "Insurance (G)"),
        (10, "Direct payment with unrestricted use (D)"),
        (11, "Other reimbursable, contingent, intangible or indirect financial assistance"),    
    )
    
    RECORD_TYPE_CHOICES = (
        (1, "County aggregate reporting"),
        (2, "Action-by-action reporting")
    )
    
    CORRECTION_LATE_INDICATOR_CHOICES = (
        ('C', "Correction to a record reported in a prior quarter"),
        ('L', "Late reporting of an action occurring in a prior quarter")
    )

    cfda_program_number = models.CharField("CFDA Program Number", max_length=7)
    sai = models.CharField("State Application Identifier", max_length=20)
    recipient_name = models.CharField("Recipient Name", max_length=45)
    recipient_city_code = models.CharField("Recipient City Code", max_length=5, help_text="FIPS 55-3 place code")
    recipient_city_name = models.CharField("Recipient City Name", max_length=21)
    recipient_county_code = models.CharField("Recipient County Code", max_length=3, help_text="FIPS PUB 6-4")
    recipient_county_name = models.CharField("Recipient County Name", max_length=21)
    recipient_state_code = models.CharField("Recipient State Code", max_length=2, help_text="FIPS PUB 5-1")
    recipient_zip_code = models.CharField("Recipient Zip Code", max_length=9)
    type_of_recipient = models.IntegerField("Type of Recipient", choices=TYPE_OF_RECIPIENT_CHOICES)
    type_of_action = models.CharField("Type of Action", max_length=1, choices=TYPE_OF_ACTION_CHOICES)
    recipient_congressional_district = models.IntegerField("Recipient Congressional District")
    federal_agency_organizational_unit_code = models.CharField("Federal Agency/Organizational Unit Code", max_length=4)
    federal_award_identifier_number_core = models.CharField("Federal Award Identifier Number (core number)", max_length=16)
    federal_award_identifier_number_modification = models.CharField("Federal Award Identifier Number (modification number)", max_length=4)
    federal_funding_sign = models.CharField("Federal Funding Sign", max_length=1)
    federal_funding_amount = models.IntegerField("Federal Funding Amount")
    non_federal_funding_sign = models.CharField("Non-Federal Funding Sign", max_length=1)
    non_federal_funding_amount = models.IntegerField("Non-Federal Funding Amount")
    total_funding_sign = models.CharField("Total Funding Sign", max_length=1)
    total_funding_amount = models.IntegerField("Total Funding Amount")
    obligation_action_date = models.DateField("Obligation/Action Date")
    starting_date = models.DateField("Starting Date", blank=True)
    ending_date = models.DateField("Ending Date", blank=True)
    type_of_assistance_action = models.IntegerField("Type of Assistance Action", choices=TYPE_OF_ASSISTANCE_ACTION_CHOICES)
    record_type = models.IntegerField("Record Type", choices=RECORD_TYPE_CHOICES)
    correction_late_indicator = models.CharField("Correction/Late Indicator", max_length=1, choices=CORRECTION_LATE_INDICATOR_CHOICES)
    fiscal_year_and_quarter_correction = models.CharField("Fiscal Year and Quarter Correction (YYYYQ)", max_length=5)
    principal_place_of_performance_code_state = models.CharField("Principal Place of Performance Code (State)", max_length=2)
    principal_place_of_performance_code_county_or_city = models.CharField("Principal Place of Performance Code (County or City)", max_length=5)
    principal_place_of_performance_state = models.CharField("Principal Place of Performance", max_length=25)
    principal_place_of_performance_county_or_city = models.CharField("Principal Place of Performance", max_length=25)
    cfda_program_title = models.CharField("CFDA Program Title", max_length=74)
    federal_agency_name = models.CharField("Federal Agency Name", max_length=72)
    state_name = models.CharField("State Name", max_length=25)
    project_description = models.TextField("Project Description")
    
    def extract_faads_field(self, line, fieldname):
        record_positions = self.SOURCE_FILE_RECORD_POSITIONS[fieldname]
        transform = lambda x: x.strip()
        if len(record_positions)>2 and callable(record_positions[2]):
            transform = record_positions[2]
        return transform(line[(record_positions[0]-1):(record_positions[1])])
       
    
    def process_faads_line(self, line):
        for field in self._meta.fields:
            if field.name in self.SOURCE_FILE_RECORD_POSITIONS:                    
                setattr(self, field.name, self.extract_faads_field(line, field.name))
                
                    
        

    SOURCE_FILE_RECORD_POSITIONS = {
        "cfda_program_number": (1, 7, lambda x: ProgramDescription.objects.filter(program_number=Decimal(x.strip()))[0]), 
        "sai": (8, 27), 
        "recipient_name": (28, 72), 
        "recipient_city_code": (73, 77), 
        "recipient_city_name": (78, 98),
        "recipient_county_code": (99, 101), 
        "recipient_county_name": (102, 122), 
        "recipient_state_code": (123, 124), 
        "recipient_zip_code": (125, 133), 
        "type_of_recipient": (134, 135), 
        "type_of_action": (136, 136), 
        "recipient_congressional_district": (137, 138), 
        "federal_agency_organizational_unit_code": (139, 142), 
        "federal_award_identifier_number_core": (143, 158), 
        "federal_award_identifier_number_modification": (159, 162), 
        "federal_funding_sign": (163, 163), 
        "federal_funding_amount": (164, 173), 
        "non_federal_funding_sign": (174, 174), 
        "non_federal_funding_amount": (175, 184), 
        "total_funding_sign": (185, 185), 
        "total_funding_amount": (186, 196), 
        "obligation_action_date": (197, 204), 
        "starting_date": (205, 212), 
        "ending_date": (213, 220), 
        "type_of_assistance_action": (221, 222), 
        "record_type": (223, 223), 
        "correction_late_indicator": (224, 224), 
        "fiscal_year_and_quarter_correction": (225, 229), 
        "principal_place_of_performance_code_state": (230, 231), 
        "principal_place_of_performance_code_county_or_city": (232, 236), 
        "principal_place_of_performance_state": (237, 261), 
        "principal_place_of_performance_county_or_city": (262, 286),     
        "cfda_program_title": (287, 360), 
        "federal_agency_name": (361, 432), 
        "state_name": (433, 457), 
        "project_description": (458, 606), 
    }