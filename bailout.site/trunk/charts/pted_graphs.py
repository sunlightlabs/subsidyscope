from charty import Column, Line, Pie

treasury_jct_comparison = Column(400, 300, [[('Housing', 185),
                    ('Energy', 5),
                    ('Transportation', 4)],
				    [('Housing', 154),
                    ('Energy', 13), 
                    ('Transportation', 5)]], "barchart.css", x_label_padding=15, x_label_height=50,  x_padding=10)

treasury_jct_comparison.max_x_point_width = 10
treasury_jct_comparison.output("../media/images/charts/pted/treasury_jct_comparison.svg")

                                   


#energy_grants = Line(300, 200, [[(1982, 515.8),
#								(1983, 556.3),
#								(1984, 589.8),
#								(1985, 633.3),
#								(1986, 689.2),
#								(1987, 642.4),
#								(1988, 498.5),
#								(1989, 527.9),
#								(1990, 534.4),
#								(1991, 525.2),
#								(1992, 542.6),
#								(1993, 550.3),
#								(1994, 578.8),
#								(1995, 599.4),
#								(1996, 602.5),
#								(1997, 628.6),
#								(1998, 710.9),
#								(1999, 764.7),
#								(2000, 800.1),
#								(2001, 867.6),
#								(2002, 901.0),
#								(2003, 863.4),
#								(2004, 831.2),
#								(2005, 857.4),
#								(2006, 905.0),
#								(2007, 876.8),
#								(2008, 891.1),
#								(2009, 980.8)],
#								[(1982, 652.2),
#								(1983, 677.1),
#								(1984, 701.2),
#								(1985, 744.3),
#								(1986, 767.2),
#								(1987, 757.0),
#								(1988, 766.9),
#								(1989, 777.0),
#								(1990, 767.5),
#								(1991, 787.8),
#								(1992, 768.5),
#								(1993, 759.8),
#								(1994, 746.8),
#								(1995, 736.0),
#								(1996, 705.9),
#								(1997, 712.0),
#								(1998, 709.4),
#								(1999, 725.4),
#								(2000, 764.5),
#								(2001, 788.8),
#								(2002, 877.6),
#								(2003, 966.3),
#								(2004, 1022.2),
#								(2005, 1070.6),
#								(2006, 1086.7),
#								(2007, 1081.1),
#								(2008, 1151.9),
#								(2009, 1237.7)]], 'linechart.css', label_intervals=5, currency=False, x_padding=10, padding=10, units="", use_zero_minimum=True)
#energy_grants.output('../media/images/charts/pted/historical_tes_vs_outlays.svg')


#energy_transportation_housing_as_percent_of_total = Pie(300, 300, [[('All Other Tax Expenditures', 786673), 
#                                             ('Energy', 5220), 
#                                             ('Housing', 185210), 
#                                             ('Transportation', 3690)]], 'piechart.css', y_padding=10, x_padding=10)
#energy_transportation_housing_as_percent_of_total.output("../media/images/charts/pted/energy_transportation_housing_as_percent_of_total.svg")



