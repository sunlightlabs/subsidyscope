import sys
import csv
from cfda.models import ProgramDescription

MODEL_FIELDS = (
    'program_number',
    'program_title',
    'federal_agency',
    'major_agency',
    'minor_agency',
    'authorization',
    'objectives',
    'types_of_assistance',
    'uses_and_use_restrictions',
    'applicant_eligibility',
    'beneficiary_eligibility',
    'credentials_documentation',
    'preapplication_coordination',
    'application_procedure',
    'award_procedure',
    'deadlines',
    'range_of_approval_disapproval_time',
    'appeals',
    'renewals',
    'formula_and_matching_requirements',
    'length_and_time_phasing_of_assistance',
    'reports',
    'audits',
    'records',
    'account_identification',
    'obligations',
    'range_and_average_of_financial_assistance',
    'program_accomplishments',
    'regulations_guidelines_and_literature',
    'regional_or_local_office',
    'headquarters_office',
    'web_site_address',
    'related_programs',
    'examples_of_funded_projects',
    'criteria_for_selecting_proposals',
)

def main():
    f = open(sys.argv[1],'r')
    reader = csv.reader(f)
    for row in reader:        
        PD = ProgramDescription()
        i = 0
        for item in row:
            # print 'setting %s to %s' % (MODEL_FIELDS[i], item)
            if i==2:
                PD.save()
            setattr(PD, MODEL_FIELDS[i], item)
            i = i + 1
        PD.save()
    f.close()


if __name__ == '__main__':
    main()