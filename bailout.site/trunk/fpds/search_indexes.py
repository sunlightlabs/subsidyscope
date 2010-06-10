import datetime
from haystack import indexes
from haystack.sites import site
from fpds.models import FPDSRecord, ExtentCompetedMapper

extent_competed_mapper = ExtentCompetedMapper()

class FPDSRecordIndex(indexes.SearchIndex):
    
    type = 'fpds'

    # sectors
    sectors = indexes.MultiValueField(null=False)
    subsectors = indexes.MultiValueField(null=True)

    # categories
    product_or_service_code = indexes.IntegerField(model_attr='product_or_service_code__id', null=True)
    principal_naicscode = indexes.IntegerField(model_attr='principal_naicscode__id', null=True)    

    # chrono
    fiscal_year = indexes.IntegerField(model_attr='fiscal_year', null=True) 
    obligation_date = indexes.DateField(model_attr='effective_date', null=True) # aka effective date
    
    # dollars
    obligated_amount = indexes.FloatField(model_attr='obligated_amount', null=True)

    # text
    text = indexes.CharField(model_attr='description_of_contract_requirement', null=True, document=True)
    vendor_name = indexes.CharField(model_attr='vendor_name', null=True)
    vendor_alternate_name = indexes.CharField(model_attr='vendor_alternate_name', null=True)
    contractor_name = indexes.CharField(model_attr='contractor_name', null=True)
    
    # geo
    principal_place_state = indexes.IntegerField(model_attr='place_of_performance_state__id', null=True)
    recipient_state = indexes.IntegerField(model_attr='state__id', null=True) # aka vendor state
    # city = indexes.CharField(model_attr='city', null=True) # necessary?
    # vendor_country_code = indexes.CharField(model_attr='vendor_country_code', null=True)
    # location_code = indexes.CharField(model_attr='location_code', null=True)

    # FPDS-only fields    
    # 1 = false; 2 = true -- cannot return 0 for haystack prepare_* or the field won't be indexed
    nonprofit_organization_flag = indexes.IntegerField(model_attr='nonprofit_organization_flag', null=True)
    educational_institution_flag = indexes.IntegerField(model_attr='educational_institution_flag', null=True)
    extent_competed = indexes.IntegerField(null=True)

    # TODO
    # 1. add extent competed, nonprofit and "educational institution" flags
    # 1a. make solr summing occur for summary/state/year AT THE SAME TIME. aha!
    # 2. get canary back up to speed for indexing
    # 3. reindex
    # 4. expose new fields through the interface
    # 5. collaborate with Kevin to investigate heap problems
    # 6. investigate solr multi-index operation
    

    # free text combination fields (for OR-based searches)
    recipient = indexes.CharField(null=True)
    all_text = indexes.CharField(null=True)
    all_states = indexes.MultiValueField(null=True)

    def prepare_nonprofit_organization_flag(self, object):
        if object.nonprofit_organization_flag:
            return 2
        else:
            return 1
            
    def prepare_educational_institution_flag(self, object):
        if object.educational_institution_flag:
            return 2
        else:
            return 1

    # def prepare_nonprofit_organization_flag(self, object):
    #     if object.nonprofit_organization_flag is True:
    #         return 1
    #     else:        
    #         return 0
    #             
    # def prepare_educational_institution_flag(self, object):
    #     print int(object.educational_institution_flag), object.educational_institution_flag
    #     return int(object.educational_institution_flag)
    # 
    def prepare_extent_competed(self, object):
        return extent_competed_mapper.assign_index(object.extent_competed)
    
    def prepare_recipient(self, object):
        s = "%s %s %s" % (getattr(object, 'vendor_name', ''), getattr(object, 'contractor_name', ''), getattr(object, 'vendor_alternate_name', ''))
        return len(s)>0 and s.strip() or None
    
    
    def prepare_all_text(self, object):
        s = "%s %s %s %s" % (getattr(object, 'vendor_name', ''), getattr(object, 'contractor_name', ''), getattr(object, 'vendor_alternate_name', ''), getattr(object, 'description_of_contract_requirement', ''))
        return len(s)>0 and s.strip() or None

    def prepare_all_states(self, object):
        r = []
        for f in ('place_of_performance_state', 'state'):
            s = getattr(object, f, None)
            if s is not None:
                i = getattr(s, 'id', None)
                if i is not None:
                    r.append(i)
                    
        return len(r)>0 and r or None
        

    def prepare_product_or_service_code(self, object):
        if object.product_or_service_code:
            return object.product_or_service_code.id
        else:
            return None

    def prepare_principal_naicscode(self, object):
        if object.principal_naicscode:
            return object.principal_naicscode.id
        else:
            return None

    def prepare_principal_place_state(self, object):
        if object.place_of_performance_state:
            return object.place_of_performance_state.id
        else:
            return None
            
    def prepare_recipient_state(self, object):
        if object.state:
            return object.state.id
        else:
            return None

    
    def prepare_fiscal_year(self, object):  
        if object.fiscal_year != None:
            return int(object.fiscal_year)
        else:
            return None
            
    def obligation_date(self, object):
        try:
            if object.effective_date.year > 1900:
                return object.effective_date
            else:
                return None
        except:
            return None
      
    def prepare_sectors(self, object):
        return map(lambda x: x.id, object.sectors.all())
        
    def prepare_subsectors(self, object):
        return map(lambda x: x.id, object.subsectors.all())

    
    def get_queryset(self):
        "Used when the entire index for model is updated."
        return FPDSRecord.objects.all()


site.register(FPDSRecord, FPDSRecordIndex)


# # unused model attributes follow
# 
# version = indexes.CharField(model_attr='version', null=True)
# agency_id = indexes.CharField(model_attr='agency_id', null=True)
# piid = indexes.CharField(model_attr='piid', null=True)
# mod_number = indexes.CharField(model_attr='mod_number', null=True)
# transaction_number = indexes.CharField(model_attr='transaction_number', null=True)    
# street_address = indexes.CharField(model_attr='street_address', null=True)
# street_address2 = indexes.CharField(model_attr='street_address2', null=True)
# street_address3 = indexes.CharField(model_attr='street_address3', null=True)         
# idvagency_id = indexes.CharField(model_attr='idvagency_id', null=True)
# idvpiid = indexes.CharField(model_attr='idvpiid', null=True)
# idvmodification_number = indexes.CharField(model_attr='idvmodification_number', null=True)
# signed_date = indexes.DateField(model_attr='signed_date', null=True)
# current_completion_date = indexes.DateField(model_attr='current_completion_date', null=True)
# ultimate_completion_date = indexes.DateField(model_attr='ultimate_completion_date', null=True)
# base_and_exercised_options_value = indexes.FloatField(model_attr='base_and_exercised_options_value', null=True)
# base_and_all_options_value = indexes.FloatField(model_attr='base_and_all_options_value', null=True)
# contracting_office_agency_id = indexes.CharField(model_attr='contracting_office_agency_id', null=True)
# contracting_office_id = indexes.CharField(model_attr='contracting_office_id', null=True)
# funding_requesting_agency_id = indexes.CharField(model_attr='funding_requesting_agency_id', null=True)
# funding_requesting_office_id = indexes.CharField(model_attr='funding_requesting_office_id', null=True)
# purchase_reason = indexes.CharField(model_attr='purchase_reason', null=True)
# funded_by_foreign_entity = indexes.NullBooleanField(model_attr='funded_by_foreign_entity', null=True)
# fee_paid_for_use_of_service = indexes.FloatField(model_attr='fee_paid_for_use_of_service', null=True)
# contract_action_type = indexes.CharField(model_attr='contract_action_type', null=True)
# type_of_contract_pricing = indexes.CharField(model_attr='type_of_contract_pricing', null=True)
# national_interest_action_code = indexes.CharField(model_attr='national_interest_action_code', null=True)
# reason_for_modification = indexes.CharField(model_attr='reason_for_modification', null=True)
# major_program_code = indexes.CharField(model_attr='major_program_code', null=True)
# cost_or_pricing_data = indexes.CharField(model_attr='cost_or_pricing_data', null=True)
# solicitation_id = indexes.CharField(model_attr='solicitation_id', null=True)
# cost_accounting_standards_clause = indexes.NullBooleanField(model_attr='cost_accounting_standards_clause', null=True)
# gfe_gfp = indexes.NullBooleanField(model_attr='gfe_gfp', null=True)
# sea_transportation = indexes.CharField(model_attr='sea_transportation', null=True)
# consolidated_contract = indexes.NullBooleanField(model_attr='consolidated_contract', null=True)
# letter_contract = indexes.NullBooleanField(model_attr='letter_contract', null=True)
# multi_year_contract = indexes.NullBooleanField(model_attr='multi_year_contract', null=True)
# performance_based_service_contract = indexes.NullBooleanField(model_attr='performance_based_service_contract', null=True)
# contingency_humanitarian_peacekeeping_operation = indexes.CharField(model_attr='contingency_humanitarian_peacekeeping_operation', null=True)
# contract_financing = indexes.CharField(model_attr='contract_financing', null=True)
# purchase_card_as_payment_method = indexes.NullBooleanField(model_attr='purchase_card_as_payment_method', null=True)
# number_of_actions = indexes.IntegerField(model_attr='number_of_actions', null=True)
# walsh_healy_act = indexes.NullBooleanField(model_attr='walsh_healy_act', null=True)
# service_contract_act = indexes.NullBooleanField(model_attr='service_contract_act', null=True)
# davis_bacon_act = indexes.NullBooleanField(model_attr='davis_bacon_act', null=True)
# clinger_cohen_act = indexes.NullBooleanField(model_attr='clinger_cohen_act', null=True)
# contract_bundling = indexes.CharField(model_attr='contract_bundling', null=True)
# claimant_program_code = indexes.CharField(model_attr='claimant_program_code', null=True)
# recovered_material_clauses = indexes.CharField(model_attr='recovered_material_clauses', null=True)
# system_equipment_code = indexes.CharField(model_attr='system_equipment_code', null=True)
# information_technology_commercial_item_category = indexes.CharField(model_attr='information_technology_commercial_item_category', null=True)
# use_of_epadesignated_products = indexes.CharField(model_attr='use_of_epadesignated_products', null=True)
# country_of_origin = indexes.CharField(model_attr='country_of_origin', null=True)
# place_of_manufacture = indexes.CharField(model_attr='place_of_manufacture', null=True)
# vendor_legal_organization_name = indexes.CharField(model_attr='vendor_legal_organization_name', null=True)
# vendor_doing_as_business_name = indexes.CharField(model_attr='vendor_doing_as_business_name', null=True)
# vendor_enabled = indexes.NullBooleanField(model_attr='vendor_enabled', null=True)
# small_business_flag = indexes.NullBooleanField(model_attr='small_business_flag', null=True)
# firm8aflag = indexes.NullBooleanField(model_attr='firm8aflag', null=True)
# hubzone_flag = indexes.NullBooleanField(model_attr='hubzone_flag', null=True)
# sdbflag = indexes.NullBooleanField(model_attr='sdbflag', null=True)
# sheltered_workshop_flag = indexes.NullBooleanField(model_attr='sheltered_workshop_flag', null=True)
# hbcuflag = indexes.NullBooleanField(model_attr='hbcuflag', null=True)
# educational_institution_flag = indexes.NullBooleanField(model_attr='educational_institution_flag', null=True)
# women_owned_flag = indexes.NullBooleanField(model_attr='women_owned_flag', null=True)
# veteran_owned_flag = indexes.NullBooleanField(model_attr='veteran_owned_flag', null=True)
# srdvobflag = indexes.NullBooleanField(model_attr='srdvobflag', null=True)
# local_government_flag = indexes.NullBooleanField(model_attr='local_government_flag', null=True)
# minority_institution_flag = indexes.NullBooleanField(model_attr='minority_institution_flag', null=True)
# aiobflag = indexes.NullBooleanField(model_attr='aiobflag', null=True)
# state_government_flag = indexes.NullBooleanField(model_attr='state_government_flag', null=True)
# federal_government_flag = indexes.NullBooleanField(model_attr='federal_government_flag', null=True)
# minority_owned_business_flag = indexes.NullBooleanField(model_attr='minority_owned_business_flag', null=True)
# apaobflag = indexes.NullBooleanField(model_attr='apaobflag', null=True)
# tribal_government_flag = indexes.NullBooleanField(model_attr='tribal_government_flag', null=True)
# baobflag = indexes.NullBooleanField(model_attr='baobflag', null=True)
# naobflag = indexes.NullBooleanField(model_attr='naobflag', null=True)
# saaobflag = indexes.NullBooleanField(model_attr='saaobflag', null=True)
# nonprofit_organization_flag = indexes.NullBooleanField(model_attr='nonprofit_organization_flag', null=True)
# haobflag = indexes.NullBooleanField(model_attr='haobflag', null=True)
# very_small_business_flag = indexes.NullBooleanField(model_attr='very_small_business_flag', null=True)
# hospital_flag = indexes.NullBooleanField(model_attr='hospital_flag', null=True)
# number_of_employees = indexes.IntegerField(model_attr='number_of_employees', null=True)
# organizational_type = indexes.CharField(model_attr='organizational_type', null=True)
# dunsnumber = indexes.CharField(model_attr='dunsnumber', null=True)
# parent_dunsnumber = indexes.CharField(model_attr='parent_dunsnumber', null=True)
# phone_no = indexes.CharField(model_attr='phone_no', null=True)
# fax_no = indexes.CharField(model_attr='fax_no', null=True)
# division_name = indexes.CharField(model_attr='division_name', null=True)
# division_number_or_office_code = indexes.CharField(model_attr='division_number_or_office_code', null=True)
# registration_date = indexes.DateField(model_attr='registration_date', null=True)
# renewal_date = indexes.DateField(model_attr='renewal_date', null=True)
# vendor_location_disable_flag = indexes.NullBooleanField(model_attr='vendor_location_disable_flag', null=True)
# congressional_district = indexes.CharField(model_attr='congressional_district', null=True)
# ccrexception = indexes.CharField(model_attr='ccrexception', null=True)
# contracting_officer_business_size_determination = indexes.CharField(model_attr='contracting_officer_business_size_determination', null=True)
# extent_competed = indexes.CharField(model_attr='extent_competed', null=True)
# competitive_procedures = indexes.CharField(model_attr='competitive_procedures', null=True)
# solicitation_procedures = indexes.CharField(model_attr='solicitation_procedures', null=True)
# type_of_set_aside = indexes.CharField(model_attr='type_of_set_aside', null=True)
# evaluated_preference = indexes.CharField(model_attr='evaluated_preference', null=True)
# research = indexes.CharField(model_attr='research', null=True)
# statutory_exception_to_fair_opportunity = indexes.CharField(model_attr='statutory_exception_to_fair_opportunity', null=True)
# reason_not_competed = indexes.CharField(model_attr='reason_not_competed', null=True)
# number_of_offers_received = indexes.IntegerField(model_attr='number_of_offers_received', null=True)
# commercial_item_acquisition_procedures = indexes.NullBooleanField(model_attr='commercial_item_acquisition_procedures', null=True)
# commercial_item_test_program = indexes.NullBooleanField(model_attr='commercial_item_test_program', null=True)
# small_business_competitiveness_demonstration_program = indexes.NullBooleanField(model_attr='small_business_competitiveness_demonstration_program', null=True)
# pre_award_synopsis_requirement = indexes.NullBooleanField(model_attr='pre_award_synopsis_requirement', null=True)
# synopsis_waiver_exception = indexes.NullBooleanField(model_attr='synopsis_waiver_exception', null=True)
# alternative_advertising = indexes.NullBooleanField(model_attr='alternative_advertising', null=True)
# a76action = indexes.NullBooleanField(model_attr='a76action', null=True)
# price_evaluation_percent_difference = indexes.CharField(model_attr='price_evaluation_percent_difference', null=True)
# subcontract_plan = indexes.CharField(model_attr='subcontract_plan', null=True)
# reason_not_awarded_to_small_disadvantaged_business = indexes.CharField(model_attr='reason_not_awarded_to_small_disadvantaged_business', null=True)
# reason_not_awarded_to_small_business = indexes.CharField(model_attr='reason_not_awarded_to_small_business', null=True)
# created_by = indexes.CharField(model_attr='created_by', null=True)
# created_date = indexes.DateField(model_attr='created_date', null=True)
# last_modified_by = indexes.CharField(model_attr='last_modified_by', null=True)
# last_modified_date = indexes.DateField(model_attr='last_modified_date', null=True)
# status = indexes.NullBooleanField(model_attr='status', null=True)
# agencyspecific_id = indexes.CharField(model_attr='agencyspecific_id', null=True)
# offerors_proposal_number = indexes.CharField(model_attr='offerors_proposal_number', null=True)
# prnumber = indexes.CharField(model_attr='prnumber', null=True)
# closeout_pr = indexes.NullBooleanField(model_attr='closeout_pr', null=True)
# procurement_placement_code = indexes.CharField(model_attr='procurement_placement_code', null=True)
# solicitation_issue_date = indexes.DateField(model_attr='solicitation_issue_date', null=True)
# contract_administration_delegated = indexes.CharField(model_attr='contract_administration_delegated', null=True)
# advisory_or_assistance_services_contract = indexes.NullBooleanField(model_attr='advisory_or_assistance_services_contract', null=True)
# support_services_type_contract = indexes.NullBooleanField(model_attr='support_services_type_contract', null=True)
# new_technology_or_patent_rights_clause = indexes.NullBooleanField(model_attr='new_technology_or_patent_rights_clause', null=True)
# management_reporting_requirements = indexes.CharField(model_attr='management_reporting_requirements', null=True)
# property_financial_reporting = indexes.NullBooleanField(model_attr='property_financial_reporting', null=True)
# value_engineering_clause = indexes.NullBooleanField(model_attr='value_engineering_clause', null=True)
# security_code = indexes.NullBooleanField(model_attr='security_code', null=True)
# administrator_code = indexes.CharField(model_attr='administrator_code', null=True)
# contracting_officer_code = indexes.CharField(model_attr='contracting_officer_code', null=True)
# negotiator_code = indexes.CharField(model_attr='negotiator_code', null=True)
# cotrname = indexes.CharField(model_attr='cotrname', null=True)
# alternate_cotrname = indexes.CharField(model_attr='alternate_cotrname', null=True)
# organization_code = indexes.CharField(model_attr='organization_code', null=True)
# contract_fund_code = indexes.CharField(model_attr='contract_fund_code', null=True)
# is_physically_complete = indexes.NullBooleanField(model_attr='is_physically_complete', null=True)
# physical_completion_date = indexes.DateField(model_attr='physical_completion_date', null=True)
# installation_unique = indexes.CharField(model_attr='installation_unique', null=True)
# funded_through_date = indexes.DateField(model_attr='funded_through_date', null=True)
# cancellation_date = indexes.DateField(model_attr='cancellation_date', null=True)
# principal_investigator_first_name = indexes.CharField(model_attr='principal_investigator_first_name', null=True)
# principal_investigator_middle_initial = indexes.CharField(model_attr='principal_investigator_middle_initial', null=True)
# principal_investigator_last_name = indexes.CharField(model_attr='principal_investigator_last_name', null=True)
# alternate_principal_investigator_first_name = indexes.CharField(model_attr='alternate_principal_investigator_first_name', null=True)
# alternate_principal_investigator_middle_initial = indexes.CharField(model_attr='alternate_principal_investigator_middle_initial', null=True)
# alternate_principal_investigator_last_name = indexes.CharField(model_attr='alternate_principal_investigator_last_name', null=True)
# field_of_science_or_engineering = indexes.CharField(model_attr='field_of_science_or_engineering', null=True)
# final_invoice_paid_date = indexes.DateField(model_attr='final_invoice_paid_date', null=True)
# accession_number = indexes.CharField(model_attr='accession_number', null=True)
# destroy_date = indexes.DateField(model_attr='destroy_date', null=True)
# accounting_installation_number = indexes.CharField(model_attr='accounting_installation_number', null=True)
# other_statutory_authority = indexes.CharField(model_attr='other_statutory_authority', null=True)
# wild_fire_program = indexes.CharField(model_attr='wild_fire_program', null=True)
# ee_parent_duns = indexes.CharField(model_attr='ee_parent_duns', null=True)
# parent_company = indexes.CharField(model_attr='parent_company', null=True)
# po_pcd = indexes.CharField(model_attr='po_pcd', null=True)
# name_type = indexes.CharField(model_attr='name_type', null=True)
# mod_name = indexes.CharField(model_attr='mod_name', null=True)
# mod_parent = indexes.CharField(model_attr='mod_parent', null=True)
# record_id = indexes.IntegerField(model_attr='record_id', null=True)
# parent_id = indexes.IntegerField(model_attr='parent_id', null=True)
# award_id = indexes.IntegerField(model_attr='award_id', null=True)
# idv_id = indexes.IntegerField(model_attr='idv_id', null=True)
# mod_sort = indexes.IntegerField(model_attr='mod_sort', null=True)
# compete_cat = indexes.CharField(model_attr='compete_cat', null=True)
# maj_agency_cat = indexes.CharField(model_attr='maj_agency_cat', null=True)
# psc_cat = indexes.CharField(model_attr='psc_cat', null=True)
# setaside_cat = indexes.NullBooleanField(model_attr='setaside_cat', null=True)
# vendor_type = indexes.CharField(model_attr='vendor_type', null=True)
# vendor_cd = indexes.CharField(model_attr='vendor_cd', null=True)
# pop_cd = indexes.CharField(model_attr='pop_cd', null=True)
# data_src = indexes.NullBooleanField(model_attr='data_src', null=True)
# mod_agency = indexes.CharField(model_attr='mod_agency', null=True)
# mod_eeduns = indexes.CharField(model_attr='mod_eeduns', null=True)
# mod_dunsid = indexes.IntegerField(model_attr='mod_dunsid', null=True)
# mod_fund_agency = indexes.CharField(model_attr='mod_fund_agency', null=True)
# maj_fund_agency_cat = indexes.CharField(model_attr='maj_fund_agency_cat', null=True)
# prog_source_agency = indexes.CharField(model_attr='prog_source_agency', null=True)
# prog_source_account = indexes.CharField(model_attr='prog_source_account', null=True)
# prog_source_sub_acct = indexes.CharField(model_attr='prog_source_sub_acct', null=True)
# rec_flag = indexes.NullBooleanField(model_attr='rec_flag', null=True)
# annual_revenue = indexes.FloatField(model_attr='annual_revenue', null=True)