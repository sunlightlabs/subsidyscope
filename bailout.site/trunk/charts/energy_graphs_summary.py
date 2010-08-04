
from charty import *

#DE = Column(440, 220, 
#            [
#                [ ('scale', 31200000000),
#		  ('Direct Expenditures', 13500000000),
#                  ('Direct Expenditures\n (subsidy)', 'Subsidy Spending Unknown'),
#                ]
#            ],
#            'barchart.css',
#            currency="$",
#            units=True,
#            padding=10,
#            x_label_height=30
#            )
#
#DE.output('summary_DE.svg')
#
#TE = Column(440, 220, 
#            [
#                [ 
#		  ('scale', 31200000000),
#		  ('Tax Expenditures', 5300000000),
#                  ('Tax Expenditures\n(subsidy)', 5300000000),
#                ]
#            ],
#            'barchart_TE.css',
#            currency="$",
#            units=True,
#            x_label_height=30,
#            padding=10
#            )
#
#TE.output('summary_TE.svg')
#
#RT = Column(440, 220, 
#            [
#                [ ('scale', 31200000000),
#		  ('Risk Transfers \n(outstanding credit)', 31200000000),
#                  ('Risk Transfers \n(subsidy)', 'Subsidy Spending Unknown'),
#                ]
#            ],
#            'barchart_RT.css',
#            currency="$",
#            units=True,
#            padding=10,
#            x_label_height=30,
#            )
#
#RT.output('summary_RT.svg')

CO = Line(440, 130,
         [
            [ (2000, 7677302177),
              (2001, 1768682830),
              (2002, 2332004092),
              (2003, 2518815327),
              (2004, 3526604913),
              (2005, 4348697450),
              (2006, 7184534121),
              (2007, 3042779663),
              (2008, 5026602271),
              (2009, 4261998770)
            ]
         ],
            'linechart.css',
            currency="$",
            units=True,
            padding=10,
            x_padding=40,
            label_intervals=2
            )
CO.output('summary_CON.svg')
