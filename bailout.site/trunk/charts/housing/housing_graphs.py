from charty.charty import *

top_housing_TE = Column(650, 350, [[("Deductibility of\n mortgage interest \non owner-occupied\n homes", 61450000000), ("Deductibility of \nState and local\n property tax on \nowner-occupied \nhomes", 19930000000), ("Capital gains\n exclusion on\n home sales", 29730000000), ("Exclusion of\n net imputed\n rental income on \nowner-occupied \nhomes", 24590000000), ("Credit for\n home buyer", 9730000000) ]], "barchart_housing.css", x_label_padding=20, x_padding=5, x_label_height=60, units=True, currency=True)
top_housing_TE.output("../../media/images/charts/housing/top_housing_TE.svg")
