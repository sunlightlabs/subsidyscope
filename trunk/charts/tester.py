
from charts import *

g = Column(600, 300, [[('aaaaaaaaaa', 'Subsidy Spending Unknown'), ('bbbbbbbbbb',800)], [('aaaaaaaaaa',230), ('bbbbbbbbbb',260), ('cccc', 300)]], "barchart.css", label_rotate=-45, y_padding=30)

g.output("bar.svg")

h = Line(400, 300, [[(2000, 10), (2001, 30), (2002, 40), (2003, 50)], [(1990, 30),  (1992, 40), (2004, 50)]], 'linechart.css', label_intervals=2, x_padding=15)
h.output("line.svg")

h = Pie(400, 400, [[(2000, 1230), (2001, 3230), (2002, 4000), (2003, 1250), (2004, 1000), (2005, 1200), (2006, 800), (2007, 100), (22, 2332), (30, 3234)]], 'piechart_orange.css', y_padding=70, x_padding=70)
h.output("pie.svg")


#risk transfers
risk_transfers = Column(370, 185, [[('Outstanding Credit', 7445983679), ('Subsidy', 114141251)]], "barchart.css", padding=10, currency=True)
risk_transfers.output("risk_transfers.svg")

#contracts

contracts = Line(515, 230, [[(2000, 12972951342), (2001, 14109441817), (2002, 15780150198), (2003, 20911608531), (2004, 21064466760), (2005, 15275901189)], [(2005, 15275901189), (2006, 15939230914), (2007, 19124684255), (2008, 18239197959), (2009, 16226290107)]], 'linechart_test.css', 2, label_intervals=3, units='', currency=False, x_padding=35)
#in the above example, the '2' is part of the *args array designating the series numbers that shouls be dashed. The stroke-dasharray property doesn't work in the stylesheet for some reason.
contracts.output("contracts.svg")
