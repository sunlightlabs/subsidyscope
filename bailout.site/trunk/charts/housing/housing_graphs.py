from charty import * 

#top_housing_TE = Column(650, 350, [[("Deductibility of\n mortgage interest \non owner-occupied\n homes", 61450000000), ("Deductibility of \nState and local\n property tax on \nowner-occupied \nhomes", 19930000000), ("Capital gains\n exclusion on\n home sales", 29730000000), ("Exclusion of\n net imputed\n rental income on \nowner-occupied \nhomes", 24590000000), ("Credit for\n home buyer", 9730000000) ]], "barchart_housing.css", x_label_padding=20, x_padding=5, x_label_height=60, units=True, currency=True)
#top_housing_TE.output("../../media/images/charts/housing/top_housing_TE.svg")
#
#
#energy_grants = Line(500, 350, [[ (2000, 43514975367), 
#                                  (2001, 38522803953), 
#                                  (2002, 10909951502), 
#                                  (2003, 13702360419), 
#                                  (2004, 16555616735), 
#                                  (2005, 16610663068), 
#                                  (2006, 45454010190)], 
#                                  [(2008, 38434322404), 
#                                  (2009, 58781363031)]], '../linechart.css', currency=False, x_padding=35, padding=40, units="")
#energy_grants.output('../../media/images/charts/housing/housing_direct_expenditures_billions.svg')
#
#
#
#energy_contracts = Line(500, 350, [[ (2000, 381234796), 
#                                  (2001, 73589876), 
#                                  (2002, 153773357), 
#                                  (2003, 378937334), 
#                                  (2004, 243981896), 
#                                  (2005, 782114440), 
#                                  (2006, 576079508),
#                                  (2007, 373125797), 
#                                  (2008, 374693948), 
#                                  (2009, 287651498)]], '../linechart.css', currency=False, x_padding=35, padding=40, units="")
#energy_contracts.output('../../media/images/charts/housing/housing_contracts.svg')

#struct1 = Pie(300, 300, [[('',  76.4), 
#                                 ('',  35.4), 
#                                 ('',  13.7), 
#                                 ('',  4.6)]], '../piechart.css')  # ('Imports', 112)
#struct1.output('../../media/images/charts/housing/structure_figure1.svg')

test = Column(500, 340, [[('testA', 1640), 
                    ('testB', 1050),
                    ('testC', 770)],
                    [('testA', 1050), 
                    ('testB', 123),
                    ('testC', 770)],
                    [('testA', 1050), 
                    ('testB', 123),
                    ('testC', 770)]], "../barchart.css", label_rotate=-35, x_label_padding=10, x_label_height=100)
test.output("../../media/images/charts/housing/test.svg")



