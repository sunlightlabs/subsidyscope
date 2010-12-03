from charty.charty import Line, Column, StackedColumn, Pie 

#top_housing_TE = Column(650, 350, [[("Deductibility of\n mortgage interest \non owner-occupied\n homes", 61450000000), ("Deductibility of \nState and local\n property tax on \nowner-occupied \nhomes", 19930000000), ("Capital gains\n exclusion on\n home sales", 29730000000), ("Exclusion of\n net imputed\n rental income on \nowner-occupied \nhomes", 24590000000), ("Credit for\n home buyer", 9730000000) ]], "barchart_housing.css", x_label_padding=20, x_padding=5, x_label_height=60, units=True, currency=True)
#top_housing_TE.output("../../media/images/charts/housing/top_housing_TE.svg")
#
#
energy_grants = Line(500, 350, [[ (2000, 43514975367), 
                                  (2001, 38522803953), 
                                  (2002, 10909951502), 
                                  (2003, 13702360419), 
                                  (2004, 16555616735), 
                                  (2005, 16610663068), 
                                  (2006, 45454010190),
                                  (2007, 0),
                                  (2008, 38434322404), 
                                  (2009, 58781363031)]], '../linechart.css', currency=True, x_padding=35, padding=40, units="", use_zero_minimum=True, label_intervals=2, label_offset=1)
energy_grants.output('../../media/images/charts/housing/housing_direct_expenditures_billions.svg')



energy_contracts = Line(500, 350, [[ (2000, 381234796), 
                                  (2001, 73589876), 
                                  (2002, 153773357), 
                                  (2003, 378937334), 
                                  (2004, 243981896), 
                                  (2005, 782114440), 
                                  (2006, 576079508),
                                  (2007, 373125797), 
                                  (2008, 374693948), 
                                  (2009, 287651498)]], '../linechart.css', currency=True, x_padding=35, padding=40, units="", label_intervals=2)
energy_contracts.output('../../media/images/charts/housing/housing_contracts.svg')

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



top_housing_TE = Column(600, 350, [[("Deductibility of\n mortgage interest \non owner-occupied\n homes", 79400000000), ("Deductibility of \nState and local\n property tax on \nowner-occupied \nhomes", 29010000000), ("Exclusion of\n net imputed\n rental income on \nowner-occupied \nhomes", 27040000000), ("Capital gains\n exclusion on\n home sales", 24000000000), ("Credit for\n homebuyer",10000000000 ) ]], "barchart_housing.css", x_label_padding=20, x_padding=5, padding=20, x_label_height=80, units=False, currency=True, max_x_point_width=70)
top_housing_TE.output("../../media/images/charts/housing/top_housing_TE.svg")

grants = Column(500, 250, [[('Programs Containing Subsidy', 58781363031), ('Subsidy', 'Subsidy Cost Unknown')]], "barchart_grants.css", units=True, currency=True, use_zero_minimum=True )
grants.output("../../media/images/charts/housing/grants.svg")

contracts = Line(500, 250, [[(2000, 381234796), (2001, 73589876), (2002, 153773357), (2003, 378937334), (2004, 243981896), (2005, 782114440), (2006, 576079508), (2007, 373125797), (2008, 374693948), (2009, 287651498)]], "../linechart.css", currency=True, use_zero_minimum=True, x_padding=20, label_intervals=2, label_offset=1)
contracts.output("../../media/images/charts/housing/contracts.svg")


tax_expend = Column(500, 250, [[('Programs Containing Subsidy', 185230000000), ('Subsidy', 185230000000)]], "barchart_te.css", units=True, currency=True, use_zero_minimum=True )
tax_expend.output("../../media/images/charts/housing/tax_expenditures.svg")

housing_activities = StackedColumn(500, 300, [[('Grant Expenditures', 386603767), ('Tax Expenditures', 170740000000)], [('Grant Expenditures', 43130045891), ('Tax Expenditures', 14490000000)], [('Grant Expenditures', 15542205373), ('Tax Expenditures', 0)]], "../stacked_barchart.css", units=True, currency=True, use_zero_minimum=True, x_padding=30, padding=5)
housing_activities.output("../../media/images/charts/housing/activities_supported_by_housing_spending.svg")
