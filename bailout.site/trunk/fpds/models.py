from django.db import models
from geo.models import *

class FPDSRecord(models.Model):
    def __unicode__(self):
        return "%s - %s - %s" % (self.fiscal_year, self.federal_funding_amount, self.recipient_name)
    class Meta:
        verbose_name = 'FPDS Record'
        
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
    purchase_reason = models.CharField('purchaseReason', max_length=1, blank=True, default='')
    funded_by_foreign_entity = models.BooleanField('fundedByForeignEntity', default=False, blank=True) # values: ['f', '', 't']
    fee_paid_for_use_of_service = models.DecimalField('feePaidForUseOfService', max_digits=18, decimal_places=2, blank=True, null=True)
    contract_action_type = models.CharField('contractActionType', max_length=1, blank=True, default='')
    type_of_contract_pricing = models.CharField('typeOfContractPricing', max_length=1, blank=True, default='')
    national_interest_action_code = models.CharField('nationalInterestActionCode', max_length=4, blank=True, default='')
    reason_for_modification = models.CharField('reasonForModification', max_length=1, blank=True, default='')
    major_program_code = models.CharField('majorProgramCode', max_length=100, blank=True, default='')
    cost_or_pricing_data = models.CharField('costOrPricingData', max_length=1, blank=True, default='')
    solicitation_id = models.CharField('solicitationID', max_length=25, blank=True, default='')
    cost_accounting_standards_clause = models.BooleanField('costAccountingStandardsClause', default=False, blank=True) # values: ['f', '', 't']
    description_of_contract_requirement = models.TextField('descriptionOfContractRequirement', blank=True, null=True)
    gfe_gfp = models.BooleanField('GFE_GFP', default=False, blank=True) # values: ['f', 't', '']
    sea_transportation = models.CharField('seaTransportation', max_length=1, blank=True, default='')
    consolidated_contract = models.BooleanField('consolidatedContract', default=False, blank=True) # values: ['', 'f', 't']
    letter_contract = models.BooleanField('letterContract', default=False, blank=True) # values: ['f', '', 't']
    multi_year_contract = models.BooleanField('multiYearContract', default=False, blank=True) # values: ['f', '', 't']
    performance_based_service_contract = models.BooleanField('performanceBasedServiceContract', default=False, blank=True) # values: ['Y', 'N', '']
    contingency_humanitarian_peacekeeping_operation = models.BooleanField('contingencyHumanitarianPeacekeepingOperation', default=False, blank=True) # values: ['', 'A', 'B']
    contract_financing = models.CharField('contractFinancing', max_length=1, blank=True, default='')
    purchase_card_as_payment_method = models.BooleanField('purchaseCardAsPaymentMethod', default=False, blank=False) # values: ['f', 't']
    number_of_actions = models.IntegerField('numberOfActions', max_length=11, blank=True, null=True)
    walsh_healy_act = models.BooleanField('WalshHealyAct', default=False, blank=False) # values: ['f', 't']
    service_contract_act = models.BooleanField('serviceContractAct', default=False, blank=False) # values: ['f', 't']
    davis_bacon_act = models.BooleanField('DavisBaconAct', default=False, blank=False) # values: ['f', 't']
    clinger_cohen_act = models.BooleanField('ClingerCohenAct', default=False, blank=True) # values: ['f', 't', '']
    product_or_service_code = models.CharField('productOrServiceCode', max_length=4, blank=True, default='')
    contract_bundling = models.CharField('contractBundling', max_length=1, blank=True, default='')
    claimant_program_code = models.CharField('claimantProgramCode', max_length=3, blank=True, default='')
    principal_naicscode = models.CharField('principalNAICSCode', max_length=6, blank=True, default='')
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
    vendor_enabled = models.BooleanField('vendorEnabled', default=False, blank=True) # values: ['', 'f']
    small_business_flag = models.BooleanField('smallBusinessFlag', default=False, blank=False) # values: ['t', 'f']
    firm8aflag = models.BooleanField('firm8AFlag', default=False, blank=False) # values: ['f', 't']
    hubzone_flag = models.BooleanField('HUBZoneFlag', default=False, blank=False) # values: ['f', 't']
    sdbflag = models.BooleanField('SDBFlag', default=False, blank=False) # values: ['f', 't']
    sheltered_workshop_flag = models.BooleanField('shelteredWorkshopFlag', default=False, blank=False) # values: ['f', 't']
    hbcuflag = models.BooleanField('HBCUFlag', default=False, blank=False) # values: ['f', 't']
    educational_institution_flag = models.BooleanField('educationalInstitutionFlag', default=False, blank=False) # values: ['f', 't']
    women_owned_flag = models.BooleanField('womenOwnedFlag', default=False, blank=False) # values: ['f', 't']
    veteran_owned_flag = models.BooleanField('veteranOwnedFlag', default=False, blank=False) # values: ['f', 't']
    srdvobflag = models.BooleanField('SRDVOBFlag', default=False, blank=False) # values: ['f', 't']
    local_government_flag = models.BooleanField('localGovernmentFlag', default=False, blank=False) # values: ['f', 't']
    minority_institution_flag = models.BooleanField('minorityInstitutionFlag', default=False, blank=False) # values: ['f', 't']
    aiobflag = models.BooleanField('AIOBFlag', default=False, blank=False) # values: ['f', 't']
    state_government_flag = models.BooleanField('stateGovernmentFlag', default=False, blank=False) # values: ['f', 't']
    federal_government_flag = models.BooleanField('federalGovernmentFlag', default=False, blank=False) # values: ['f', 't']
    minority_owned_business_flag = models.BooleanField('minorityOwnedBusinessFlag', default=False, blank=False) # values: ['f', 't']
    apaobflag = models.BooleanField('APAOBFlag', default=False, blank=False) # values: ['f', 't']
    tribal_government_flag = models.BooleanField('tribalGovernmentFlag', default=False, blank=False) # values: ['f']
    baobflag = models.BooleanField('BAOBFlag', default=False, blank=False) # values: ['f', 't']
    naobflag = models.BooleanField('NAOBFlag', default=False, blank=False) # values: ['f', 't']
    saaobflag = models.BooleanField('SAAOBFlag', default=False, blank=False) # values: ['f', 't']
    nonprofit_organization_flag = models.BooleanField('nonprofitOrganizationFlag', default=False, blank=False) # values: ['f', 't']
    haobflag = models.BooleanField('HAOBFlag', default=False, blank=False) # values: ['f', 't']
    very_small_business_flag = models.BooleanField('verySmallBusinessFlag', default=False, blank=False) # values: ['f', 't']
    hospital_flag = models.BooleanField('hospitalFlag', default=False, blank=False) # values: ['f', 't']
    number_of_employees = models.IntegerField('numberOfEmployees', max_length=11, blank=True, null=True)
    organizational_type = models.CharField('organizationalType', max_length=30, blank=True, default='')
    street_address = models.CharField('streetAddress', max_length=55, blank=True, default='')
    street_address2 = models.CharField('streetAddress2', max_length=55, blank=True, default='')
    street_address3 = models.CharField('streetAddress3', max_length=55, blank=True, default='')
    city = models.CharField('city', max_length=35, blank=True, default='')
    state = models.CharField('state', max_length=2, blank=True, default='')
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
    vendor_location_disable_flag = models.BooleanField('vendorLocationDisableFlag', default=False, blank=True) # values: ['']
    contractor_name = models.CharField('contractorName', max_length=80, blank=True, default='')
    ccrexception = models.CharField('CCRException', max_length=1, blank=True, default='')
    contracting_officer_business_size_determination = models.BooleanField('contractingOfficerBusinessSizeDetermination', default=False, blank=True) # values: ['S', 'O', '']
    location_code = models.CharField('locationCode', max_length=5, blank=True, default='')
    state_code = models.CharField('stateCode', max_length=2, blank=True, default='')
    place_of_performance_country_code = models.CharField('placeOfPerformanceCountryCode', max_length=3, blank=True, default='')
    place_of_performance_zipcode = models.CharField('placeOfPerformanceZIPCode', max_length=10, blank=True, default='')
    place_of_performance_congressional_district = models.CharField('placeOfPerformanceCongressionalDistrict', max_length=6, blank=True, default='')
    extent_competed = models.CharField('extentCompeted', max_length=3, blank=True, default='')
    competitive_procedures = models.CharField('competitiveProcedures', max_length=3, blank=True, default='')
    solicitation_procedures = models.CharField('solicitationProcedures', max_length=5, blank=True, default='')
    type_of_set_aside = models.CharField('typeOfSetAside', max_length=10, blank=True, default='')
    evaluated_preference = models.CharField('evaluatedPreference', max_length=6, blank=True, default='')
    research = models.CharField('research', max_length=3, blank=True, default='')
    statutory_exception_to_fair_opportunity = models.CharField('statutoryExceptionToFairOpportunity', max_length=3, blank=True, default='')
    reason_not_competed = models.CharField('reasonNotCompeted', max_length=3, blank=True, default='')
    number_of_offers_received = models.IntegerField('numberOfOffersReceived', max_length=6, blank=True, null=True)
    commercial_item_acquisition_procedures = models.BooleanField('commercialItemAcquisitionProcedures', default=False, blank=True) # values: ['t', 'f', '']
    commercial_item_test_program = models.BooleanField('commercialItemTestProgram', default=False, blank=False) # values: ['t', 'f']
    small_business_competitiveness_demonstration_program = models.BooleanField('smallBusinessCompetitivenessDemonstrationProgram', default=False, blank=False) # values: ['f', 't']
    pre_award_synopsis_requirement = models.BooleanField('preAwardSynopsisRequirement', default=False, blank=False) # values: ['t', 'f']
    synopsis_waiver_exception = models.BooleanField('synopsisWaiverException', default=False, blank=False) # values: ['f', 't']
    alternative_advertising = models.BooleanField('alternativeAdvertising', default=False, blank=False) # values: ['f', 't']
    a76action = models.BooleanField('A76Action', default=False, blank=True) # values: ['f', '', 't']
    price_evaluation_percent_difference = models.CharField('priceEvaluationPercentDifference', max_length=2, blank=True, default='')
    subcontract_plan = models.CharField('subcontractPlan', max_length=1, blank=True, default='')
    reason_not_awarded_to_small_disadvantaged_business = models.CharField('reasonNotAwardedToSmallDisadvantagedBusiness', max_length=1, blank=True, default='')
    reason_not_awarded_to_small_business = models.CharField('reasonNotAwardedToSmallBusiness', max_length=1, blank=True, default='')
    created_by = models.CharField('createdBy', max_length=50, blank=True, default='')
    created_date = models.DateField('createdDate', blank=True, null=True)
    last_modified_by = models.CharField('lastModifiedBy', max_length=50, blank=True, default='')
    last_modified_date = models.DateField('lastModifiedDate', blank=True, null=True)
    status = models.BooleanField('status', default=False, blank=False) # values: ['F']
    agencyspecific_id = models.CharField('agencyspecificID', max_length=4, blank=True, default='')
    offerors_proposal_number = models.CharField('offerorsProposalNumber', max_length=18, blank=True, default='')
    prnumber = models.CharField('PRNumber', max_length=12, blank=True, default='')
    closeout_pr = models.BooleanField('closeoutPR', default=False, blank=True) # values: ['', 'f', 't']
    procurement_placement_code = models.CharField('procurementPlacementCode', max_length=2, blank=True, default='')
    solicitation_issue_date = models.DateField('solicitationIssueDate', blank=True, null=True)
    contract_administration_delegated = models.CharField('contractAdministrationDelegated', max_length=10, blank=True, default='')
    advisory_or_assistance_services_contract = models.BooleanField('advisoryOrAssistanceServicesContract', default=False, blank=True) # values: ['', 'f']
    support_services_type_contract = models.BooleanField('supportServicesTypeContract', default=False, blank=True) # values: ['', 'f', 't']
    new_technology_or_patent_rights_clause = models.BooleanField('newTechnologyOrPatentRightsClause', default=False, blank=True) # values: ['', 'f', 't']
    management_reporting_requirements = models.CharField('managementReportingRequirements', max_length=1, blank=True, default='')
    property_financial_reporting = models.BooleanField('propertyFinancialReporting', default=False, blank=True) # values: ['', 'f', 't']
    value_engineering_clause = models.BooleanField('valueEngineeringClause', default=False, blank=True) # values: ['', 'f', 't']
    security_code = models.BooleanField('securityCode', default=False, blank=True) # values: ['', 'f']
    administrator_code = models.CharField('administratorCode', max_length=3, blank=True, default='')
    contracting_officer_code = models.CharField('contractingOfficerCode', max_length=3, blank=True, default='')
    negotiator_code = models.CharField('negotiatorCode', max_length=3, blank=True, default='')
    cotrname = models.CharField('COTRName', max_length=15, blank=True, default='')
    alternate_cotrname = models.CharField('alternateCOTRName', max_length=15, blank=True, default='')
    organization_code = models.CharField('organizationCode', max_length=5, blank=True, default='')
    contract_fund_code = models.BooleanField('contractFundCode', default=False, blank=True) # values: ['', 'F', 'I']
    is_physically_complete = models.BooleanField('isPhysicallyComplete', default=False, blank=True) # values: ['', 'f', 't']
    physical_completion_date = models.DateField('physicalCompletionDate', blank=True, null=True)
    installation_unique = models.CharField('installationUnique', max_length=9, blank=True, default='')
    funded_through_date = models.DateField('fundedThroughDate', blank=True, null=True)
    cancellation_date = models.DateField('cancellationDate', blank=True, null=True)
    principal_investigator_first_name = models.CharField('principalInvestigatorFirstName', max_length=40, blank=True, default='')
    principal_investigator_middle_initial = models.CharField('principalInvestigatorMiddleInitial', max_length=6, blank=True, default='')
    principal_investigator_last_name = models.CharField('principalInvestigatorLastName', max_length=75, blank=True, default='')
    alternate_principal_investigator_first_name = models.CharField('alternatePrincipalInvestigatorFirstName', max_length=40, blank=True, default='')
    alternate_principal_investigator_middle_initial = models.CharField('alternatePrincipalInvestigatorMiddleInitial', max_length=6, blank=True, default='')
    alternate_principal_investigator_last_name = models.CharField('alternatePrincipalInvestigatorLastName', max_length=75, blank=True, default='')
    field_of_science_or_engineering = models.CharField('fieldOfScienceOrEngineering', max_length=2, blank=True, default='')
    final_invoice_paid_date = models.DateField('finalInvoicePaidDate', blank=True, null=True)
    accession_number = models.CharField('accessionNumber', max_length=20, blank=True, default='')
    destroy_date = models.DateField('destroyDate', blank=True, null=True)
    accounting_installation_number = models.CharField('accountingInstallationNumber', max_length=2, blank=True, default='')
    other_statutory_authority = models.TextField('otherStatutoryAuthority', blank=True, null=True)
    wild_fire_program = models.CharField('wildFireProgram', max_length=3, blank=True, default='')
    ee_parent_duns = models.CharField('eeParentDuns', max_length=13, blank=True, default='')
    parent_company = models.CharField('ParentCompany', max_length=100, blank=True, default='')
    po_pcd = models.CharField('PoPCD', max_length=10, blank=True, default='')
    fiscal_year = models.IntegerField('fiscal_year', max_length=6, blank=True, null=True)
    name_type = models.CharField('name_type', max_length=1, blank=True, default='')
    mod_name = models.CharField('mod_name', max_length=120, blank=True, default='')
    mod_parent = models.CharField('mod_parent', max_length=100, blank=True, default='')
    record_id = models.IntegerField('record_id', max_length=20, blank=True, null=True)
    parent_id = models.IntegerField('parent_id', max_length=20, blank=True, null=True)
    award_id = models.IntegerField('award_id', max_length=20, blank=True, null=True)
    idv_id = models.IntegerField('idv_id', max_length=20, blank=True, null=True)
    mod_sort = models.IntegerField('mod_sort', max_length=11, blank=True, null=True)
    compete_cat = models.CharField('compete_cat', max_length=1, blank=True, default='')
    maj_agency_cat = models.CharField('maj_agency_cat', max_length=2, blank=True, default='')
    psc_cat = models.CharField('psc_cat', max_length=2, blank=True, default='')
    setaside_cat = models.BooleanField('setaside_cat', default=False, blank=True) # values: ['']
    vendor_type = models.CharField('vendor_type', max_length=2, blank=True, default='')
    vendor_cd = models.CharField('vendor_cd', max_length=4, blank=True, default='')
    pop_cd = models.CharField('pop_cd', max_length=4, blank=True, default='')
    data_src = models.BooleanField('data_src', default=False, blank=False) # values: ['f']
    mod_agency = models.CharField('mod_agency', max_length=4, blank=True, default='')
    mod_eeduns = models.CharField('mod_eeduns', max_length=13, blank=True, default='')
    mod_dunsid = models.IntegerField('mod_dunsid', max_length=20, blank=True, null=True)
    mod_fund_agency = models.CharField('mod_fund_agency', max_length=4, blank=True, default='')
    maj_fund_agency_cat = models.CharField('maj_fund_agency_cat', max_length=2, blank=True, default='')
    prog_source_agency = models.CharField('ProgSourceAgency', max_length=2, blank=True, default='')
    prog_source_account = models.CharField('ProgSourceAccount', max_length=4, blank=True, default='')
    prog_source_sub_acct = models.CharField('ProgSourceSubAcct', max_length=3, blank=True, default='')
    rec_flag = models.BooleanField('rec_flag', default=False, blank=True) # values: ['']
    annual_revenue = models.DecimalField('annualRevenue', max_digits=20, decimal_places=2, blank=True, null=True)

