from fpds.search import *
from geo.models import State
from django.test import TestCase



class search(TestCase):
    
    def __init__(self):
        super(search, self).__init__()

    def mysql_query(self):
        return FPDSSearch().filter('fiscal_year', (1900, None))

    def solr_query(self):
        return FPDSSearch().filter('all_text','*')
    
    def testTextSearch(self):
        """
        Determines if a record matching the string 'southwest' is properly returned
        """
        s = FPDSSearch()
        r = s.filter('all_text', 'SOUTHWEST').get_haystack_queryset()
        found_match = False
        for x in r:
            if int(x.pk)==383921:
                found_match = True

        self.failUnlessEqual(found_match, True)

    def testSampleDataSetAggregationByRecipientState(self):
        """
        runs aggregation by state
        """
      
        r = self.solr_query()

        # only test if we're sure we're using the sample dataset
        if int(r.count())==257:
            
            correct_result = {1: Decimal("107609.0"), 2: Decimal("600.0"), 3: Decimal("0.0"), 4: Decimal("28414.0"), 5: Decimal("49344.0"), 6: Decimal("129761.82"), 7: Decimal("10000.0"), 9: Decimal("224834.52"), 10: Decimal("-3371.88"), 11: Decimal("364982.97"), 14: Decimal("10011.2"), 15: Decimal("76492.5"), 16: Decimal("2672.0"), 17: Decimal("14432.11"), 18: Decimal("-21388.0"), 20: Decimal("2033.0"), 21: Decimal("3599090.81"), 22: Decimal("376812.95"), 23: Decimal("5294.0"), 24: Decimal("246589.44"), 25: Decimal("-34000.0"), 26: Decimal("318658.73"), 27: Decimal("5000.0"), 28: Decimal("4.75"), 29: Decimal("22524.0"), 31: Decimal("7014.0"), 32: Decimal("2663.41"), 33: Decimal("89897.94"), 34: Decimal("-1201.39"), 35: Decimal("227529.0"), 36: Decimal("391226.26"), 37: Decimal("3000.0"), 38: Decimal("0.0"), 39: Decimal("5520.0"), 41: Decimal("-4588.0"), 42: Decimal("115288.36"), 44: Decimal("133011.12"), 47: Decimal("7890842.49"), 48: Decimal("73457.21"), 50: Decimal("9781.05"), 51: Decimal("33083.0")}
            
            s = r.aggregate('recipient_state')  

            for (i, total) in correct_result.items():
                self.failUnlessEqual(s[i], total)


    def testSampleDataSetAggregationByYear(self):
        """
        Determines if a simple aggregation by fiscal year (on all records) works
        """
        
        r = self.solr_query()
        
        # only test if we're sure we're using the sample dataset
        if int(r.count())==257:
            s = FPDSSearch().filter('all_text', '*').aggregate('fiscal_year')        
            self.failUnlessEqual(s[2000], Decimal("7000.00"))
            self.failUnlessEqual(s[2001], Decimal("4761445.00"))
            self.failUnlessEqual(s[2002], Decimal("422417.00"))
            self.failUnlessEqual(s[2003], Decimal("888961.00"))
            self.failUnlessEqual(s[2004], Decimal("627510.80"))
            self.failUnlessEqual(s[2005], Decimal("1898221.43"))
            self.failUnlessEqual(s[2006], Decimal("1637043.34"))
            self.failUnlessEqual(s[2007], Decimal("608433.25"))
            self.failUnlessEqual(s[2008], Decimal("1064551.19"))
            self.failUnlessEqual(s[2009], Decimal("2695343.36"))
            
    def testSampleDataSetAggregationByNAICS(self):
        """
        runs aggregation by NAICS
        """
        r = self.solr_query()

        # only test if we're sure we're using the sample dataset
        if int(r.count())==257:
            
            correct_result = {1: Decimal("1142853.0"), 2: Decimal("6336445.0"), 3: Decimal("113515.0"), 4: Decimal("305979.0"), 5: Decimal("2606414.0"), 6: Decimal("644080.0"), 7: Decimal("73730.0"), 8: Decimal("-300.0"), 9: Decimal("33083.0"), 10: Decimal("244867.0"), 11: Decimal("14831.0"), 12: Decimal("10547.94"), 13: Decimal("-1426.77"), 14: Decimal("1000.0"), 15: Decimal("5160.0"), 16: Decimal("-4588.0"), 17: Decimal("187115.1"), 18: Decimal("0.0"), 19: Decimal("459.6"), 20: Decimal("5000.0"), 21: Decimal("142460.0"), 22: Decimal("6105.0"), 23: Decimal("359235.0"), 24: Decimal("116.0"), 25: Decimal("750.0"), 26: Decimal("3000.0"), 27: Decimal("-21428.0"), 28: Decimal("107609.0"), 29: Decimal("115260.0"), 30: Decimal("22904.0"), 31: Decimal("4440.0"), 32: Decimal("5475.0"), 33: Decimal("3224.09"), 34: Decimal("1794.74"), 35: Decimal("1566.0"), 36: Decimal("4399.2"), 37: Decimal("21400.0"), 38: Decimal("-1000.0"), 39: Decimal("0.0"), 40: Decimal("5112.63"), 41: Decimal("2672.0"), 42: Decimal("600.0"), 43: Decimal("577.95"), 44: Decimal("121053.0"), 45: Decimal("37000.0"), 46: Decimal("7014.0"), 47: Decimal("0.0"), 48: Decimal("7014.0"), 49: Decimal("38422.45"), 50: Decimal("5700.0"), 51: Decimal("225.38"), 52: Decimal("4412.0"), 53: Decimal("20000.0"), 54: Decimal("22383.0"), 55: Decimal("-5280.0"), 56: Decimal("0.0"), 57: Decimal("0.0"), 58: Decimal("3251.6"), 59: Decimal("630.81")}
            
            s = r.aggregate('naics_code')  
            
            for (i, total) in correct_result.items():
                self.failUnlessEqual(s[i], total)
    
    def testMySQLAggregation(self):
        
        print self.mysql_query().aggregate('fiscal_year')
