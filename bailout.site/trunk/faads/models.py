from django.db import models
from decimal import Decimal
from cfda.models import ProgramDescription

def generate_model_entries(obj):
    type(obj).objects.all().delete()
    for code,name in obj.OPTIONS:
        x = type(obj)()
        x.code = code
        x.name = name
        x.save()

class AssistanceType(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Assistance Type'
    code = models.IntegerField("Numeric Code", max_length=2, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=False)    
    generate_entries = generate_model_entries

    OPTIONS = (
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


class ActionType(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Action Type'
    code = models.IntegerField("Numeric Code", max_length=2, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=False)    
    generate_entries = generate_model_entries    

    TYPE_OF_ACTION_CHOICES = (
        ("A", "New assistance action"),
        ("B", "Continuation"),
        ("C", "Revision"),
        ("D", "Funding adjustment to completed project")        
    )


class RecipientType(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Recipient Type'    
    code = models.IntegerField("Numeric Code", max_length=2, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=False)

    generate_entries = generate_model_entries

    OPTIONS = (
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


class RecordType(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Record Type'    
    code = models.IntegerField("Numeric Code", max_length=2, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=False)

    generate_entries = generate_model_entries

    OPTIONS = (
         (1, "County aggregate reporting"),
         (2, "Action-by-action reporting")
     )    



class Record(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'FAADS Record'
    
    fyq = models.CharField("FYQ", max_length=8, blank=True, default='')
    cfda_program = models.ForeignKey(ProgramDescription)
    sai_number = models.CharField("State Application Identifier", max_length=20, blank=True, default='')
    recipient_name = models.CharField("Recipient Name", max_length=45, blank=True, default='')
    recipient_city_code = models.CharField("Recipient City Code", max_length=5, blank=True, default='', help_text="FIPS 55-3 place code") # NORMALIZE 
    recipient_city_name = models.CharField("Recipient City Name", max_length=21, blank=True, default='') 
    recipient_county_code = models.CharField("Recipient County Code", max_length=3, blank=True, default='', help_text="FIPS PUB 6-4") # NORMALIZE
    recipient_county_name = models.CharField("Recipient County Name", max_length=21, blank=True, default='')
    recipient_state_code = models.CharField("Recipient State Code", max_length=2, blank=True, default='', help_text="FIPS PUB 5-1") # NORMALIZE
    recipient_zip_code = models.CharField("Recipient Zip Code", max_length=9, blank=True, default='')
    recipient_type = models.ForeignKey(RecipientType)
    action_type = models.ForeignKey(ActionType)
    recipient_congressional_district = models.IntegerField("Recipient Congressional District", blank=True, null=True)
    agency_code = models.CharField("Agency Code", max_length=4, blank=True, default='')
    federal_award_identifier_number_core = models.CharField("Federal Award Identifier Number (core number)", max_length=16, blank=True, default='')
    federal_award_identifier_number_modification = models.CharField("Federal Award Identifier Number (modification number)", max_length=4, blank=True, default='')
    federal_funding_amount = models.DecimalField("Federal Funding Amount", max_digits=15, decimal_places=2, blank=True, null=True)
    non_federal_funding_amount = models.DecimalField("Non-federal Funding Amount", max_digits=15, decimal_places=2, blank=True, null=True)
    total_funding_amount = models.DecimalField("Total Funding Amount", max_digits=15, decimal_places=2, blank=True, null=True)
    obligation_action_date = models.DateField("Obligation Action Date", blank=True, null=True)
    starting_date = models.DateField("Starting Date", blank=True, null=True)
    ending_date = models.DateField("Ending Date", blank=True, null=True)
    assistance_type = models.ForeignKey(AssistanceType)
    record_type = models.ForeignKey(RecordType)
    correction_late_indicator = models.CharField("Correction/Late Indicator", max_length=1, blank=True, default='')
    fyq_correction = models.CharField("FYQ Correction", max_length=5, blank=True, default='')
    principal_place_code = models.CharField("Principal Place of Performance Code", max_length=7, blank=True, default='') # NORMALIZE
    principal_place_state = models.CharField("Principal Place of Performance State", max_length=25, blank=True, default='') # NORMALIZE
    principal_place_state_code = models.CharField("Principal Place of Performance State Code", max_length=2, blank=True, default='') # NORMALIZE
    principal_place_county_or_city = models.CharField("Principal Place of Performance County/City", max_length=25, blank=True, default='') # NORMALIZE
    principal_place_zip_code = models.CharField("Principal Place of Performance Zip Code", max_length=9, blank=True, default='') # NORMALIZE
    principal_place_congressional_district = models.CharField("Principal Place Congressional District", max_length=2, blank=True, default='') # NORMALIZE
    cfda_program_title = models.CharField("CFDA Program Title", max_length=74, blank=True, default='')
    agency_name = models.CharField("Federal Agency Name", max_length=72, blank=True, default='')
    recipient_state_name = models.CharField("Recipient State Name", max_length=25, blank=True, default='')
    project_description = models.TextField("Project Description", max_length=149, blank=True, default='')
    duns_number = models.TextField("DUNS Number", max_length=13, blank=True, default='')
    duns_confidence_code = models.TextField("DUNS Confidence Code", max_length=2, blank=True, default='')
    progsrc_agen_code = models.CharField("Program Source/Treasury Account Symbol: Agency Code", max_length=2, blank=True, default='')
    progsrc_acnt_code = models.CharField("Program Source/Treasury Account Symbol: Account Code", max_length=4, blank=True, default='')
    progsrc_subacnt_code = models.CharField("Program Source/Treasury Account Symbol: Sub-Account Code", max_length=3, blank=True, default='')
    recipient_address_1 =  models.CharField("Recipient Address 1", max_length=35, blank=True, default='')
    recipient_address_2 =  models.CharField("Recipient Address 2", max_length=35, blank=True, default='')
    recipient_address_3 =  models.CharField("Recipient Address 3", max_length=35, blank=True, default='')        
    face_loan_guran = models.DecimalField("Face Value of Direct Loan/Loan Guarantee", max_digits=15, decimal_places=2, blank=True, null=True)
    orig_sub_guran = models.DecimalField("Original Subsidy Cost of the Direct Loan/Loan Guarantee", max_digits=15, decimal_places=2, blank=True, null=True)
    parent_duns =  models.CharField("Parent DUNS", max_length=13, blank=True, default='')
    record_id = models.IntegerField("Record ID", max_length=20, blank=True, null=True)
    fiscal_year = models.IntegerField("Fiscal Year", max_length=6, blank=True, null=True)
    award_id = models.IntegerField("Award ID", max_length=11, blank=True, null=True)
    recipient_category_type = models.CharField("Recipient Category Type", max_length=1, blank=True, default='')
    asistance_category_type = models.CharField("Assistance Category Type", max_length=1, blank=True, default='')
    recipient_congressional_district = models.CharField("Recipient Congressional District", max_length=3, blank=True, default='')
    major_agency_category = models.CharField("Major Agency Category", max_length=2, blank=True, default='')
    mod_name = models.CharField("Modified(?) Name", max_length=45, blank=True, default='')
    recipient_id = models.IntegerField("Recipient ID", max_length=11, blank=True, null=True)
    lookup_record_id = models.IntegerField("Lookup Record ID", max_length=20, blank=True, null=True)
    lookup_recipient_id = models.IntegerField("Lookup Recipient ID", max_length=20, blank=True, null=True)
    business_identifier = models.CharField("Business Identifier", max_length=3, blank=True, default='')
    rec_flag = models.CharField("Recovery(?) Flag", max_length=1, blank=True, default='')
    
    field_mapping = [
    #   'django field name': 'FAADS field name' OR callable that returns value when passed row
        'fyq': 'fyq',
        'cfda_program': 'cfda_program_num',
        'sai_number': 'sai_number',
        'recipient_name': 'recipient_name',
        'recipient_city_code': 'recipient_city_code',
        'recipient_city_name': 'recipient_city_name',
        'recipient_county_code': 'recipient_county_code',
        'recipient_county_name': 'recipient_county_name',
        'recipient_state_code': 'recipient_state_code',
        'recipient_zip_code': 'recipient_zip',
        'recipient_type': 'recipient_type', # NEED LAMBDA
        'action_type': 'action_type', # NEED LAMBDA
        'recipient_congressional_district': 'recipient_cong_district',
        'agency_code': 'agency_code',
        'federal_award_identifier_number_core': 'federal_award_id',
        'federal_award_identifier_number_modification': 'federal_award_mod',
        'federal_funding_amount': 'fed_funding_amount',
        'non_federal_funding_amount': non_fed_funding_amount'',
        'total_funding_amount': 'total_funding_amount',
        'obligation_action_date': 'obligation_action_date', # NEED DATE LAMBDA
        'starting_date': 'starting_date', # NEED DATE LAMBDA
        'ending_date': 'ending_date', # NEED DATE LAMBDA
        'assistance_type': 'assistance_type',
        'record_type': 'record_type',
        'correction_late_indicator': 'correction_late_ind',
        'fyq_correction': 'fyq_correction',
        'principal_place_code': 'principal_place_code',
        'principal_place_state': 'principal_place_state',
        'principal_place_state_code': 'principal_place_state_code',
        'principal_place_county_or_city': 'principal_place_cc',
        'principal_place_zip_code': 'principal_place_zip',
        'principal_place_congressional_district': 'principal_place_cd',
        'cfda_program_title': 'cfda_program_title',
        'agency_name': 'agency_name',
        'recipient_state_name': 'recipient_state_name',
        'project_description': 'project_description',
        'duns_number': 'duns_no',
        'duns_confidence_code': 'duns_conf_code',
        'progsrc_agen_code': 'progsrc_agen_code',
        'progsrc_acnt_code': 'progsrc_acnt_code',
        'progsrc_subacnt_code': 'progsrc_subacnt_code',
        'recipient_address_1': 'receip_addr1',
        'recipient_address_2': 'receip_addr2',
        'recipient_address_3': 'receip_addr3',
        'face_loan_guran': 'face_loan_guran',
        'orig_sub_guran': 'orig_sub_guran',
        'parent_duns': 'parent_duns_no',
        'record_id': 'record_id',
        'fiscal_year': 'fiscal_year',
        'award_id': 'award_id',
        'recipient_category_type': 'recip_cat_type',
        'asistance_category_type': 'asst_cat_type',
        'recipient_congressional_district': 'recipient_cd',
        'major_agency_category': 'maj_agency_cat',
        'mod_name': 'mod_name',
        'recipient_id': 'recip_id',
        'lookup_record_id': 'lookup_record_id',
        'lookup_recipient_id': 'lookup_recip_id',
        'business_identifier': 'business_identifier',
        'rec_flag': 'rec_flag',
    ]
    

    # # DEPRECATED -- ONLY APPLICABLE TO CENSUS FAADS FORMAT
    #    
    # def extract_faads_field(self, line, fieldname):
    #     record_positions = self.SOURCE_FILE_RECORD_POSITIONS[fieldname]
    #     transform = lambda x: x.strip()
    #     if len(record_positions)>2 and callable(record_positions[2]):
    #         transform = record_positions[2]
    #     return transform(line[(record_positions[0]-1):(record_positions[1])])
    #    
    # 
    # def process_faads_line(self, line):
    #     for field in self._meta.fields:
    #         if field.name in self.SOURCE_FILE_RECORD_POSITIONS:                    
    #             setattr(self, field.name, self.extract_faads_field(line, field.name))
    #             
    # 
    # SOURCE_FILE_RECORD_POSITIONS = {
    #     "cfda_program_number": (1, 7, lambda x: ProgramDescription.objects.filter(program_number=Decimal(x.strip()))[0]), 
    #     "sai": (8, 27), 
    #     "recipient_name": (28, 72), 
    #     "recipient_city_code": (73, 77), 
    #     "recipient_city_name": (78, 98),
    #     "recipient_county_code": (99, 101), 
    #     "recipient_county_name": (102, 122), 
    #     "recipient_state_code": (123, 124), 
    #     "recipient_zip_code": (125, 133), 
    #     "type_of_recipient": (134, 135), 
    #     "type_of_action": (136, 136), 
    #     "recipient_congressional_district": (137, 138), 
    #     "federal_agency_organizational_unit_code": (139, 142), 
    #     "federal_award_identifier_number_core": (143, 158), 
    #     "federal_award_identifier_number_modification": (159, 162), 
    #     "federal_funding_sign": (163, 163), 
    #     "federal_funding_amount": (164, 173), 
    #     "non_federal_funding_sign": (174, 174), 
    #     "non_federal_funding_amount": (175, 184), 
    #     "total_funding_sign": (185, 185), 
    #     "total_funding_amount": (186, 196), 
    #     "obligation_action_date": (197, 204), 
    #     "starting_date": (205, 212), 
    #     "ending_date": (213, 220), 
    #     "type_of_assistance_action": (221, 222), 
    #     "record_type": (223, 223), 
    #     "correction_late_indicator": (224, 224), 
    #     "fiscal_year_and_quarter_correction": (225, 229), 
    #     "principal_place_of_performance_code_state": (230, 231), 
    #     "principal_place_of_performance_code_county_or_city": (232, 236), 
    #     "principal_place_of_performance_state": (237, 261), 
    #     "principal_place_of_performance_county_or_city": (262, 286),     
    #     "cfda_program_title": (287, 360), 
    #     "federal_agency_name": (361, 432), 
    #     "state_name": (433, 457), 
    #     "project_description": (458, 606), 
    # }

    



