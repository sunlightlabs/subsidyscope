from django.db import models
from django.db.models import Max
from sectors.models import Sector, Subsector
import pg
import sys
from geo.models import *
import csv
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class ExtentCompetedMapper(object):
    # (code, title, description, considered subsidy?)
    CODES = (
        ('A', 'Full and Open Competition', 'Report this code if the action resulted from an award pursuant to FAR 6.102(a) - sealed bid, FAR 6.102(b) - competitive proposal, FAR 6.102(c) - Combination, or any other competitive method that did not exclude sources of any type', False),
        ('B', 'Not Available for Competition', 'Select this code when the contract is not available for competition', True),
        ('C', 'Not Competed', 'Select this code when the contract is not competed.', True),
        ('D', 'Full and Open Competition after exclusion of sources', 'Select this code when some sources are excluded before competition', True),
        ('E', 'Follow On to Competed Action', 'Select this code when the action is a follow on to an existing competed contract. FAR 6.302-1. This code is not valid for base documents signed after 10/31/2009.', True),
        ('F', 'Competed under SAP', 'Select this code when the action is competed under the Simplified Acquisition Threshold. This code is valid for DoD effective 10/31/2009.', False),
        ('G', 'Not Competed under SAP', 'Select this code when the action is NOT competed under the Simplified Acquisition Threshold. This code is valid for DoD effective 10/31/2009.', True),
        ('CDO', 'Competitive Delivery Order', 'Apply to Full and Open Competition pursuant to FAR 6.1 and only apply to Delivery Orders) Report this code if the IDV Type is a Federal Schedule. Report this code when the Order delivery/task order award was made pursuant to a process that permitted each contract awardee a fair opportunity to be considered. See FAR Part 16.505(b)(1). Report this code if the action is for the award of a multiple award schedule or an order against a multiple award schedule pursuant to FAR 6.102(d)(3) and the applicable provisions referenced there under. This code is not valid for base documents signed after 10/31/2009.', False),
        ('NDO', 'Non-Competitive Delivery Order', 'Report this code when competitive procedures are not used in awarding the delivery order for a reason not included above (when the action was non-competitive. This code is not valid for base documents signed after 10/31/2009.', True)
    ) # add new codes to end of list
    
    def __init__(self):
        self._lookup = {}
        self._reverse_lookup = {}    
        for i,code in enumerate(self.CODES):
            self._lookup[code[0]] = (i+1)
            self._reverse_lookup[(i+1)] = code[0]

    def assign_index(self, code):
        return self._lookup.get(code, 0)

class NAICSCodeManager(models.Manager):

    def load_naics(self, infile=None):
        if not infile:
            f = csv.reader(open("data/naics/naics_codes.csv"))
        else:
            f = csv.reader(open(infile))

        f.next() #header line
        for l in f:
            code = l[1]
            desc = l[2]

            try:
                code = int(code)
            except:
                print "%s is not valid" % code
                
                continue #not a valid code

            print code     

            try:
                n = NAICSCode.objects.get(code=code)

            except ObjectDoesNotExist as e:
                n = NAICSCode(code=code, name=desc)

            if len(str(code)) > 2:
                parent_code = int(str(code)[:2])
                try:
                    n.parent_code = NAICSCode.objects.get(code=parent_code)
                
                except ObjectDoesNotExist:
                    pc = NAICSCode(code=parent_code)
                    pc.save()
                    n.parent_code = pc
            n.name = desc
            print n
            n.save()


class NAICSCode(models.Model):
    def __unicode__(self):
        if self.code and self.name:
            return "%s - %s" % (self.code, self.name)
        else:
            return self.code
        
    class Meta:
        verbose_name = 'NAICS Code'
        
    code = models.IntegerField("Numeric Code", primary_key=True, max_length=6, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=True, default='')

    sectors = models.ManyToManyField(Sector, blank=True)
    subsectors = models.ManyToManyField(Subsector, blank=True)

    parent_code = models.ForeignKey('NAICSCode', blank=True, null=True)
    objects = NAICSCodeManager()

class ProductOrServiceCodeManager(models.Manager):

    def load_psc(self, infile=None):
        if not infile:
            f = csv.reader(open("data/psc/psc_codes.csv"))
        else:
            f = csv.reader(open(infile))

        f.next() #header line
        for l in f:
            code = l[0]
            desc = l[1]
            try:
                p = ProductOrServiceCode.objects.get(code=code, name=desc)

            except ObjectDoesNotExist:
                p = ProductOrServiceCode(code=code, name=desc)
                p.save()

class ProductOrServiceCode(models.Model):
    def __unicode__(self):
        if self.code and self.name:
            return "%s - %s" % (self.code, self.name)
        else:
            return self.code

    class Meta:
        verbose_name = 'PSC Code'

    code = models.CharField("Numeric Code", max_length=5, primary_key=True, blank=False)
    name = models.CharField("Descriptive Name", max_length=255, blank=True, default='')    

    sectors = models.ManyToManyField(Sector, blank=True)
    subsectors = models.ManyToManyField(Subsector, blank=True)

    objects = ProductOrServiceCodeManager()


class CodeMatcher(object):
    """ Matches NAICS/PSC codes; inserts new ones as needed."""
    # We do this here rather than with Django convenience methods so that the lookup table stays in memory. 

    def __init__(self, target_class):
        self.target_class = target_class
        self.lookup = {}
        for x in self.target_class.objects.all():
            self.lookup[x.code] = x                        

    def _clean(self, code):
        return code.strip().upper()
            
    def match(self, code, name=''):
        code = self._clean(code)
        
        m = self.lookup.get(code, None)
        if m is None:
            m = self.target_class()
            m.code = code
            m.name = name
            m.save()
            self.lookup[m.code] = m

        return m
            
        

class FPDSRecord(models.Model):
    def __unicode__(self):
        return "%s - %s - %s" % (self.fiscal_year, self.obligated_amount, self.vendor_name)
    class Meta:
        verbose_name = 'FPDS Record'
    
    def _generate_sector_hash(self):
        h = 0
        for s in self.sectors.iterator():            
            h = h | s.binary_hash()
        return h
        
    def save(self):
        self.sector_hash = self._generate_sector_hash()
        try:
            super(FPDSRecord, self).save()
        except:
            pass#change this, stupid truncation...
    
    unique_transaction_id = models.CharField('unique_transaction_id', max_length=255, blank=False, null=False, primary_key=True)
    data_commons_id = models.IntegerField('data commons id', blank=False, null=False)

    sectors = models.ManyToManyField(Sector, blank=True)
    subsectors = models.ManyToManyField(Subsector, blank=True)
    sector_hash = models.IntegerField("Sector Hash", blank=True, null=True, db_index=True)

    version = models.CharField('version', max_length=10, blank=True, default='')
    agency_id = models.CharField('agencyID', max_length=4, blank=True, default='')
    piid = models.CharField('PIID', max_length=50, blank=True, default='')
    mod_number = models.CharField('modNumber', max_length=25, blank=True, default='')
    transaction_number = models.CharField('transactionNumber', max_length=6, blank=True, default='')
    idvagency_id = models.CharField('IDVAgencyID', max_length=4, blank=True, default='')
    idvpiid = models.CharField('IDVPIID', max_length=50, blank=True, default='')
    idvmodification_number = models.CharField('IDVModificationNumber', max_length=25, blank=True, default='')
    signed_date = models.DateField('signedDate', blank=True, null=True)
    effective_date = models.DateField('effectiveDate', blank=True, null=True)
    current_completion_date = models.DateField('currentCompletionDate', blank=True, null=True)
    ultimate_completion_date = models.DateField('ultimateCompletionDate', blank=True, null=True)
    obligated_amount = models.DecimalField('obligatedAmount', max_digits=18, decimal_places=2, blank=True, null=True)
    base_and_exercised_options_value = models.DecimalField('baseAndExercisedOptionsValue', max_digits=18, decimal_places=2, blank=True, null=True)
    base_and_all_options_value = models.DecimalField('baseAndAllOptionsValue', max_digits=18, decimal_places=2, blank=True, null=True)
    contracting_office_agency_id = models.CharField('contractingOfficeAgencyID', max_length=4, blank=True, default='')
    contracting_office_id = models.CharField('contractingOfficeID', max_length=6, blank=True, default='')
    funding_requesting_agency_id = models.CharField('fundingRequestingAgencyID', max_length=4, blank=True, default='')
    funding_requesting_office_id = models.CharField('fundingRequestingOfficeID', max_length=6, blank=True, default='')
    funded_by_foreign_entity = models.NullBooleanField('fundedByForeignEntity', default=False, blank=True, null=True) # values: ['f', '', 't']
    contract_action_type = models.CharField('contractActionType', max_length=1, blank=True, default='')
    type_of_contract_pricing = models.CharField('typeOfContractPricing', max_length=1, blank=True, default='')
    national_interest_action_code = models.CharField('nationalInterestActionCode', max_length=4, blank=True, default='')
    reason_for_modification = models.CharField('reasonForModification', max_length=1, blank=True, default='')
    major_program_code = models.CharField('majorProgramCode', max_length=100, blank=True, default='')
    cost_or_pricing_data = models.CharField('costOrPricingData', max_length=1, blank=True, default='')
    solicitation_id = models.CharField('solicitationID', max_length=25, blank=True, default='')
    cost_accounting_standards_clause = models.NullBooleanField('costAccountingStandardsClause', default=False, blank=True, null=True) # values: ['f', '', 't']
    description_of_contract_requirement = models.TextField('descriptionOfContractRequirement', blank=True, null=True)
    gfe_gfp = models.NullBooleanField('GFE_GFP', default=False, blank=True) # values: ['f', 't', '']
    sea_transportation = models.CharField('seaTransportation', max_length=1, blank=True, default='')
    consolidated_contract = models.NullBooleanField('consolidatedContract', default=False, blank=True, null=True) # values: ['', 'f', 't']
    letter_contract = models.NullBooleanField('letterContract', default=False, blank=True, null=True) # values: ['f', '', 't']
    multi_year_contract = models.NullBooleanField('multiYearContract', default=False, blank=True, null=True) # values: ['f', '', 't']
    performance_based_service_contract = models.NullBooleanField('performanceBasedServiceContract', default=False, blank=True, null=True) # values: ['Y', 'N', '']
    contingency_humanitarian_peacekeeping_operation = models.CharField('contingencyHumanitarianPeacekeepingOperation', max_length=1, default='', blank=True) # values: ['', 'A', 'B']
    contract_financing = models.CharField('contractFinancing', max_length=1, blank=True, default='')
    purchase_card_as_payment_method = models.NullBooleanField('purchaseCardAsPaymentMethod', default=False, blank=False) # values: ['f', 't']
    number_of_actions = models.IntegerField('numberOfActions', max_length=11, blank=True, null=True)
    walsh_healy_act = models.NullBooleanField('WalshHealyAct', default=False, blank=True, null=True) # values: ['f', 't']
    service_contract_act = models.NullBooleanField('serviceContractAct', default=False, blank=True, null=True) # values: ['f', 't']
    davis_bacon_act = models.NullBooleanField('DavisBaconAct', default=False, blank=True, null=True) # values: ['f', 't']
    clinger_cohen_act = models.NullBooleanField('ClingerCohenAct', default=False, blank=True, null=True) # values: ['f', 't', '']
    product_or_service_code = models.ForeignKey(ProductOrServiceCode, blank=True, default=None, null=True)
    contract_bundling = models.CharField('contractBundling', max_length=1, blank=True, default='')
    claimant_program_code = models.CharField('claimantProgramCode', max_length=3, blank=True, default='')
    principal_naicscode = models.ForeignKey(NAICSCode, blank=True, default=None, null=True)
    recovered_material_clauses = models.CharField('recoveredMaterialClauses', max_length=1, blank=True, default='')
    system_equipment_code = models.CharField('systemEquipmentCode', max_length=4, blank=True, default='')
    information_technology_commercial_item_category = models.CharField('informationTechnologyCommercialItemCategory', max_length=1, blank=True, default='')
    use_of_epadesignated_products = models.CharField('useOfEPADesignatedProducts', max_length=1, blank=True, default='')
    country_of_origin = models.CharField('countryOfOrigin', max_length=2, blank=True, default='')
    place_of_manufacture = models.CharField('placeOfManufacture', max_length=1, blank=True, default='')
    vendor_name = models.CharField('vendorName', max_length=100, blank=True, default='')
    vendor_alternate_name = models.CharField('vendorAlternateName', max_length=255, blank=True, default='')
    vendor_legal_organization_name = models.CharField('vendorLegalOrganizationName', max_length=120, blank=True, default='')
    vendor_doing_as_business_name = models.CharField('vendorDoingAsBusinessName', max_length=80, blank=True, default='')
    vendor_enabled = models.NullBooleanField('vendorEnabled', default=False, blank=True, null=True) # values: ['', 'f']
    firm8aflag = models.NullBooleanField('firm8AFlag', default=False, blank=True, null=True) # values: ['f', 't']
    hubzone_flag = models.NullBooleanField('HUBZoneFlag', default=False, blank=True, null=True) # values: ['f', 't']
    sdbflag = models.NullBooleanField('SDBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    sheltered_workshop_flag = models.NullBooleanField('shelteredWorkshopFlag', default=False, blank=True, null=True) # values: ['f', 't']
    hbcuflag = models.NullBooleanField('HBCUFlag', default=False, blank=True, null=True) # values: ['f', 't']
    educational_institution_flag = models.NullBooleanField('educationalInstitutionFlag', default=False, blank=True, null=True) # values: ['f', 't']
    women_owned_flag = models.NullBooleanField('womenOwnedFlag', default=False, blank=True, null=True) # values: ['f', 't']
    veteran_owned_flag = models.NullBooleanField('veteranOwnedFlag', default=False, blank=True, null=True) # values: ['f', 't']
    srdvobflag = models.NullBooleanField('SRDVOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    local_government_flag = models.NullBooleanField('localGovernmentFlag', default=False, blank=True, null=True) # values: ['f', 't']
    minority_institution_flag = models.NullBooleanField('minorityInstitutionFlag', default=False, blank=True, null=True) # values: ['f', 't']
    aiobflag = models.NullBooleanField('AIOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    state_government_flag = models.NullBooleanField('stateGovernmentFlag', default=False, blank=True, null=True) # values: ['f', 't']
    federal_government_flag = models.NullBooleanField('federalGovernmentFlag', default=False, blank=True, null=True) # values: ['f', 't']
    minority_owned_business_flag = models.NullBooleanField('minorityOwnedBusinessFlag', default=False, blank=True, null=True) # values: ['f', 't']
    apaobflag = models.NullBooleanField('APAOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    tribal_government_flag = models.NullBooleanField('tribalGovernmentFlag', default=False, blank=True, null=True) # values: ['f']
    baobflag = models.NullBooleanField('BAOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    naobflag = models.NullBooleanField('NAOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    saaobflag = models.NullBooleanField('SAAOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    nonprofit_organization_flag = models.NullBooleanField('nonprofitOrganizationFlag', default=False, blank=True, null=True) # values: ['f', 't']
    haobflag = models.NullBooleanField('HAOBFlag', default=False, blank=True, null=True) # values: ['f', 't']
    very_small_business_flag = models.NullBooleanField('verySmallBusinessFlag', default=False, blank=True, null=True) # values: ['f', 't']
    hospital_flag = models.NullBooleanField('hospitalFlag', default=False, blank=True, null=True) # values: ['f', 't']
    number_of_employees = models.IntegerField('numberOfEmployees', max_length=11, blank=True, null=True)
    organizational_type = models.CharField('organizationalType', max_length=30, blank=True, default='')
    street_address = models.CharField('streetAddress', max_length=55, blank=True, default='')
    street_address2 = models.CharField('streetAddress2', max_length=55, blank=True, default='')
    street_address3 = models.CharField('streetAddress3', max_length=55, blank=True, default='')
    city = models.CharField('city', max_length=35, blank=True, default='')
    state = models.ForeignKey(State, related_name='state', blank=True, null=True)
    zipcode = models.CharField('ZIPCode', max_length=10, blank=True, default='')
    vendor_country_code = models.CharField('vendorCountryCode', max_length=3, blank=True, default='')
    vendor_site_code = models.CharField('vendorSiteCode', max_length=15, blank=True, default='')
    vendor_alternate_site_code = models.CharField('vendorAlternateSiteCode', max_length=15, blank=True, default='')
    dunsnumber = models.CharField('DUNSNumber', max_length=13, blank=True, default='')
    parent_dunsnumber = models.CharField('parentDUNSNumber', max_length=13, blank=True, default='')
    phone_no = models.CharField('phoneNo', max_length=20, blank=True, default='')
    fax_no = models.CharField('faxNo', max_length=20, blank=True, default='')
    division_name = models.CharField('divisionName', max_length=60, blank=True, default='')
    division_number_or_office_code = models.CharField('divisionNumberOrOfficeCode', max_length=10, blank=True, default='')
    congressional_district = models.CharField('congressionalDistrict', max_length=6, blank=True, default='')
    registration_date = models.DateField('registrationDate', blank=True, null=True)
    renewal_date = models.DateField('renewalDate', blank=True, null=True)
    vendor_location_disable_flag = models.NullBooleanField('vendorLocationDisableFlag', default=False, blank=True, null=True) # values: ['']
    ccrexception = models.CharField('CCRException', max_length=1, blank=True, default='')
    contracting_officer_business_size_determination = models.CharField('contractingOfficerBusinessSizeDetermination', max_length=1, default='', blank=True) # values: ['S', 'O', '']
    location_code = models.CharField('locationCode', max_length=5, blank=True, default='')
    state_code = models.ForeignKey(State, related_name='state_code', blank=True, null=True)
    place_of_performance_country_code = models.CharField('placeOfPerformanceCountryCode', max_length=3, blank=True, default='')
    place_of_performance_zipcode = models.CharField('placeOfPerformanceZIPCode', max_length=10, blank=True, default='')
    place_of_performance_congressional_district = models.CharField('placeOfPerformanceCongressionalDistrict', max_length=6, blank=True, default='')
    place_of_performance_state = models.ForeignKey(State, related_name='place of performance state', blank=True, null=True)
    extent_competed = models.CharField('extentCompeted', max_length=3, blank=True, default='')
    competitive_procedures = models.CharField('competitiveProcedures', max_length=3, blank=True, default='')
    solicitation_procedures = models.CharField('solicitationProcedures', max_length=5, blank=True, default='')
    type_of_set_aside = models.CharField('typeOfSetAside', max_length=10, blank=True, default='')
    evaluated_preference = models.CharField('evaluatedPreference', max_length=6, blank=True, default='')
    research = models.CharField('research', max_length=3, blank=True, default='')
    statutory_exception_to_fair_opportunity = models.CharField('statutoryExceptionToFairOpportunity', max_length=10, blank=True, default='')
    reason_not_competed = models.CharField('reasonNotCompeted', max_length=3, blank=True, default='')
    number_of_offers_received = models.IntegerField('numberOfOffersReceived', max_length=6, blank=True, null=True)
    commercial_item_acquisition_procedures = models.NullBooleanField('commercialItemAcquisitionProcedures', default=False, blank=True, null=True) # values: ['t', 'f', '']
    commercial_item_test_program = models.NullBooleanField('commercialItemTestProgram', default=False, blank=True, null=True) # values: ['t', 'f']
    small_business_competitiveness_demonstration_program = models.NullBooleanField('smallBusinessCompetitivenessDemonstrationProgram', default=False, blank=True, null=True) # values: ['f', 't']
    a76action = models.NullBooleanField('A76Action', default=False, blank=True, null=True) # values: ['f', '', 't']
    price_evaluation_percent_difference = models.CharField('priceEvaluationPercentDifference', max_length=2, blank=True, default='')
    subcontract_plan = models.CharField('subcontractPlan', max_length=1, blank=True, default='')
    status = models.NullBooleanField('status', default=False, blank=False) # values: ['F']
    other_statutory_authority = models.TextField('otherStatutoryAuthority', blank=True, null=True)
    fiscal_year = models.IntegerField('fiscal_year', max_length=6, blank=True, null=True)
    mod_parent = models.CharField('mod_parent', max_length=100, blank=True, default='')
    maj_agency_cat = models.CharField('maj_agency_cat', max_length=2, blank=True, default='')
    psc_cat = models.CharField('psc_cat', max_length=2, blank=True, default='')
    vendor_cd = models.CharField('vendor_cd', max_length=4, blank=True, default='')
    pop_cd = models.CharField('pop_cd', max_length=4, blank=True, default='')
    mod_agency = models.CharField('mod_agency', max_length=4, blank=True, default='')
    maj_fund_agency_cat = models.CharField('maj_fund_agency_cat', max_length=2, blank=True, default='')
    prog_source_agency = models.CharField('ProgSourceAgency', max_length=2, blank=True, default='')
    prog_source_account = models.CharField('ProgSourceAccount', max_length=4, blank=True, default='')
    prog_source_sub_acct = models.CharField('ProgSourceSubAcct', max_length=3, blank=True, default='')
    rec_flag = models.NullBooleanField('rec_flag', default=False, blank=True, null=True) # values: ['']
    annual_revenue = models.DecimalField('annualRevenue', max_digits=20, decimal_places=2, blank=True, null=True)



class FPDSLoader(object):
    """ handles FPDS import """

    def __init__(self):

        super(FPDSLoader, self).__init__()        

        self.state_matcher = StateMatcher()
        self.naics_matcher = CodeMatcher(NAICSCode)
        self.psc_matcher = CodeMatcher(ProductOrServiceCode)

        self.FIELD_MAPPING = {
        #   'django field name': 'FPDS field name' OR callable that returns value when passed row
            'unique_transaction_id': 'unique_transaction_id',
            'data_commons_id': 'id',
            'agency_id': (self.make_null_emptystring, {'field_name': 'agencyid'}),
            'piid': (self.make_null_emptystring, {'field_name': 'piid'}),
            'mod_number': (self.make_null_emptystring, {'field_name': 'modnumber'}),
            'transaction_number': (self.make_null_emptystring, {'field_name': 'transactionnumber'}),
            'idvagency_id': (self.make_null_emptystring, {'field_name': 'idvagencyid'}),
            'idvpiid': (self.make_null_emptystring, {'field_name': 'idvpiid'}),
            'idvmodification_number': (self.make_null_emptystring, {'field_name': 'idvmodificationnumber'}),
            'signed_date': 'signeddate',
            'effective_date': 'effectivedate',
            'current_completion_date': 'currentcompletiondate',
            'ultimate_completion_date': 'ultimatecompletiondate',
            'obligated_amount': (self.convert_float_to_string, { 'field_name': 'obligatedamount'}),
            'base_and_exercised_options_value': (self.convert_float_to_string, { 'field_name': 'baseandexercisedoptionsvalue'}),
            'base_and_all_options_value': (self.convert_float_to_string, { 'field_name': 'baseandalloptionsvalue'}),
            'contracting_office_agency_id': (self.make_null_emptystring, {'field_name': 'contractingofficeagencyid'}),
            'contracting_office_id': (self.make_null_emptystring, {'field_name': 'contractingofficeid'}),
            'funding_requesting_agency_id': (self.make_null_emptystring, {'field_name': 'fundingrequestingagencyid'}),
            'funding_requesting_office_id': (self.make_null_emptystring, {'field_name': 'fundingrequestingofficeid'}),
            'funded_by_foreign_entity': (self.make_boolean_from_char, {'field_name': 'fundedbyforeignentity'}),
            'contract_action_type': (self.make_null_emptystring, {'field_name': 'contractactiontype'}),
            'type_of_contract_pricing': (self.make_null_emptystring, {'field_name': 'typeofcontractpricing'}),
            'national_interest_action_code': (self.make_null_emptystring, {'field_name': 'nationalinterestactioncode'}),
            'reason_for_modification': (self.make_null_emptystring, {'field_name': 'reasonformodification'}),
            'major_program_code': (self.make_null_emptystring, {'field_name': 'majorprogramcode'}),
            'cost_or_pricing_data': (self.make_null_emptystring, {'field_name': 'costorpricingdata'}),
            'solicitation_id': (self.make_null_emptystring, {'field_name': 'solicitationid'}),
            'cost_accounting_standards_clause': (self.make_boolean_from_char, {'field_name': 'costaccountingstandardsclause'}),
            'description_of_contract_requirement': (self.make_null_emptystring, {'field_name': 'descriptionofcontractrequirement'}),
            'gfe_gfp': (self.make_boolean_from_char, {'field_name': 'gfe_gfp'}),
            'sea_transportation': (self.make_null_emptystring, {'field_name': 'seatransportation'}),
            'consolidated_contract': (self.make_boolean_from_char, {'field_name': 'consolidatedcontract'}),
            'letter_contract': (self.make_boolean_from_char, {'field_name': 'lettercontract'}),
            'multi_year_contract': (self.make_boolean_from_char, {'field_name': 'multiyearcontract'}),
            'performance_based_service_contract': (self.make_boolean_from_char, {'field_name': 'performancebasedservicecontract'}),
            'contingency_humanitarian_peacekeeping_operation': (self.make_null_emptystring, {'field_name': 'contingencyhumanitarianpeacekeepingoperation'}),
            'contract_financing': (self.make_null_emptystring, {'field_name': 'contractfinancing'}),
            'purchase_card_as_payment_method': (self.make_boolean_from_char, {'field_name': 'purchasecardaspaymentmethod'}),
            'number_of_actions': 'numberofactions',
            'walsh_healy_act': (self.make_boolean_from_char, {'field_name': 'Walshhealyact'}),
            'service_contract_act': (self.make_boolean_from_char, {'field_name': 'servicecontractact'}),
            'davis_bacon_act': (self.make_boolean_from_char, {'field_name': 'davisbaconact'}),
            'clinger_cohen_act': (self.make_boolean_from_char, {'field_name': 'clingercohenact'}),
            'product_or_service_code': (self.lookup_classification_code, {'field_name': 'productorservicecode', 'matcher': self.psc_matcher}),
            'contract_bundling': (self.make_null_emptystring, {'field_name': 'contractbundling'}),
            'claimant_program_code': (self.make_null_emptystring, {'field_name': 'claimantprogramcode'}),
            'principal_naicscode': (self.lookup_classification_code, {'field_name': 'principalnaicscode', 'matcher': self.naics_matcher}),
            'recovered_material_clauses': (self.make_null_emptystring, {'field_name': 'recoveredmaterialclauses'}),
            'system_equipment_code': (self.make_null_emptystring, {'field_name': 'systemequipmentcode'}),
            'information_technology_commercial_item_category': (self.make_null_emptystring, {'field_name': 'informationtechnologycommercialitemcategory'}),
            'use_of_epadesignated_products': (self.make_null_emptystring, {'field_name': 'useofepadesignatedproducts'}),
            'country_of_origin': (self.make_null_emptystring, {'field_name': 'countryoforigin'}),
            'place_of_manufacture': (self.make_null_emptystring, {'field_name': 'placeofmanufacture'}),
            'vendor_name': (self.make_null_emptystring, {'field_name': 'vendorname'}),
            'vendor_alternate_name': (self.make_null_emptystring, {'field_name': 'vendoralternatename'}),
            'vendor_legal_organization_name': (self.make_null_emptystring, {'field_name': 'vendorlegalorganizationname'}),
            'vendor_doing_as_business_name': (self.make_null_emptystring, {'field_name': 'vendordoingasbusinessname'}),
            'vendor_enabled': (self.make_boolean_from_char, {'field_name': 'vendorenabled'}),
            'firm8aflag': (self.make_boolean_from_char, {'field_name': 'firm8aflag'}),
            'hubzone_flag': (self.make_boolean_from_char, {'field_name': 'hubzoneflag'}),
            'sdbflag': (self.make_boolean_from_char, {'field_name': 'sdbflag'}),
            'sheltered_workshop_flag': (self.make_boolean_from_char, {'field_name': 'shelteredworkshopflag'}),
            'hbcuflag': (self.make_boolean_from_char, {'field_name': 'hbcuflag'}),
            'educational_institution_flag': (self.make_boolean_from_char, {'field_name': 'educationalinstitutionflag'}),
            'women_owned_flag': (self.make_boolean_from_char, {'field_name': 'womenownedflag'}),
            'veteran_owned_flag': (self.make_boolean_from_char, {'field_name': 'veteranownedflag'}),
            'srdvobflag': (self.make_boolean_from_char, {'field_name': 'srdvobflag'}),
            'local_government_flag': (self.make_boolean_from_char, {'field_name': 'localgovernmentflag'}),
            'minority_institution_flag': (self.make_boolean_from_char, {'field_name': 'minorityinstitutionflag'}),
            'aiobflag': (self.make_boolean_from_char, {'field_name': 'aiobflag'}),
            'state_government_flag': (self.make_boolean_from_char, {'field_name': 'stategovernmentflag'}),
            'federal_government_flag': (self.make_boolean_from_char, {'field_name': 'federalgovernmentflag'}),
            'minority_owned_business_flag': (self.make_boolean_from_char, {'field_name': 'minorityownedbusinessflag'}),
            'apaobflag': (self.make_boolean_from_char, {'field_name': 'apaobflag'}),
            'tribal_government_flag': (self.make_boolean_from_char, {'field_name': 'tribalgovernmentflag'}),
            'baobflag': (self.make_boolean_from_char, {'field_name': 'baobflag'}),
            'naobflag': (self.make_boolean_from_char, {'field_name': 'naobflag'}),
            'saaobflag': (self.make_boolean_from_char, {'field_name': 'saaobflag'}),
            'nonprofit_organization_flag': (self.make_boolean_from_char, {'field_name': 'nonprofitorganizationflag'}),
            'haobflag': (self.make_boolean_from_char, {'field_name': 'haobflag'}),
            'very_small_business_flag': (self.make_boolean_from_char, {'field_name': 'verysmallbusinessflag'}),
            'hospital_flag': (self.make_boolean_from_char, {'field_name': 'hospitalflag'}),
            'number_of_employees': 'numberofemployees',
            'organizational_type': (self.make_null_emptystring, {'field_name': 'organizationaltype'}),
            'street_address': (self.make_null_emptystring, {'field_name': 'streetaddress'}),
            'street_address2': (self.make_null_emptystring, {'field_name': 'streetaddress2'}),
            'street_address3': (self.make_null_emptystring, {'field_name': 'streetaddress3'}),
            'city': (self.make_null_emptystring, {'field_name': 'city'}),
            'state': (self.lookup_state, {'field_name': 'state'}),
            'zipcode': (self.make_null_emptystring, {'field_name': 'zipcode'}),
            'vendor_country_code': (self.make_null_emptystring, {'field_name': 'vendorcountrycode'}),
            'vendor_site_code': (self.make_null_emptystring, {'field_name': 'vendorsitecode'}),
            'vendor_alternate_site_code': (self.make_null_emptystring, {'field_name': 'vendoralternatesitecode'}),
            'dunsnumber': (self.make_null_emptystring, {'field_name': 'dunsnumber'}),
            'parent_dunsnumber': (self.make_null_emptystring, {'field_name': 'parentdunsnumber'}),
            'phone_no': (self.make_null_emptystring, {'field_name': 'phoneno'}),
            'fax_no': (self.make_null_emptystring, {'field_name': 'faxno'}),
            'division_name': (self.make_null_emptystring, {'field_name': 'divisionname'}),
            'division_number_or_office_code': (self.make_null_emptystring, {'field_name': 'divisionnumberorofficecode'}),
            'congressional_district': (self.make_null_emptystring, {'field_name': 'congressionaldistrict'}),
            'registration_date': 'registrationdate',
            'renewal_date': 'renewaldate',
            'vendor_location_disable_flag': (self.make_boolean_from_char, {'field_name': 'vendorlocationdisableflag'}),
            'ccrexception': (self.make_null_emptystring, {'field_name': 'ccrexception'}),
            'contracting_officer_business_size_determination': (self.make_null_emptystring, {'field_name': 'contractingofficerbusinesssizedetermination'}),
            'location_code': (self.make_null_emptystring, {'field_name': 'locationcode'}),
            'state_code': (self.lookup_state, {'field_name': 'statecode'}),
            'place_of_performance_country_code': (self.make_null_emptystring, {'field_name': 'placeofperformancecountrycode'}),
            'place_of_performance_zipcode': (self.make_null_emptystring, {'field_name': 'placeofperformancezipcode'}),
            'place_of_performance_congressional_district': (self.make_null_emptystring, {'field_name': 'placeofperformancecongressionaldistrict'}),
            'place_of_performance_state': (self.lookup_pop_state, {}),
            'extent_competed': (self.make_null_emptystring, {'field_name': 'extentcompeted'}),
            'competitive_procedures': (self.make_null_emptystring, {'field_name': 'competitiveprocedures'}),
            'solicitation_procedures': (self.make_null_emptystring, {'field_name': 'solicitationprocedures'}),
            'type_of_set_aside': (self.make_null_emptystring, {'field_name': 'typeofsetaside'}),
            'evaluated_preference': (self.make_null_emptystring, {'field_name': 'evaluatedpreference'}),
            'research': (self.make_null_emptystring, {'field_name': 'research'}),
            'statutory_exception_to_fair_opportunity': (self.make_null_emptystring, {'field_name': 'statutoryexceptiontofairopportunity'}),
            'reason_not_competed': (self.make_null_emptystring, {'field_name': 'reasonnotcompeted'}),
            'number_of_offers_received': 'numberofoffersreceived',
            'commercial_item_acquisition_procedures': (self.make_boolean_from_char, {'field_name': 'commercialitemacquisitionprocedures'}),
            'commercial_item_test_program': (self.make_boolean_from_char, {'field_name': 'commercialitemtestprogram'}),
            'small_business_competitiveness_demonstration_program': (self.make_boolean_from_char, {'field_name': 'smallbusinesscompetitivenessdemonstrationprogram'}),
            'a76action': (self.make_boolean_from_char, {'field_name': 'a76action'}),
            'price_evaluation_percent_difference': (self.make_null_emptystring, {'field_name': 'priceevaluationpercentdifference'}),
            'subcontract_plan': (self.make_null_emptystring, {'field_name': 'subcontractplan'}),
            'status': (self.make_boolean_from_char, {'field_name': 'transaction_status'}),
            'other_statutory_authority': (self.make_null_emptystring, {'field_name': 'otherstatutoryauthority'}),
            'fiscal_year': 'fiscal_year',
            'mod_parent': (self.make_null_emptystring, {'field_name': 'mod_parent'}),
            'maj_agency_cat': (self.make_null_emptystring, {'field_name': 'maj_agency_cat'}),
            'psc_cat': (self.make_null_emptystring, {'field_name': 'psc_cat'}),
            'vendor_cd': (self.make_null_emptystring, {'field_name': 'vendor_cd'}),
            'pop_cd': (self.make_null_emptystring, {'field_name': 'pop_cd'}),
            'mod_agency': (self.make_null_emptystring, {'field_name': 'mod_agency'}),
            'maj_fund_agency_cat': (self.make_null_emptystring, {'field_name': 'maj_fund_agency_cat'}),
            'prog_source_agency': (self.make_null_emptystring, {'field_name': 'progsourceagency'}),
            'prog_source_account': (self.make_null_emptystring, {'field_name': 'progsourceaccount'}),
            'prog_source_sub_acct': (self.make_null_emptystring, {'field_name': 'progsourcesubacct'}),
            'rec_flag': (self.make_boolean_from_char, {'field_name': 'rec_flag'}),
            'annual_revenue': (self.convert_float_to_string, { 'field_name': 'annualrevenue'}),     
        }


    def reset_fpds_import(self):
        FPDSRecord.objects.all().delete()

    def assign_sectors(self, *args, **kwargs):

        """ check for assignation of sector to each record """
        record = args[0]
        sectors_to_assign = []
        n_txt = record.get('principalnaicscode')
        p_txt = record.get('productorservicecode')
        print n_txt
        if n_txt != '':
            naics = NAICSCode.objects.filter(code=n_txt)
            if len(naics) > 0:
                naics = naics[0]
                for s in self.sector_sql_mapping:
                    if s in naics.sectors.all():
                        sectors_to_assign.append(s)
        elif p_txt != '':
            psc = ProductOrServiceCode.objects.filter(code=record.get('productorservicecode'))
            if len(psc) > 0:
                psc = psc[0]
                for s in self.sector_sql_mapping:
                    if s in psc.sectors.all():
                        sectors_to_assign.append(s)

        return sectors_to_assign



    def make_boolean_from_char(self, *args, **kwargs):
        """ return (success, result) """
        record = args[0]
        field_name = kwargs['field_name']
        c = record[field_name]
        if c.lower() in ('f', 'n'):
            return (True, False)
        elif c.lower() in ('t', 'y'):
            return (True, True)
        else:
            return (False, None)
            
    def convert_float_to_string(self, *args, **kwargs):
        """ return (success, result) """        
        record = args[0]
        field_name = kwargs['field_name']
        r = record.get(field_name, None)
        if r is not None:
            return (True, str(r))
        else:
            return (False, None)


    def make_null_emptystring(self, *args, **kwargs):
        """ return (success, result) """        
        record = args[0]
        field_name = kwargs['field_name']
        r = record.get(field_name, None)
        if r is not None:
            return (True, r)
        else:
            return (False, '')


    def lookup_pop_state(self, *args, **kwargs):
        """ 
        return (success, result) 
        """
        record = args[0]
        try:
            if record['pop_cd'][:2] is not 'ZZ':
                state = self.state_matcher.matchName(record['pop_cd'][:2])
                if state:
                    return (True, state)
                    
        except Exception, e:
            pass
            
        return (False, None)            
    
    
    def lookup_classification_code(self, *args, **kwargs):
        """
        match PSC/NAICS codes using appropriate utility
        return (success, result)
        """
        record = args[0]
        field_name = kwargs['field_name']
        matcher = kwargs['matcher']
        
        r = record[field_name]
        if r is None or len(r)==0:
            return (False, None)
        else:
            m = matcher.match(r)
            return (m is not None, m)   


    def lookup_recipient_county(self, *args, **kwargs):
        """ return (success, result) """
        record = args[0]

        try:
            recipient_state_code = int(record['recipient_state_code'])

            state = self.state_matcher.matcher.matchFips(recipient_state_code)

            if state:
                recipient_county_code = int(record['recipient_county_code'])

                county_matcher = self.state_matcher.matcher.getCountyMatcher(state)
                county = county_matcher.matchFips(recipient_county_code)

                if county:
                    return (True, county)
                else:
                    return (False, None)
            else:
                return (False, None)

        except Exception, e:
            return (False, None)

    def lookup_recipient_state(self, *args, **kwargs):
        """ return (success, result) """
        record = args[0]

        try:
            recipient_state_code = int(record['recipient_state_code'])

            state = self.state_matcher.matcher.matchFips(recipient_state_code)

            if state:
                return (True, state)
            else:
                return (False, None)

        except Exception, e:
            return (False, None) 

    def lookup_state(self, *args, **kwargs):
        """ return (success, result) """
        record = args[0]

        try:
            state = None
            state_key = kwargs.get('field_name', None)
            if state_key is not None:
                state = self.state_matcher.matchName(record[state_key])

            if state:
                return (True, state)
            else:
                return (False, None)

        except Exception, e:
            return (False, None) 

    def lookup_principal_place_county(self, *args, **kwargs):
        """ return (success, result) """
        record = args[0]

        try:
            principal_place_code = record['principal_place_code']

            state, county = self.state_matcher.matchPrincipalPlace(principal_place_code)

            if county:
                return (True, county)
            else:
                return (False, None)

        except Exception, e:
            return (False, None)

    def lookup_fk_field(self, *args, **kwargs):
        """ return (success, result) """        
        record = args[0]
        code_extractor = kwargs.get('code_extractor')
        value = code_extractor(record)

        type_name = kwargs.get('type_name')

        lookup_object = getattr(self, type_name, None)
        if lookup_object is not None:
            r = lookup_object.get(value, None)
            if r is not None:
                return (True, r)

        return (False, None)


    def process_record(self, FPDS_record):
        django_record = FPDSRecord()
        failed_fields = []
        print "id: %s" % FPDS_record.get('id')
        for attrname in self.FIELD_MAPPING:            
            grabber = self.FIELD_MAPPING[attrname]
            if type(grabber)==tuple and callable(grabber[0]):
                func = grabber[0]
                args = [FPDS_record]
                kwargs = grabber[1]
                if FPDS_record.get(kwargs.get('field_name')) or attrname == 'place_of_performance_state' :
                    (success, extracted_value) = func(FPDS_record, *args, **kwargs)
                    if success:
                        setattr(django_record, attrname, extracted_value)
                    else:
                        failed_fields.append("%s (%s)" % (attrname, str(extracted_value)))                    
            else:
                setattr(django_record, attrname, FPDS_record.get(grabber))

        if len(failed_fields):
            sys.stderr.write("%s: failed to extract field(s) %s\n" % (FPDS_record['unique_transaction_id'], ', '.join(failed_fields)))


        django_record.save()
        print "saved record"
        django_record.sectors = self.assign_sectors(FPDS_record)
        django_record.save()

        # try:
        #     django_record.save()    
        # except Exception, e:
        #     sys.stderr.write("%d: failed to save / %s\n" % (FPDS_record['record_id'], str(e)))

    def get_max_id(self):
        return FPDSRecord.objects.aggregate(Max('data_commons_id'))['data_commons_id__max'] or 0
        
    def get_max_server_id(self, conn, settings):
        
        sql = "SELECT MAX(id) FROM %s" % settings.FPDS_IMPORT_MYSQL_SETTINGS.get('source_table', 'contracts_contract')
        res = conn.query(sql)
        d = res.dictresult()[0].get('max')
        return d
        

    def do_import(self, table_override=None):
        import imp
        from django.conf import settings
        sql_selection_clauses = []
        self.sector_sql_mapping = {}
        #for app in settings.INSTALLED_APPS:
        #    try:
        #        app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        #    except AttributeError:
        #        continue
        #
        #    try:
        #        imp.find_module('usaspending', app_path)
        #    except ImportError:
        #        continue

        #    m = __import__("%s.usaspending" % app)            
        #    f = getattr(getattr(m, 'usaspending', 'None'), 'fpds', False)
        #    if f:
        #        sector_selection_criteria = f()
        #        if sector_selection_criteria not in (None, False):   
        #            sql_selection_clauses.append("(%s)" % sector_selection_criteria['sector'].values()[0])
        #            self.sector_sql_mapping[sector_selection_criteria['sector'].keys()[0]] = sector_selection_criteria['sector'].values()[0]

        all_sectors = Sector.objects.all()
        for sector in all_sectors:

            psc_codes = ProductOrServiceCode.objects.filter(sectors=sector)
            naics_codes = NAICSCode.objects.filter(sectors=sector)
             
            if psc_codes or naics_codes:     
                psc_code_string = "'%s'" % "','".join(map(lambda x: str(x.code).upper().strip(), psc_codes)) # chars -- need quotes
                naics_code_string = "'%s'" % ",".join(map(lambda x: str(x.code), naics_codes)) # ints -- no quotes necessary
                sql = "TRIM(UPPER(extentCompeted)) IN ('B', 'C', 'D', 'E', 'G', 'NDO') AND ((TRIM(UPPER(principalNAICSCode)) IN (%s)) OR ((TRIM(principalNAICSCode)='') AND (TRIM(UPPER(productOrServiceCode)) IN (%s))))" % (naics_code_string, psc_code_string)
            
                sql_selection_clauses.append("(%s)" % sql)
                self.sector_sql_mapping[sector] = sql

        # generate SQL that will provide a field for each record delineating the sectors to which it should be assigned
        sector_inclusion_sql = map(lambda (sector, sql): "IF ((%s)) THEN AS include_in_sector_%s END IF " % (sql, sector.id), self.sector_sql_mapping.items())
        if len(sector_inclusion_sql):
            sector_inclusion_sql.insert(0, '')
        
        max_id = self.get_max_id()
        
        conn = pg.connect(host=settings.FPDS_IMPORT_MYSQL_SETTINGS['host'], user=settings.FPDS_IMPORT_MYSQL_SETTINGS['user'], passwd=settings.FPDS_IMPORT_MYSQL_SETTINGS['password'], dbname=settings.FPDS_IMPORT_MYSQL_SETTINGS['database'], port=settings.FPDS_IMPORT_MYSQL_SETTINGS['port'])
        
        max_server_id = self.get_max_server_id(conn, settings)
        print max_id
        print max_server_id
        i = 0
        while int(max_id) < int(max_server_id):                
            sql = "SELECT * FROM %s WHERE (%s) AND id > %d ORDER BY id ASC LIMIT 1000" % ((table_override is not None) and table_override or settings.FPDS_IMPORT_MYSQL_SETTINGS.get('source_table', 'fpds_award3_sf'), " OR ".join(sql_selection_clauses), max_id)
            print "Executing query: %s" % sql
            results = conn.query(sql).dictresult()
            for row in results:
                sys.stdout.write("Entering loop... ")
                sys.stdout.write("Processing row... ")
                self.process_record(row)
                i = i + 1

                sys.stdout.write("Finished iteration %d\n" % i)
            max_id = self.get_max_id()

        conn.close()

        
