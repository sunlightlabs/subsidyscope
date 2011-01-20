from django.db import models

# Create your models here.

class Agency(models.Model):
    
    cfda_code = models.CharField("CFDA Agency code", max_length=2)
    fips_code = models.CharField("FIPS Agency code", max_length=2)
    name = models.CharField("Agency Name", max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Agency'
        ordering = ['name']


class AgencyManager(models.Manager):

    def import_agencies(self):
        Agency.objects.all().delete()
        for k, v in AGENCY_MAP.items():
            a = Agency( cfda_code=k, fips_code=v[0], name=v[1] )
            a.save()


AGENCY_MAP = {'10': ('12', 'Department of Agriculture'), 
              '11': ('13', 'Department of Commerce'), 
              '12': ('97', 'Department of Defense'), 
              '14': ('86', 'Department of Housing and Urban Development'), 
              '15': ('14', 'Department of the Interior'), 
              '16': ('15', 'Department of Justice'), 
              '17': ('16', 'Department of Labor'), 
              '19': ('19', 'U.S. Department of State'), 
              '20': ('69', 'Department of Transportation'), 
              '21': ('20', 'Department of the Treasury'), 
              '23': ('46', 'Appalachian Regional Commission'), 
              '27': ('24', 'Office of Personnel Management'), 
              '29': ('95', 'Commission on Civil Rights'), 
              '30': ('45', 'Equal Employment Opportunity Commission'), 
              '31': ('83', 'Export Import Bank of the United States'), 
              '32': ('27', 'Federal Communications Commission'),
              '33': ('65', 'Federal Maritime Commission'), 
              '34': ('93', 'Federal Mediation and Concillation Service'), 
              '36': ('29', 'Federal Trade Commission'), 
              '39': ('47', 'General Services Administration'), 
              '40': ('04', 'Government Printing Office'), 
              '42': ('03', 'Library of Congress'), 
              '43': ('80', 'National Aeronautics and Space Administration'), 
              '44': ('25', 'National Credit Union Administration'), 
              '45': ('59', 'National Endowment for the Arts'), 
              '46': ('63', 'National Labor Relations Board'), 
              '47': ('49', 'National Science Foundation'), 
              '57': ('60', 'Railroad Retirement Board'), 
              '58': ('50', 'Securities and Exchange Commission'), 
              '59': ('73', 'Small Business Administraton'), 
              '64': ('36', 'Department of Veterans Affairs'), 
              '66': ('68', 'Environmental Protection Agency'), 
              '68': ('33', 'National Gallery of Art'), 
              '70': ('71', 'Overseas Private Investment Corporation'), 
              '77': ('31', 'Nuclear Regulatory Commission'), 
              '78': ('95', 'Commodity Futures Trading Commission'), 
              '81': ('89', 'Department of Energy'), 
              '84': ('91', 'Department of Education'), 
              '85': ('95', 'Various Scholarship and Fellowship Foundations'), 
              '86': ('16', 'Pension Benefit Guaranty Corporation'), 
              '88': ('95', 'Architectural and Transportation Barriers Compliance Board'), 
              '89': ('88', 'National Archives and Records Administration'), 
              '90': ('95', 'Denali Commission, Delta Regional Authority, Japan US Friendship Commission, US Election Assistance Commission, Broadcasting Board of Governors' ),
              '91': ('95', 'United States Institute of Peace'), 
              '93': ('75', 'Department of Health and Human Services'), 
              '94': ('95', 'Corporation for National and Community Service'), 
              '95': ('11', 'Executive Office of the President'), 
              '96': ('28', 'Social Security Administration'), 
              '97': ('70', 'Department of Homeland Security'), 
              '98': ('72', 'United States Agency for International Development') }
