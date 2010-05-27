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

energy_grants = Line(500, 350, [[(2000, 1369492264 ), (2001, 1473169350), (2002, 1745534793), (2003, 1874157383), (2004, 2126602907), (2005, 2111786331), (2006, 2073310654), (2007, 2165902524), (2008, 2034990461), (2009, 13504402487)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")
energy_grants.output('./energy/energy_direct_expenditures_billions.svg')

#energy consumption, group of 5 pie charts, 1 large 4 small

primary_energy_consumption = Pie(475, 310, [[('Petroleum', 37), ('Coal', 23), ('Natural Gas', 24), ('Nuclear', 9), ('Renewable', 7)]], 'piechart_orange.css', y_padding=30, x_padding=120)
primary_energy_consumption.output("./energy/US_primary_energy_consumption_by_source_and_sector_2008.svg")

#little charts
transportation_energy_consumption = Pie(120, 100, [[('Natural Gas', 677), ('Petroleum', 26332), ('Renewables', 833)]], 'piechart_no_label.css')
transportation_energy_consumption.output('./energy/energy_consumption_transportation_2008_SMALL.svg')

industrial_energy_consumption = Pie(120, 100, [[('Natural Gas', 8149), ('Petroleum', 8586), ('Coal', 1840), ('Renewables', 2056)]], 'piechart_no_label.css')
industrial_energy_consumption.output('./energy/energy_consumption_industrial_2008_SMALL.svg')

residential_commerical_energy_consumption = Pie(120, 100, [[('Natural Gas', 8198), ('Petroleum', 1756), ('Coal', 74), ('Renewables', 722)]], 'piechart_no_label.css')
residential_commerical_energy_consumption.output('./energy/energy_residential_and_commercial_industrial_2008_SMALL.svg')

electric_energy_consumption = Pie(120, 100, [[('Natural Gas', 6823), ('Petroleum', 463), ('Coal', 20547), ('Renewables', 3690), ('Nuclear Electric power', 8455), ('Imports', 112)]], 'piechart_no_label.css')
electric_energy_consumption.output('./energy/energy_consumption_electric_2008_SMALL.svg')
