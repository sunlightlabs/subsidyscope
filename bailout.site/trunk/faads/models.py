from django.db import models
from decimal import Decimal
from cfda.models import ProgramDescription
from geo.models import 
from decimal import Decimal
import sys
import MySQLdb

def generate_model_entries(obj):
    obj.objects.all().delete()
    for code,name in obj.OPTIONS:
        x = obj()
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
        (12, "Unknown")
    )


class ActionType(models.Model):
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = 'Action Type'
    code = models.CharField("Character Code", max_length=1, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=False)     

    OPTIONS = (
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

    OPTIONS = (
         (1, "County aggregate reporting"),
         (2, "Action-by-action reporting")
     )    



class Record(models.Model):
    def __unicode__(self):
        return "%s - %s - %s" % (self.fiscal_year, self.federal_funding_amount, self.recipient_name)
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
    recipient_type = models.ForeignKey(RecipientType, blank=True, null=True)
    
    recipient_state = models.ForeignKey(State)
    recipient_county = models.ForeignKey(County)
    
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
    assistance_type = models.ForeignKey(AssistanceType, blank=True, null=True)
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
    recipient_congressional_district = models.CharField("Recipient Congressional District", max_length=4, blank=True, default='')
    major_agency_category = models.CharField("Major Agency Category", max_length=2, blank=True, default='')
    mod_name = models.CharField("Modified(?) Name", max_length=45, blank=True, default='')
    recipient_id = models.IntegerField("Recipient ID", max_length=11, blank=True, null=True)
    lookup_record_id = models.IntegerField("Lookup Record ID", max_length=20, blank=True, null=True)
    lookup_recipient_id = models.IntegerField("Lookup Recipient ID", max_length=20, blank=True, null=True)
    business_identifier = models.CharField("Business Identifier", max_length=3, blank=True, default='')
    rec_flag = models.CharField("Recovery(?) Flag", max_length=1, blank=True, default='')
    

class FAADSLoader(object):
    """docstring for FAADSLoader"""

    MYSQL = {
        'user': 'root',
        'password': '',
        'database': 'usaspending',
        'host': '127.0.0.1',
        'port': 3306
    }

    def __init__(self):
        super(FAADSLoader, self).__init__()        

        # cache record type objects            
        TODO = (ActionType, AssistanceType, RecordType, RecipientType)
        for t in TODO:
            setattr(self, t.__name__, {})
            for i in t.OPTIONS:
                i_code = i[0]
                match = t.objects.filter(code=i_code)
                if len(match)==1:
                    getattr(self,t.__name__)[i_code] = match[0]
    
        # cache CFDA program objects
        self.cfda_programs = {}
        for p in ProgramDescription.objects.filter(sectors__name__icontains='transportation'):
            self.cfda_programs[p.program_number] = p            
        
    
        self.FIELD_MAPPING = {
        #   'django field name': 'FAADS field name' OR callable that returns value when passed row
            'fyq': 'fyq',
            'cfda_program': (self.lookup_cfda_program, {}),
            'sai_number': 'sai_number',
            'recipient_name': 'recipient_name',
            'recipient_city_code': 'recipient_city_code',
            'recipient_city_name': 'recipient_city_name',
            'recipient_county_code': 'recipient_county_code',
            'recipient_county_name': 'recipient_county_name',
            'recipient_state_code': 'recipient_state_code',
            'recipient_zip_code': 'recipient_zip',
            'recipient_type': (self.lookup_fk_field, {'type_name': 'RecipientType', 'code_extractor': self.extract_recipient_type_safely }),
            'action_type': (self.lookup_fk_field, {'type_name': 'ActionType', 'code_extractor': lambda x: x.get('action_type')}),
            'recipient_congressional_district': 'recipient_cong_district',
            'agency_code': 'agency_code',
            'federal_award_identifier_number_core': 'federal_award_id',
            'federal_award_identifier_number_modification': 'federal_award_mod',
            'federal_funding_amount': 'fed_funding_amount',
            'non_federal_funding_amount': 'non_fed_funding_amount',
            'total_funding_amount': 'total_funding_amount',
            'obligation_action_date': (self.extract_date, {'date_field_name': 'obligation_action_date'}),
            'starting_date': (self.extract_date, {'date_field_name': 'starting_date'}),
            'ending_date': (self.extract_date, {'date_field_name': 'ending_date'}),
            'assistance_type': (self.lookup_fk_field, {'type_name': 'AssistanceType', 'code_extractor': self.extract_assistance_type_safely }),
            'record_type': (self.lookup_fk_field, {'type_name': 'RecordType', 'code_extractor': lambda x: int(x.get('record_type', -1))}),
            'correction_late_indicator': 'correction_late_ind',
            'fyq_correction': 'fyq_correction',
            'principal_place_code': 'principal_place_code',
            'principal_place_state': 'principal_place_state',
            'principal_place_state_code': 'principal_place_state_code',
            'principal_place_county_or_city': 'principal_place_cc',
            'principal_place_zip_code': (self.make_null_emptystring, {'field_name': 'principal_place_zip'}),
            'principal_place_congressional_district': (self.make_null_emptystring, {'field_name': 'principal_place_cd'}),
            'cfda_program_title': 'cfda_program_title',
            'agency_name': 'agency_name',
            'recipient_state_name': 'recipient_state_name',
            'project_description': 'project_description',
            'duns_number': (self.make_null_emptystring, {'field_name': 'duns_no'}),
            'duns_confidence_code': (self.make_null_emptystring, {'field_name': 'duns_conf_code'}),
            'progsrc_agen_code': (self.make_null_emptystring, {'field_name': 'progsrc_agen_code'}),
            'progsrc_acnt_code': (self.make_null_emptystring, {'field_name': 'progsrc_acnt_code'}),
            'progsrc_subacnt_code': (self.make_null_emptystring, {'field_name': 'progsrc_subacnt_code'}),
            'recipient_address_1': (self.make_null_emptystring, {'field_name': 'receip_addr1'}),
            'recipient_address_2': (self.make_null_emptystring, {'field_name': 'receip_addr2'}),
            'recipient_address_3': (self.make_null_emptystring, {'field_name': 'receip_addr3'}),
            'face_loan_guran': 'face_loan_guran',
            'orig_sub_guran': 'orig_sub_guran',
            'parent_duns': (self.make_null_emptystring, {'field_name': 'parent_duns_no'}),
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
            'business_identifier': (self.make_null_emptystring, {'field_name': 'business_identifier'}),
            'rec_flag': 'rec_flag',
        }
    
    def reset_faads_import(self):
        # reload FK models
        generate_model_entries(ActionType)
        generate_model_entries(RecipientType)
        generate_model_entries(AssistanceType)
        generate_model_entries(RecordType)
        Record.objects.all().delete()

    
    def extract_recipient_type_safely(self,x):
        r = x.get('recipient_type')
        if r is None or r=='':
            return None
        else:
            return int(r)
    
    def extract_assistance_type_safely(self,x):
        r = x.get('assistance_type')
        if r is None or r=='':
            return None
        else:
            return int(r)
    
    def make_null_emptystring(self, *args, **kwargs):
        record = args[0]
        field_name = kwargs['field_name']
        if record[field_name] is None:
            return ''
        else:
            return record[field_name]

    
    def extract_date(self, *args, **kwargs):
        record = args[0]
        date_raw = record[kwargs['date_field_name']]
        try:
            return datetime.strptime(date_raw, '%Y-%m-%d')
        except Exception, e:
            return None

    def lookup_cfda_program(self, *args, **kwargs):
        record = args[0]
        try:
            cfda = Decimal(record['cfda_program_num'])
            return self.cfda_programs.get(cfda, False)
        except Exception, e:
            return False
        
    
    def lookup_fk_field(self, *args, **kwargs):
        record = args[0]
        code_extractor = kwargs.get('code_extractor')
        value = code_extractor(record)
        
        type_name = kwargs.get('type_name')
        
        lookup_object = getattr(self, type_name, None)
        if lookup_object is not None:
            return lookup_object.get(value, False)
        else:
            return False

    def process_record(self, faads_record):
        django_record = Record()
        
        failed_fields = []
        for attrname in self.FIELD_MAPPING:            
            grabber = self.FIELD_MAPPING[attrname]
            if type(grabber)==tuple and callable(grabber[0]):
                func = grabber[0]
                args = [faads_record]
                kwargs = grabber[1]
                extracted_value = func(faads_record, *args, **kwargs)
                if extracted_value is not False:
                    setattr(django_record, attrname, extracted_value)
                else:
                    failed_fields.append(attrname)                    
            else:
                setattr(django_record, attrname, faads_record.get(grabber))

        if len(failed_fields):
            sys.stderr.write("%d: failed to extract field(s) %s\n" % (faads_record['record_id'], ', '.join(failed_fields)))

        try:
            django_record.save()        
        except Exception, e:
            sys.stderr.write("%d: failed to save / %s\n" % (faads_record['record_id'], str(e)))

                    
    def do_import(self, table_name='faads_main_sf'):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(record_id) AS max_record_id FROM faads_record;")
        row = cursor.fetchone()
        max_record_id = row[0]
        if max_record_id is None:
            max_record_id = 0
        
        conn = MySQLdb.connect(host=FAADSLoader.MYSQL['host'], user=FAADSLoader.MYSQL['user'], passwd=FAADSLoader.MYSQL['password'], db=FAADSLoader.MYSQL['database'], port=FAADSLoader.MYSQL['port'], cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        sql = "SELECT * FROM %s WHERE TRIM(cfda_program_num) IN ('%s') AND record_id>%d ORDER BY record_id ASC LIMIT 10000" % (table_name, "','".join(map(lambda x: str(x), self.cfda_programs.keys())), max_record_id)
        print "Executing query"
        cursor.execute(sql)
        i = 0
        while True:
            sys.stdout.write("Entering loop... ")
            row = cursor.fetchone()
            if row is None:
                break
            else:
                sys.stdout.write("Processing row... ")
                self.process_record(row)
            i = i + 1
            sys.stdout.write("Finished iteration %d\n" % i)

        cursor.close()
        conn.close()
        
        
  
    



