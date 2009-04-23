import sys
import csv
from cfda.models import ProgramDescription

def main():
    f = open(sys.argv[1], 'r')
    reader = csv.reader(f)
    i = 0
    for row in reader:
        count = ProgramDescription.objects.filter(program_number=row[0]).count()
        if count==0:
            print 'missing %s: %s' % (row[0], row[1])
        else:
            print 'found match for %s: %s' % (row[0], row[1])  
        i = i + 1
    f.close()
    print 'total: %d' % i

if __name__ == '__main__':
    main()