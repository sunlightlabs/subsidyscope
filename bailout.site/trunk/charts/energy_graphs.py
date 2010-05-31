from charts import *

primary_energy = Column(480, 340, [[('Coal', 23.9), 
				    ('Natural Gas', 21.2), 
				    ('Crude Oil', 10.5), 
				    ('Nuclear Electric Power', 8.5), 
				    ('Biomass', 3.9), 
				    ('Hydroelectric Power', 2.5), 
				    ('Natural Gas Plant Liquids', 2.4), 
				    ('Wind, Geothermal, Solar P/V', 1.0)]], "barchart.css", label_rotate=-35, x_label_padding=10, x_label_height=100)
primary_energy.output("../media/images/charts/energy/US_primary_energy_production_by_major_source_2008.svg")

primary_energy_consumption = Pie(475, 310, [[('Petroleum', 37), 
					     ('Non-Fossil', 17), 
					     ('Coal', 22), 
					     ('Natural Gas', 24)]], 'piechart_orange.css', y_padding=30, x_padding=120, padding=0)
primary_energy_consumption.output("../media/images/charts/energy/US_primary_energy_consumption_by_major_fuel_type_2008.svg")

energy_related_CO2 = Pie(475, 310, [[('Petroleum', 42), 
                                     ('Coal', 37),  
                                     ('Natural Gas', 21)]], 'piechart.css', y_padding=30, x_padding=100, padding=0)
energy_related_CO2.output("../media/images/charts/energy/US_energy_related_CO2_emissions_by_major_fuel_type_2009.svg")

electric_power = Pie(650, 400, [[('Petroleum', 1.1), 
                                 ('Coal', 48.2), 
                                 ('Other', 0.6), 
                                 ('Natural Gas', 21.4), 
                                 ('Other Renewables', 3.1), 
                                 ('Nuclear', 19.6), 
                                 ('Hydroelectric', 6.0)]], 'piechart.css', y_padding=5, x_padding=120)
electric_power.output('../media/images/charts/energy/US_electric_power_industry_net_generation_2008.svg')

energy_tax_expenditures = Pie(650, 400, [[('Coal and refined Coal', 2660), 
                                          ('Nuclear', 199), 
                                          ('Natural Gas and \nPetroleum Liquids', 2090), 
                                          ('Renewables', 670), 
                                          ('Electricity (not fuel specific)', 735), 
                                          ('End Use', 120), 
                                          ('Conservation', 670)]], 'piechart.css', y_padding=30, x_padding=145)
energy_tax_expenditures.output('../media/images/charts/energy/energy_tax_expenditures_by_fuel_type_2007.svg')

energy_nc_contracts = Line(500, 350, [[ (2000, 7677302177.38), 
                                        (2001, 1768682830.59), 
                                        (2002,  2332004092.37), 
                                        (2003, 2518815327.42), 
                                        (2004, 3526604913.88), 
                                        (2005, 4348697450.95), 
                                        (2006, 7184534121.06), 
                                        (2007, 3042779663.11), 
                                        (2008, 5026602271.39), 
                                        (2009, 4261998770.56)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")
energy_nc_contracts.output('../media/images/charts/energy/energy_noncompeted_contracts_billions.svg')

energy_grants = Line(500, 350, [[ (2000, 1369492264 ), 
                                  (2001, 1473169350), 
                                  (2002, 1745534793), 
                                  (2003, 1874157383), 
                                  (2004, 2126602907), 
                                  (2005, 2111786331), 
                                  (2006, 2073310654), 
                                  (2007, 2165902524), 
                                  (2008, 2034990461), 
                                  (2009, 13504402487)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")
energy_grants.output('../media/images/charts/energy/energy_direct_expenditures_billions.svg')

#energy consumption, group of 5 pie charts, 1 large 4 small

primary_energy_consumption = Pie(600, 450, [[('Petroleum', 37), 
                                             ('Coal', 23), 
                                             ('Natural Gas', 24), 
                                             ('Nuclear', 9), 
                                             ('Renewable', 7)]], 'piechart.css', y_padding=5, x_padding=60)
primary_energy_consumption.output("../media/images/charts/energy/US_primary_energy_consumption_by_source_and_sector_2008.svg")

#little charts
transportation_energy_consumption = Pie(120, 120, [[('Petroleum', 26332),
                                                    ('', 0), #dummy so colors are consistent
                                                    ('Natural Gas', 677),
                                                    ('', 0), #dummy
                                                    ('Renewable', 833)]], 'piechart_no_label.css', padding=3)
transportation_energy_consumption.output('../media/images/charts/energy/energy_consumption_transportation_2008_SMALL.svg')

industrial_energy_consumption = Pie(120, 120, [[('Petroleum', 8586), 
                                                ('Coal', 1840),
                                                ('Natural Gas', 8149),  
                                                ('', 0),
                                                ('Renewable', 2056)]], 'piechart_no_label.css', padding=3)
industrial_energy_consumption.output('../media/images/charts/energy/energy_consumption_industrial_2008_SMALL.svg')

residential_commerical_energy_consumption = Pie(120, 120, [[('Petroleum', 1756), 
                                                            ('Coal', 74),
                                                            ('Natural Gas', 8198),  
                                                            ('', 0),
                                                            ('Renewable', 722)]], 'piechart_no_label.css', padding=3)
residential_commerical_energy_consumption.output('../media/images/charts/energy/energy_residential_and_commercial_industrial_2008_SMALL.svg')

electric_energy_consumption = Pie(120, 120, [[('Petroleum', 463), 
                                              ('Coal', 20547),
                                              ('Natural Gas', 6823),  
                                              ('Nuclear', 8455),
                                              ('Renewable', 3690),  
                                              ('Imports', 112)]], 'piechart_no_label.css', padding=3)
electric_energy_consumption.output('../media/images/charts/energy/energy_consumption_electric_2008_SMALL.svg')

#example tax expenditure chart with future years plotted
#For series that have dashed and solid lines, break them into two series with one overlapping data point. Make sure both series have the same styles in the stylesheet. To Designate a series as "dashed" pass the indices of the series in after the named arguments (series numbers are 1-indexed). So below I am passing in 2 and 4 as the series to add the dashed style to. This unfortunately can't be done in the stylesheet and so I have to manually check for it in the script.

te_example = Line(515, 300, [[(2009, 3130), (2010, 4270), (2011, 3300)],
                             [(2011, 3300), (2012, 3140), (2013, 2980)],
                             [(2009, 480), (2010, 1870), (2011, 9600)],   
                             [(2011, 9600), (2012, 11750), (2013, 7250)
                 ]], 'linechart_test.css', 2, 4, units='', currency=False, x_padding=35) 
te_example.output('tax_expend_example.svg')
