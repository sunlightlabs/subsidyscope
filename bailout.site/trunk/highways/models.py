from django.db import models

from geo.models import State 

class NationalFunding(models.Model):

    year = models.IntegerField()
    
    LEVEL_FEDERAL_HTF = 1
    LEVEL_FEDERAL_OTHER = 2
    LEVEL_STATE = 3
    LEVEL_LOCAL = 4
    
    LEVEL_CHOICES = ((LEVEL_FEDERAL_HTF, 'Federal - HTF'),
                     (LEVEL_FEDERAL_OTHER, 'Federal - Other'),
                     (LEVEL_STATE, 'State'),
                     (LEVEL_LOCAL, 'Local'))
    
    level_of_government = models.IntegerField("Level of Government", choices=LEVEL_CHOICES)
    
    
    net_collections = models.DecimalField("Net user collections", max_digits=15, decimal_places=2, null=True)
    less_nonhighway_purposes = models.DecimalField("Less non-highway purposes", max_digits=15, decimal_places=2, null=True)
    less_mass_transit = models.DecimalField("Less mass transit", max_digits=15, decimal_places=2, null=True)
    less_collection_expenses = models.DecimalField("Less collection expenses", max_digits=15, decimal_places=2, null=True)
    less_territories = models.DecimalField("Less Territories", max_digits=15, decimal_places=2, null=True)
    
    revenue_fuel_vehicle_taxes = models.DecimalField("Revenue from Fuel and Vehicle Taxes (User)", max_digits=15, decimal_places=2, null=True)
    revenue_tolls = models.DecimalField("Revenue from Tolls (User)", max_digits=15, decimal_places=2, null=True)
    
    revenue_property_taxes = models.DecimalField("Revenue from Property Taxes (Non-User)", max_digits=15, decimal_places=2, null=True)
    revenue_general_funds = models.DecimalField("Revenue from General Funds (Non-User)", max_digits=15, decimal_places=2, null=True)
    revenue_other_taxes = models.DecimalField("Revenue from Other Taxes (Non-User)", max_digits=15, decimal_places=2, null=True)
    
    revenue_investment_income = models.DecimalField("Revenue from Investments and Other Receipts (Non-User)", max_digits=15, decimal_places=2, null=True)
    revenue_bond_proceeds = models.DecimalField("Revenue from Bond Proceeds (Non-User)", max_digits=15, decimal_places=2, null=True)
    
    intergovt_transfer_federal = models.DecimalField("Intergovernmental Payment to Federal", max_digits=15, decimal_places=2, null=True)
    intergovt_transfer_state = models.DecimalField("Intergovernmental Payment to State", max_digits=15, decimal_places=2, null=True)
    intergovt_transfer_local = models.DecimalField("Intergovernmental Payment to Local", max_digits=15, decimal_places=2, null=True)
    
    reserves_allocations =  models.DecimalField("Funds Placed or Drawn From Reserves", max_digits=15, decimal_places=2, null=True)
    
    expense_capital_state_roads = models.DecimalField("Expense for Capital on State Roads", max_digits=15, decimal_places=2, null=True)
    expense_capital_local_roads = models.DecimalField("Expense for Capital on Local Roads", max_digits=15, decimal_places=2, null=True)
    expense_capital_unclassified_roads = models.DecimalField("Expense for Capital on Unclassified Roads", max_digits=15, decimal_places=2, null=True)
    
    expense_maintenance_state_roads = models.DecimalField("Expense for Maintenance on State Roads", max_digits=15, decimal_places=2, null=True)
    expense_maintenance_local_roads = models.DecimalField("Expense for Maintenance on Local Roads", max_digits=15, decimal_places=2, null=True)
    expense_maintenance_unclassified_roads = models.DecimalField("Expense for Maintenance on Unclassified Roads", max_digits=15, decimal_places=2, null=True)
     
    expense_administration_research = models.DecimalField("Expense for Administration and Research", max_digits=15, decimal_places=2, null=True)
    expense_highway_safety = models.DecimalField("Expense for Highway Law Enforcement/Safety", max_digits=15, decimal_places=2, null=True)
    expense_interest = models.DecimalField("Expense for Interest on Debt", max_digits=15, decimal_places=2, null=True)
    expense_bond_retirements = models.DecimalField("Expense for Bond Retirements", max_digits=15, decimal_places=2, null=True)
    
    

class StateFundingManager(models.Manager):
    
    def getFundingByGovt(self, state_id):
         
        funding = {}
         
        for record in self.filter(state__id=state_id, year__gte=1995):
            
            year = record.year 
            if not funding.has_key(year):
                funding[year] = {}
                funding[year]['federal'] = 0
                funding[year]['state'] = 0
                funding[year]['local'] = 0
                
            funding[year]['federal'] += record.sf1_fhwa_funds_for_highways if record.sf1_fhwa_funds_for_highways else 0
            funding[year]['federal'] += record.sf1_other_federal_funds_for_highways if record.sf1_other_federal_funds_for_highways else 0
            funding[year]['federal'] += record.lgf1_fhwa_funds_for_highways if record.lgf1_fhwa_funds_for_highways else 0
            funding[year]['federal'] += record.lgf1_other_federal_funds_for_highways if record.lgf1_other_federal_funds_for_highways else 0
            
            funding[year]['state'] += record.sf1_fuel_revenue_for_highways if record.sf1_fuel_revenue_for_highways else 0
            funding[year]['state'] += record.sf1_vehicle_revenue_for_highways if record.sf1_vehicle_revenue_for_highways else 0
            funding[year]['state'] += record.sf1_toll_revenue_for_highways if record.sf1_toll_revenue_for_highways else 0
            funding[year]['state'] += record.sf1_general_funds_for_highways if record.sf1_general_funds_for_highways else 0
            funding[year]['state'] += record.sf1_other_imposts_for_highways if record.sf1_other_imposts_for_highways else 0
            funding[year]['state'] += record.sf1_miscellanious_for_highways if record.sf1_miscellanious_for_highways else 0
            funding[year]['state'] += record.sf1_bonds_original_for_highways if record.sf1_bonds_original_for_highways else 0
            funding[year]['state'] += record.sf1_bonds_refunding_for_highways if record.sf1_bonds_refunding_for_highways else 0
            
            funding[year]['local'] += record.lgf1_fuel_vehicle_revenue_for_highways if record.lgf1_fuel_vehicle_revenue_for_highways else 0
            funding[year]['local'] += record.lgf1_toll_revenue_for_highways if record.lgf1_toll_revenue_for_highways else 0
            funding[year]['local'] += record.lgf1_general_funds_for_highways if record.lgf1_general_funds_for_highways else 0
            funding[year]['local'] += record.lgf1_property_tax_funds_for_highways if record.lgf1_property_tax_funds_for_highways else 0
            funding[year]['local'] += record.lgf1_other_imposts_for_highways if record.lgf1_other_imposts_for_highways else 0
            funding[year]['local'] += record.lgf1_miscellanious_for_highways if record.lgf1_miscellanious_for_highways else 0
            funding[year]['local'] += record.lgf1_bonds_original_for_highways if record.lgf1_bonds_original_for_highways else 0
            funding[year]['local'] += record.lgf1_bonds_refunding_for_highways if record.lgf1_bonds_refunding_for_highways else 0
            
            funding[year]['federal'] = int(funding[year]['federal'])
            funding[year]['state'] = int(funding[year]['state'])
            funding[year]['local'] = int(funding[year]['local'])
            
            
        return funding
         
         
    
    def getFundingBySource(self, state_id):
        
        funding = {}
         
        for record in self.filter(state__id=state_id, year__gte=1995):
            
            year = record.year 
            if not funding.has_key(year):
                funding[year] = {}
                funding[year]['state_user'] = 0
                funding[year]['state_non_user'] = 0
                funding[year]['state_bonds'] = 0
                funding[year]['local_user'] = 0
                funding[year]['local_non_user'] = 0
                funding[year]['local_bonds'] = 0
                funding[year]['federal'] = 0 
    
    
            funding[year]['state_user'] += record.sf1_fuel_revenue_for_highways if record.sf1_fuel_revenue_for_highways else 0
            funding[year]['state_user'] += record.sf1_vehicle_revenue_for_highways if record.sf1_vehicle_revenue_for_highways else 0
            funding[year]['state_user'] += record.sf1_toll_revenue_for_highways if record.sf1_toll_revenue_for_highways else 0
            
            funding[year]['local_user'] += record.lgf1_fuel_vehicle_revenue_for_highways if record.lgf1_fuel_vehicle_revenue_for_highways else 0
            funding[year]['local_user'] += record.lgf1_toll_revenue_for_highways if record.lgf1_toll_revenue_for_highways else 0
            
            
            
            funding[year]['state_non_user'] += record.sf1_general_funds_for_highways if record.sf1_general_funds_for_highways else 0
            funding[year]['state_non_user'] += record.sf1_other_imposts_for_highways if record.sf1_other_imposts_for_highways else 0
            funding[year]['state_non_user'] += record.sf1_miscellanious_for_highways if record.sf1_miscellanious_for_highways else 0
            
            funding[year]['local_non_user'] += record.lgf1_general_funds_for_highways if record.lgf1_general_funds_for_highways else 0
            funding[year]['local_non_user'] += record.lgf1_property_tax_funds_for_highways if record.lgf1_property_tax_funds_for_highways else 0
            funding[year]['local_non_user'] += record.lgf1_other_imposts_for_highways if record.lgf1_other_imposts_for_highways else 0
            funding[year]['local_non_user'] += record.lgf1_miscellanious_for_highways if record.lgf1_miscellanious_for_highways else 0
            
            
            
            funding[year]['state_bonds'] += record.sf1_bonds_original_for_highways if record.sf1_bonds_original_for_highways else 0
            funding[year]['state_bonds'] += record.sf1_bonds_refunding_for_highways if record.sf1_bonds_refunding_for_highways else 0
                        
            funding[year]['local_bonds'] += record.lgf1_bonds_original_for_highways if record.lgf1_bonds_original_for_highways else 0
            funding[year]['local_bonds'] += record.lgf1_bonds_refunding_for_highways if record.lgf1_bonds_refunding_for_highways else 0
            
                        
                        
            funding[year]['federal'] += record.sf1_fhwa_funds_for_highways if record.sf1_fhwa_funds_for_highways else 0
            funding[year]['federal'] += record.sf1_other_federal_funds_for_highways if record.sf1_other_federal_funds_for_highways else 0
            funding[year]['federal'] += record.lgf1_fhwa_funds_for_highways if record.lgf1_fhwa_funds_for_highways else 0
            funding[year]['federal'] += record.lgf1_other_federal_funds_for_highways if record.lgf1_other_federal_funds_for_highways else 0
            
            
    
            funding[year]['state_user'] = int(funding[year]['state_user'])
            funding[year]['state_non_user'] = int(funding[year]['state_non_user'])
            funding[year]['state_bonds'] = int(funding[year]['state_bonds'])
            
            funding[year]['local_user'] = int(funding[year]['local_user'])
            funding[year]['local_non_user'] = int(funding[year]['local_non_user'])
            funding[year]['local_bonds'] = int(funding[year]['local_bonds'])
            
            funding[year]['federal'] = int(funding[year]['federal']) 
            
            
        return funding


class StateFunding(models.Model):
    
    objects = StateFundingManager()
    
    state = models.ForeignKey(State)
    year = models.IntegerField()
    
    
    # sf1 fields
    sf1_fuel_revenue_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_vehicle_revenue_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_toll_revenue_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    sf1_general_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_other_imposts_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_miscellanious_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    sf1_bonds_original_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_bonds_refunding_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    sf1_fhwa_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_other_federal_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sf1_local_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    
    # sdf fields
    sdf_state_fuel_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_fuel_for_collection = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_fuel_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_fuel_for_general  = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    sdf_state_vehicle_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_vehicle_for_collection = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_vehicle_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_vehicle_for_general = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    sdf_state_toll_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_toll_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sdf_state_toll_for_general = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    
    # lgf1 fields
    lgf1_fuel_vehicle_revenue_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_toll_revenue_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    lgf1_general_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_property_tax_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_other_imposts_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_miscellanious_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    lgf1_bonds_original_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_bonds_refunding_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    lgf1_state_highway_user_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_other_state_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    lgf1_fhwa_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lgf1_other_federal_funds_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)


    # ldf
    ldf_state_user_revenue_available = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_state_user_revenue_used_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_state_user_revenue_used_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_state_user_revenue_used_for_general = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    ldf_local_fuel_vehicle_available = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_local_fuel_vehicle_revenue_for_highways = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_local_fuel_vehicle_revenue_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_local_fuel_vehicle_revenue_for_general = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    
    ldf_local_toll_revenue_available = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_local_toll_revenue_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_local_toll_revenue_for_mass_transit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ldf_local_toll_revenue_for_general = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    

