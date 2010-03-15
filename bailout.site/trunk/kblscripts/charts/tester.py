
from charts import *

g = Column(300, 400, [[('aaaaaaaaaa',500), ('bbbbbbbbbb',800)], [('aaaaaaaaaa',230), ('bbbbbbbbbb',260), ('cccc', 300)]], 'Column', "barchart.css")

g.output("bar.svg")

h = Line(300, 400, [[(1,2000), (3,2001), (4,2002), (5, 2003)], [(3, 2000),  (5, 2002), (3, 2003)]], 'Line', 'linechart.css', label_intervals=2)
h.output("line.svg")
