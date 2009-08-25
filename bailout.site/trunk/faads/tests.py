import unittest

from faads.search import *
from faads.views import construct_form_and_query_from_querydict

class FAADSSearchTestCase(unittest.TestCase):

        
    sector_name = 'Transportation'
    
    basic_querydict = 'eJxtlUGPnDgQhe/%2BIzOXRBTY2D5mk0uO2ZX6ihggDqtuqDRuaebf76vHRFrt5tJ%2BUEV99iuonqZd34b7Uhx%2Bpn076v0x1f3utHHP0/z3uJX9449a1X17LPe3L%2BtUnYqbhuHlsV7rug2Dm3mzdc%2Bzdu6yv1zXMtZ134bxtj%2B2OtzWbb09bk69e75qcBenvRuPf2fOY12Go453FIqWlVxhTl1e6/DT0EN908Vptqg07tJiH2Ip48QSZ1haxrGPT7jwbrz8gTVg/YyVJcfjWIHapuXXMyRKcpcOFxm5HsdpsAasYFx6rC3WiLXDmrB6bm8sx7C8TtfHjP2bgfN4f0M0WMm2hx0brqLlTt/ncdD7Xu7jDbnX5dz3bak/9hlJiY9kZ0Wdds3vLFo2ZHZimV37btH/S77fOZDaMdW7S2oaXJoRqRGongomdpEKR%2B8SlJzhzJvwwTdUcMILFbzwLRXc8HSjgR/eU2UoQtAi9YSgS%2BoJQXPUJyrgPBnokQYy0CUNZKBPGshAazSQgfZoIAMd0kAGeqSBDHRJAxnokwYy0CkNZKBX2pOBvmhPBnqjPRnojvZkoAXak4E2aE8G%2BqA9GbBdezJgvfZkwF/tyYDHGsmAyRrJgMkayYDJGsmAyRrJgMcayYDHGsmAxxrJgMcayYDHGsmAx5rIgMeayIDHmsiAx5rIgMeayIDHmsiAx5rIgMeayIDHmsiAx5rIgMeayYDHmsmAx5rJgMeayYDHmsmAx5rJgMeayYDHmsmAx5rJgMeayYDH%2BIQJgcmQpMBlSGJgMyQ58BmSINgLSVK0r78hKtpH25AVWZewyLqkRasrpEWrK6RFqytGyw0TjCb9edufOpsO1MnYNj9Mi2kjShQ%2Bm07N6vnUVoczBNrqcI5ItFdWOEugmUNutJdLWn9qO0ZLbvR8ltwYqDlLMKtXXRcM119jj9NDbHwYoSPZhGHNrK4955p03TnYpPPnZBNOBWE2QUy343GznAoto3Y0%2B76EQ8G%2BL%2BFQsK9KbCgcv5v%2B4%2Bs5/cVzGAne4v/OdguGM9ifwQoZ3Z/4Tfa/IvDhryeMv2mf16082UxvcOdRv39IvBJ3IAFDcuQl/40Er3UBLbijRFcSluwKXoWj4JAFLYdAQCyCQxQYDYH/Hvh4FHhXYBsEysAtewoxYdBOU%2BwsJoNJPGtbuD3q%2BHJduAvvvuI1P14%2B/gPv9uuE'
    
    tag_querydict = 'eJxtlU2PmzAQhu/%2BI7uXrjA2tjn249JjWylXxAL1UiUwDY60%2B%2B/7zutUqtpe4gHb8%2BB5YDJNu7wN1yUb/Ez7dpTrbSr71UhjHqf5x7jl/emlFDFfbsv17dM6FSPWTMPwfFvPZd2Gwcy82ZrHWZw57c/nNY9l3bdhvOy3rQyXdVsvt4sRbx7P0pmTkWDG48%2BV81iW4SjjFYmirkomc01ZXsvwU9FDeZPFSK%2BztjGnFs9hdck4MUWdti3n8RzvceHNePqAscP4ESNTynXP1/EyHMt5uW8d84FZgm0ypx4XPbY4nKrBGDECdbIatGQex4rH3ablzm2dbm694SbleYzgnTqMEWPAmO7JNHky4hoeEfRheZ3Otxk1UAnzeH3DrNWUrkVJN1w5XTt9n8fh3wNclvKyz1jECjuUGElx%2Bd8yL5uu5GHd7zL/m/J%2BB3VxLLlHyVPTQKJWIjUWUcsIIrxjhKN7Lbmt0x1vog4%2BMEIlfGSEWvjECNXwrEaDenQNI5S/IwSapSMEpqUjBIKl84yA68iAZ%2BnIgGnpyIBr6chQax0ZcCuBDOiVQAYESyADiiWQAccSyIBWCWRArQQyYFcCGfArgQwYlkAGHEskA5YlkgHPEsmAU4lkwKtEMmBWIhnQJ5EMKJRIBhxKJAPKJJIBbZLIgBtJZMCPJDIgSBIZECSJDAiSRAYESSIDfiSRAT%2BSyIAfSWTAj/RkwI/0ZMCP9GTAj/RkwI/0ZMCP9GTAj/RkwI/0ZMCP9GTAj/RkwA8%2BZUI6/eYaUmAIITFQhJCcoN97QxAkISQJlhASBU0IyYInhIRBFELSgtIsaVERlrTIPkJa1LyWtKh52T5S1LzsIClqXkta1LyWtMi8SusbLlCaDbzN9oFYT1dbSEjK1i6isZ6vdWwt%2BsLa1tdYs7OLIGaeUGPmiYxb5kk15hpyo75i1jU11mO42rpUo3XkRla7dhR0/VXWBW363kBrD7HaRJTgSNZAsVosl2p3s66v7c36pvY3y96g36plb9Bv1bI38GHZG1rO6tFazmp6/cosW0PLdOmvtvX7f2R8rf8j1td/AbyPf/9LaLO3dbKtkwWhM1/x6/UfyuKV/PaAJjjt87rlB90QcOdWvr9LvIrmwAK0ypGXqe7qTfYmd%2BbI0eSEATfwMh0Zh8x4aRBgwuoMjpMh8siofEbFEWCr070oYna6xmk%2Bbtc5y0k9VtZDIcQhsh7h0Ge53Mr4fF70cfBxfMYXczw//QIXPQLS'
   
    text_querydict = 'eJxtlUGPpDYQhe/%2BIzuXrCiwsX3c7F5yTCL1FXmAZYm6oQJuaebf59VjV4qSlUbjBy7XZ78y1eO46/twzIvDv3Hfzno8x7ofThv3Mk5/lW3ZP36rVd3vz/l4/7KO1am4cRhen%2Bu9rtswuIkvW/cyaedu%2B%2Bt9XUpd920oj/251eGxbuvj%2BXDq3ctdg7s57V05/x05lToPZy0HEkWLSm5hTJ3f6vC3oYf6rrPTbLPSuFuLfYiFlJEprmlpOY99fMKDd%2BX2K8aA8TNGpiznuQK1jfOPNSRKcrcODxmxHsdpMAaMYNx6jC3GiLHDmDB6bq8s5zC/jffnhP2bgVM53jEbLGXbw44NT9Fix69TGfTYl6M8EHufr30/5vptnxCUuCQ7S%2Bq0a35m0bwhshOL7NrvFv0/5fc3J0I7hnp3S02DRzMiNQLVU8HELlLh6F2Ckms68yV88A0VnPBCBS98SwU3PN1o4If3VBmKEJRIPSGoknpCUBz1iQo4TwZqpIEMVEkDGaiTBjJQGg1koDwayECFNJCBGmkgA1XSQAbqpIEMVEoDGaiV9mSgLtqTgdpoTwaqoz0ZKIH2ZKAM2pOBOmhPBmzXngxYrz0Z8Fd7MuCxRjJgskYyYLJGMmCyRjJgskYy4LFGMuCxRjLgsUYy4LFGMuCxRjLgsSYy4LEmMuCxJjLgsSYy4LEmMuCxJjLgsSYy4LEmMuCxJjLgsSYy4LFmMuCxZjLgsWYy4LFmMuCxZjLgsWYy4LFmMuCxZjLgsWYy4LFmMuAxPmFCYDIkKXAZkhjYDEkOfIYkCPZCkhTt62%2BIivbRNmRF5iUsMi9p0fIKadHyCmnR8orRcsMAo0l/vfaXzqYDdTK29Q/TYtqIEoVr06WZPV/a8rCHQFse9hGJdmWFvQSaMeRGu1zS%2BkvbMVpyo%2BdacmOgZi9Br151ndFcf7Q9dg%2Bx9mGEjmQThjWzuvbqa9J1V2OTzl%2BdTdgVhNEEMdyOx82yK7SctaPZ9yVsCvZ9CZuCfVViTeH8Wfcvb1f3F89mJLjF/%2B3tNhmuSbTMepT1fto7O2vFmNwf%2BJ/tF0Zwkf/8gEY47tO6LR%2BsuwvePOvXXxKfWnciAO2y8LG7VgGKv%2BDOJbolYchuwaU4Fxx3QfEhMCE2g%2BMssBwCv0Jw9Fzg4gIDIToIz1WYE07auRY7lclgEmttC49nLa/3mbsI7jdc%2BPP14z/nkO7h'


    def testConnection(self):
        search = FAADSSearch()
        self.assertEquals(search.get_haystack_queryset().count(), 746666)
        
        
    def testAggregation(self):
        search = FAADSSearch()
        search.aggregate('fiscal_year')
        search.aggregate('recipient_state')
        
        form, faads_search_query = construct_form_and_query_from_querydict(self.sector_name, self.tag_querydict)
        
        faads_search_query.aggregate('fiscal_year')
        faads_search_query.aggregate('recipient_state')
        
        
        form, faads_search_query = construct_form_and_query_from_querydict(self.sector_name, self.basic_querydict)
        
        faads_search_query.aggregate('fiscal_year')
        faads_search_query.aggregate('recipient_state')
        
        form, faads_search_query = construct_form_and_query_from_querydict(self.sector_name, self.text_querydict)
        
        faads_search_query.aggregate('fiscal_year')
        faads_search_query.aggregate('recipient_state')
        
        
        
    def testQueryDict(self):
        
        form, faads_search_query = construct_form_and_query_from_querydict(self.sector_name, self.basic_querydict)
        
        self.assertEquals(faads_search_query.get_haystack_queryset().count(), 746666)
        
        form, faads_search_query = construct_form_and_query_from_querydict(self.sector_name, self.tag_querydict)
        
        self.assertEquals(faads_search_query.get_haystack_queryset().count(), 2561)
        
        form, faads_search_query = construct_form_and_query_from_querydict(self.sector_name, self.text_querydict)
        
        self.assertEquals(faads_search_query.get_haystack_queryset().count(), 11916)
        
        
        

        
