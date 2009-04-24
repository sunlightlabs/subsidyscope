import re
import sys
from cfda.models import *
from etl.models import *
import django.utils.encoding

class CFDAImporter(object):

    FIELD_TO_MODEL_MAPPING = {
        'PROGRAM NUMBER': 'program_number',
        'PROGRAM TITLE': 'program_title',
        'PROGRAM NOTE': 'program_note',
        'FEDERAL AGENCY': 'federal_agency',
        'AUTHORIZATION': 'authorization',
        'OBJECTIVES': 'objectives',
        'TYPES OF ASSISTANCE': 'types_of_assistance',
        'USES AND USE RESTRICTIONS': 'uses_and_use_restrictions',
        'APPLICANT ELIGIBILITY': 'applicant_eligibility',
        'BENEFICIARY ELIGIBILITY': 'beneficiary_eligibility',
        'CREDENTIALS/DOCUMENTATION': 'credentials_documentation',
        'PREAPPLICATION COORDINATION': 'preapplication_coordination',
        'APPLICATION PROCEDURE': 'application_procedure',
        'AWARD PROCEDURE': 'award_procedure',
        'DEADLINES': 'deadlines',
        'RANGE OF APPROVAL/DISAPPROVAL TIME': 'range_of_approval_disapproval_time',
        'APPEALS': 'appeals',
        'RENEWALS': 'renewals',
        'FORMULA AND MATCHING REQUIREMENTS': 'formula_and_matching_requirements',
        'LENGTH AND TIME PHASING OF ASSISTANCE': 'length_and_time_phasing_of_assistance',
        'REPORTS': 'reports',
        'AUDITS': 'audits',
        'RECORDS': 'records',
        'ACCOUNT IDENTIFICATION': 'account_identification',
        'OBLIGATIONS': 'obligations',
        'RANGE AND AVERAGE OF FINANCIAL ASSISTANCE': 'range_and_average_of_financial_assistance',
        'PROGRAM ACCOMPLISHMENTS': 'program_accomplishments',
        'REGULATIONS, GUIDELINES, AND LITERATURE': 'regulations_guidelines_and_literature',
        'REGIONAL OR LOCAL OFFICE': 'regional_or_local_office',
        'HEADQUARTERS OFFICE': 'headquarters_office',
        'WEB SITE ADDRESS': 'web_site_address',
        'RELATED PROGRAMS': 'related_programs',
        'EXAMPLES OF FUNDED PROJECTS': 'examples_of_funded_projects',
        'CRITERIA FOR SELECTING PROPOSALS': 'criteria_for_selecting_proposals',
    }
    
    re_ignorable_line = re.compile(r'^\s{30,}')
    re_program_line = re.compile(r'^\d{2}\.\d{3}')
    re_trailing_junk = re.compile(r'\s{20,}.*$')
    CFDA_YEAR = 2008

    def __init__(self):
        super(CFDAImporter, self).__init__()
        self.active_record = {}
        self.active_token = None        
        
    
    def create_empty_record(self):
        out = {}
        for k in self.FIELD_TO_MODEL_MAPPING:
            out[k] = ""
        return out
        
    def emit_record(self):
        if len(self.active_record.keys())>0:
            record = self.post_process_record(self.active_record)
            
            sys.stderr.write("%s %s\n" % (self.active_record['PROGRAM NUMBER'], self.active_record['PROGRAM TITLE']))
            
            PD = ProgramDescription()
            PD.cfda_edition = self.CFDA_YEAR
            PD.program_number = record['PROGRAM NUMBER']
            PD.save()            
            for k in record:
                unicode_string = unicode(record[k], 'latin1', 'replace')
                setattr(PD, self.FIELD_TO_MODEL_MAPPING[k], unicode_string)

            PD.save()

        self.active_token = None
        self.active_record = self.create_empty_record()
    
    def cleanup(self):
        self.emit_record()

    def post_process_record(self, record):
        for f in record:
            record[f] = record[f].strip()

        record['PROGRAM TITLE'] = self.re_trailing_junk.sub('', record['PROGRAM TITLE'])
        return record

        
    def process_line(self, line):
        # junk line? if so, return
        if self.re_ignorable_line.match(line):
            return
        
        # only record the line if the token hasn't changed (title is a special case)
        add_this_line = True

        # check for new active token
        m = self.re_program_line.match(line)
        if m:
            self.emit_record()
            self.active_record['PROGRAM NUMBER'] = m.group(0)
            line = line.replace(self.active_record['PROGRAM NUMBER'],'')
            self.active_token = 'PROGRAM TITLE'
        else:
            for candidate_token in self.FIELD_TO_MODEL_MAPPING:
                line_token = line.replace(':','').upper().strip()
                if line_token==candidate_token:
                    self.active_token = candidate_token
                    add_this_line = False
        
        # check for lowercase note in program title area
        if self.active_token=='PROGRAM TITLE' and not line==line.upper():
            self.active_token = 'PROGRAM NOTE'
        
        if add_this_line and self.active_token is not None and len(line.strip())>0:
            self.active_record[self.active_token] = self.active_record[self.active_token] + ' ' + line.strip()
          
          
def main():
    C = CFDAImporter()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
            
        C.process_line(line)
        
    C.cleanup()
            
if __name__ == '__main__':
    main()        