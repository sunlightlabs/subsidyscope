from charts import *

#primary_energy = Column(480, 340, [[('Coal', 23.9), 
#				    ('Natural Gas', 21.2), 
#				    ('Crude Oil', 10.5), 
#				    ('Nuclear Electric Power', 8.5), 
#				    ('Biomass', 3.9), 
#				    ('Hydroelectric Power', 2.5), 
#				    ('Natural Gas Plant Liquids', 2.4), 
#				    ('Wind, Geothermal, Solar P/V', 1.0)]], "barchart.css", label_rotate=-35, x_label_padding=10, x_label_height=100)
#primary_energy.output("../media/images/charts/energy/US_primary_energy_production_by_major_source_2008.svg")



top_five_tes = Column(500, 340, [[('Expensing of exploration and development, fuels', 1640), 
				    ('Payments for specified energy property in lieu of tax credits*', 1050),
                    ('Temporary 50% expensing for liquid fuel refining equipment', 770), 
				    ('Credit for energy efficiency improvements', 570), 
				    ('New technology credit', 430), 
				    ('Excess of percentage over cost depletion, fuels', 340)]], "barchart.css", label_rotate=-35, x_label_padding=10, x_label_height=100)
top_five_tes.output("../media/images/charts/energy/top_five_tes.svg")

#primary_energy_consumption = Pie(475, 310, [[('Petroleum', 37), 
#					     ('Non-Fossil', 17), 
#					     ('Coal', 22), 
#					     ('Natural Gas', 24)]], 'piechart_orange.css', y_padding=30, x_padding=120, padding=0)
#primary_energy_consumption.output("../media/images/charts/energy/US_primary_energy_consumption_by_major_fuel_type_2008.svg")
##
#energy_related_CO2 = Pie(475, 310, [[('Petroleum', 42), 
#                                     ('Coal', 37),  
#                                     ('Natural Gas', 21)]], 'piechart.css', y_padding=30, x_padding=100, padding=0)
#energy_related_CO2.output("../media/images/charts/energy/US_energy_related_CO2_emissions_by_major_fuel_type_2009.svg")
##
#
electric_power = Pie(650, 400, [[('Petroleum', 463), 
                                 ('Coal', 20547), 
                                 ('Natural Gas', 6823), 
                                 ('Renewables', 3690), 
                                 ('Nuclear', 8455)]], 'piechart.css', y_padding=5, x_padding=120)  # ('Imports', 112)
electric_power.output('../media/images/charts/energy/US_electric_power_industry_net_generation_2008.svg')


depletion_allowance = Line(500, 350, [[(1998, 250),
									    (1999, 265),
									    (2000, 340),  
                                        (2001, 250), 
                                        (2002, 610), 
                                        (2003, 640), 
                                        (2004, 1320), 
                                        (2005, 590), 
                                        (2006, 760), 
                                        (2007, 790), 
                                        (2008, 920), 
                                        (2009, 340),
                                        (2010, 610),
                                        (2011, 670),
                                        (2012, 940),
                                        (2013, 1130),
                                        (2014, 1160),
                                        (2015, 1190)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")

depletion_allowance.output('../media/images/charts/energy/depletion_allowance.svg')
																	

energy_te_history = Line(500, 350, [    [(1998, 135),
									    (1999, 165),
									    (2000, 130),  
                                        (2001, 150), 
                                        (2002, 210), 
                                        (2003, 370), 
                                        (2004, 430), 
                                        (2005, 810), 
                                        (2006, 1170), 
                                        (2007, 1050), 
                                        (2008, 900), 
                                        (2009, 430),
                                        (2010, 740),
                                        (2011, 790),
                                        (2012, 1000),
                                        (2013, 1070),
                                        (2014, 1060),
                                        (2015, 1060)],
                                        																	
																	
                                        																	
                                        [(1998, 15),
									    (1999, 15),
									    (2000, 20),  
                                        (2001, 30), 
                                        (2002, 30), 
                                        (2003, 30), 
                                        (2004, 30), 
                                        (2005, 190), 
                                        (2006, 150), 
                                        (2007, 320), 
                                        (2008, 180), 
                                        (2009, 1470),
                                        (2010, 4910),
                                        (2011, 14040),
                                        (2012, 15980),
                                        (2013, 9610),
                                        (2014, 4350),
                                        (2015, 2650)],
                                        
                                        
																	

                                        [(1998, 155),
									    (1999, 170),
									    (2000, 150),  
                                        (2001, 120), 
                                        (2002, 150), 
                                        (2003, 150), 
                                        (2004, 170), 
                                        (2005, 150), 
                                        (2006, 670), 
                                        (2007, 1060), 
                                        (2008, 860), 
                                        (2009, 1170),
                                        (2010, 2750),
                                        (2011, 2230),
                                        (2012, 620),
                                        (2013, 720),
                                        (2014, 740),
                                        (2015, 830)],
                                        
                                        
																	
                                      																
                                        [(1998, 1230),
									    (1999, 1530),
									    (2000, 1730),  
                                        (2001, 1636), 
                                        (2002, 2760), 
                                        (2003, 2650), 
                                        (2004, 3040), 
                                        (2005, 3770), 
                                        (2006, 4650), 
                                        (2007, 4630), 
                                        (2008, 3780), 
                                        (2009, 3200),
                                        (2010, 4470),
                                        (2011, 3720),
                                        (2012, 3610),
                                        (2013, 3470),
                                        (2014, 2220),
                                        (2015, 1280)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")

energy_te_history.output('../media/images/charts/energy/energy_te_history.svg')


#energy_tax_expenditures = Pie(650, 400, [[('Coal and refined Coal', 2660), 
#                                          ('Nuclear', 199), 
#                                          ('Natural Gas and \nPetroleum Liquids', 2090), 
#                                          ('Renewables', 670), 
#                                          ('Electricity (not fuel specific)', 735), 
#                                          ('End Use', 120), 
#                                          ('Conservation', 670)]], 'piechart.css', y_padding=30, x_padding=145)
#energy_tax_expenditures.output('../media/images/charts/energy/energy_tax_expenditures_by_fuel_type_2007.svg')
#
#energy_nc_contracts = Line(500, 350, [[ (2000, 7677302177.38), 
#                                        (2001, 1768682830.59), 
#                                        (2002,  2332004092.37), 
#                                        (2003, 2518815327.42), 
#                                        (2004, 3526604913.88), 
#                                        (2005, 4348697450.95), 
#                                        (2006, 7184534121.06), 
#                                        (2007, 3042779663.11), 
#                                        (2008, 5026602271.39), 
#                                        (2009, 4261998770.56)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")
#energy_nc_contracts.output('../media/images/charts/energy/energy_noncompeted_contracts_billions.svg')
#

                                   


energy_grants = Line(500, 350, [[ (2000, 3214212807), 
                                  (2001, 3292482671), 
                                  (2002, 5344934793), 
                                  (2003, 4696662114), 
                                  (2004, 4015094677), 
                                  (2005, 4273538731), 
                                  (2006, 5145921114), 
                                  (2007, 4326775524), 
                                  (2008, 4629731149), 
                                  (2009, 18603682169)]], 'linechart.css', label_intervals=2, currency=False, x_padding=35, padding=40, units="")
energy_grants.output('../media/images/charts/energy/energy_direct_expenditures_billions.svg')
#
##energy consumption, group of 5 pie charts, 1 large 4 small
#
primary_energy_consumption = Pie(600, 450, [[('Petroleum', 37), 
                                             ('Coal', 23), 
                                             ('Natural Gas', 24), 
                                             ('Nuclear', 9), 
                                             ('Renewable', 7)]], 'piechart.css', y_padding=5, x_padding=60)
primary_energy_consumption.output("../media/images/charts/energy/US_primary_energy_consumption_by_source_and_sector_2008.svg")

#little charts
transportation_energy_consumption = Pie(120, 120, [[('', 26332), # Petroleum
                                                    (' ', 0), #dummy so colors are consistent
                                                    ('', 677),  # Natural Gas
                                                    (' ', 0), #dummy
                                                    ('', 833)] #Renewable
                                                            ], 'piechart.css', padding=3)
transportation_energy_consumption.output('../media/images/charts/energy/energy_consumption_transportation_2008_SMALL.svg')

industrial_energy_consumption = Pie(120, 120, [[('', 8586),  # Petroleum 
                                                ('', 1840),  # Coal
                                                ('', 8149),  # Natural Gas
                                                (' ', 0),    #dummy
                                                ('', 2056)]  # Renewable
                                                            ], 'piechart.css', padding=3)
industrial_energy_consumption.output('../media/images/charts/energy/energy_consumption_industrial_2008_SMALL.svg')

residential_commerical_energy_consumption = Pie(120, 120, [[('', 1756), # Petroleum
                                                            ('', 74),   # Coal
                                                            ('', 8198), # Natural Gas
                                                            (' ', 0),   #dummy
                                                            ('', 722)]  # Renewable
                                                                ], 'piechart.css', padding=3)
residential_commerical_energy_consumption.output('../media/images/charts/energy/energy_residential_and_commercial_industrial_2008_SMALL.svg')

electric_energy_consumption = Pie(120, 120, [[('', 463),   # Petroleum
                                              ('', 20547), # Coal
                                              ('', 6823),  # Natural Gas
                                              ('', 8455),  # Nuclear
                                              ('', 3690)  # Renewable
                                                ]], 'piechart.css', padding=3)
electric_energy_consumption.output('../media/images/charts/energy/energy_consumption_electric_2008_SMALL.svg')

#example tax expenditure chart with future years plotted
#For series that have dashed and solid lines, break them into two series with one overlapping data point. Make sure both series have the same styles in the stylesheet. To Designate a series as "dashed" pass the indices of the series in after the named arguments (series numbers are 1-indexed). So below I am passing in 2 and 4 as the series to add the dashed style to. This unfortunately can't be done in the stylesheet and so I have to manually check for it in the script.

te_example = Line(515, 300, [[(2009, 3130), (2010, 4270), (2011, 3300)],
                             [(2011, 3300), (2012, 3140), (2013, 2980)],
                             [(2009, 480), (2010, 1870), (2011, 9600)],   
                             [(2011, 9600), (2012, 11750), (2013, 7250)
                 ]], 'linechart_test.css', 2, 4, units='', currency=False, x_padding=35) 
te_example.output('tax_expend_example.svg')


