import sys
import os
from cfda_settings import * 

for pagenum in range(723, END_PAGE+1):
    sys.stderr.write("Processing page %6d/%6d\n" % (pagenum, END_PAGE))
    rendered_text_handle = os.popen('pdftotext -layout -f %d -l %d CFDA.pdf - 2>/dev/null' % (pagenum, pagenum))    
    rendered_text = []
    for line in rendered_text_handle:
        rendered_text.append(line)

    # find longest line
    longest_line = 0
    for line in rendered_text:
        longest_line = max(longest_line, len(line))
    
    # perform a binary AND for spaces on all the lines of this page
    working_line = "".zfill(longest_line)
    for line in rendered_text:
        out_line = ""
        for i in range(0, len(working_line)):
            if i<len(line):
                if not line[i]==' ':
                    out_line = out_line + '1'
                else:
                    out_line = out_line + working_line[i]
            else:
                out_line = out_line + working_line[i]
        working_line = out_line
    
    # find the length of each span of spaces
    space_groups = []
    for i in range(0, len(working_line)):
        char = working_line[i]
        if char=='0':
            run_length = 1
            run_start = i
            i = i + 1
            while i<len(working_line) and working_line[i]=='0':
                run_length = run_length + 1
                i = i + 1
            space_groups.append({ 'length': run_length, 'start': run_start})
    
    # find the longest span of spaces
    space_groups.sort(key = lambda x: x['length'] )

    # is there a span of spaces? if not, may be a single-pager
    split_group = None
    if len(space_groups):

        max_length = space_groups[-1]['length']

        # sort the spans of spaces sharing the max length so that they ordered by their start position (ascending)
        eligible_groups = []
        for group in space_groups:
            if group['length']==max_length:
                eligible_groups.append(group)            
        eligible_groups.sort(key=lambda x: x['length'])
    
        # there's our split position!
        split_group = eligible_groups[0]
                

    # now actually split the pages
    parts = [[], []]
    for line in rendered_text:
        if not split_group is None:
            parts[0].append(line[0:split_group['start']])
            parts[1].append(line[(split_group['start']+split_group['length']):])
        else:
            parts[0].append(line)
    page_text = "\n".join(parts[0]) + "".join(parts[1])
    f = open('pages/%d.txt' % pagenum, 'w')
    f.write(page_text)
    f.close()