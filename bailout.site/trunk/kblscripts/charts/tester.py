
from charts import *

g = Column(300, 400, [[('aaaaaaaaaa',500), ('bbbbbbbbbb',800)], [('aaaaaaaaaa',230), ('bbbbbbbbbb',260), ('cccc', 300)]], 'Column', "barchart.css")

g.output("bar.svg")

h = Line(300, 400, [[(2000, 10), (2001, 30), (2002, 40), (2003, 50)], [(2000, 30),  (2002, 40), (2003, 50)]], 'Line', 'linechart.css', label_intervals=2)
h.output("line.svg")

h = PieChart(400, 400, [[(2000, 10), (2001, 30), (2002, 40), (2003, 50)]], 'Pie', 'piechart.css')
h.output("pie.svg")


#risk transfers
risk_transfers = Column(185, 220, [[('Outstanding Credit', 7445983679), ('Subsidy', 114141251)]], 'Column', "barchart.css", padding=10)
risk_transfers.output("risk_transfers.svg")

#contracts

contracts = Line(230, 315, [[(2000, 12972951342), (2001, 14109441817), (2002, 15780150198), (2003, 20911608531), (2004, 21064466760), (2005, 15275901189), (2006, 15939230914), (2007, 19124684255), (2008, 18239197959), (2009, 16226290107)]], 'Line', 'linechart.css', label_intervals=2, units='', currency=False)
contracts.output("contracts.svg")
