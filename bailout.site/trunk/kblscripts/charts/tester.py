
from charts import *

g = Column(300, 400, [[('aaaaaaaaaa',500), ('bbbbbbbbbb',800)], [('aaaaaaaaaa',230), ('bbbbbbbbbb',260), ('cccc', 300)]], 'Column', "barchart.css")

g.output("bar.svg")

h = Line(300, 400, [[(2000, 10), (2001, 30), (2002, 40), (2003, 50)], [(2000, 30),  (2002, 40), (2003, 50)]], 'Line', 'linechart.css', label_intervals=2)
h.output("line.svg")
