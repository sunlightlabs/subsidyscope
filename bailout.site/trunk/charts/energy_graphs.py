from charts import *

primary_energy = Column(480, 340, [[('Coal', 23.9), ('Natural Gas', 21.2), ('Crude Oil', 10.5), ('Nuclear Electric Power', 8.5), ('Biomass', 3.9), ('Hydroelectric Power', 2.5), ('Natural Gas Plant Liquids', 2.4), ('Wind, Geothermal, Solar P/V', 1.0)]], "barchart.css", label_rotate=-35, x_label_padding=10, x_label_height=100)
primary_energy.output("./energy/US_primary_energy_production_by_major_source_2008.svg")

primary_energy_consumption = Pie(475, 310, [[('Petroleum', 37), ('Non-Fossil', 17), ('Coal', 22), ('Natural Gas', 24)]], 'piechart_orange.css', y_padding=30, x_padding=120)
primary_energy_consumption.output("./energy/US_primary_energy_consumption_by_major_fuel_type_2008.svg")

energy_related_CO2 = Pie(475, 310, [[('Petroleum', 42), ('Coal', 37), ('Natural Gas', 21)]], 'piechart.css', y_padding=30, x_padding=120)
energy_related_CO2.output("./energy/US_energy_related_CO2_emissions_by_major_fuel_type_2009.svg")

electric_power = Pie(495, 310, [[('Petroleum', 1.1), ('Coal', 48.2), ('Other', 0.6), ('Natural Gas', 21.4), ('Other Renewables', 3.1), ('Nuclear', 19.6), ('Hydroelectric', 6.0)]], 'piechart.css', y_padding=30, x_padding=130)
electric_power.output('./energy/US_electric_power_industry_net_generation_2008.svg')

energy_tax_expenditures = Pie(700, 400, [[('Coal and refined Coal', 2660), ('Nuclear', 199), ('Natural Gas and \nPetroleum Liquids', 2090), ('Renewables', 670), ('Electricity (not fuel specific)', 735), ('End Use', 120), ('Conservation', 670)]], 'piechart.css', y_padding=30, x_padding=180)
energy_tax_expenditures.output('./energy/energy_tax_expenditures_by_fuel_type_2007.svg')

energy_nc_contracts = Line(500, 350, [[(2000, 7677302177.38), (2001, 1768682830.59), (2002,  2332004092.37), (2003, 2518815327.42), (2004, 3526604913.88), (2005, 4348697450.95), (2006, 7184534121.06), (2007, 3042779663.11), (2008, 5026602271.39), (2009, 4261998770.56)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")
energy_nc_contracts.output('./energy/energy_noncompeted_contracts_billions.svg')
