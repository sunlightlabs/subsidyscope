from charty.charty import *

top_housing_TE = Column(600, 350, [[("Deductibility of\n mortgage interest \non owner-occupied\n homes", 79400000000), ("Deductibility of \nState and local\n property tax on \nowner-occupied \nhomes", 29010000000), ("Exclusion of\n net imputed\n rental income on \nowner-occupied \nhomes", 27040000000), ("Capital gains\n exclusion on\n home sales", 24000000000), ("Credit for\n home buyer",10000000000 ) ]], "barchart_housing.css", x_label_padding=20, x_padding=5, padding=20, x_label_height=80, units=False, currency=True)
top_housing_TE.output("../../media/images/charts/housing/top_housing_TE.svg")

grants = Column(500, 250, [[('Programs Containing Subsidy', 58781363031), ('Subsidy', 'Subsidy Cost Unknown')]], "barchart_grants.css", units=True, currency=True, use_zero_minimum=True )
grants.output("../../media/images/charts/housing/grants.svg")

contracts = Line(500, 250, [[(2000, 381234796), (2001, 73589876), (2002, 153773357), (2003, 378937334), (2004, 243981896), (2005, 782114440), (2006, 576079508), (2007, 373125797), (2008, 374693948), (2009, 287651498)]], "../linechart.css", use_zero_minimum=True, x_padding=20, label_intervals=2)
contracts.output("../../media/images/charts/housing/contracts.svg")


tax_expend = Column(500, 250, [[('Programs Containing Subsidy', 185230000000), ('Subsidy', 185230000000)]], "barchart_te.css", units=True, currency=True, use_zero_minimum=True )
tax_expend.output("../../media/images/charts/housing/tax_expenditures.svg")
