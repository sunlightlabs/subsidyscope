import re, sys, os
from BeautifulSoup import BeautifulSoup

def adjust_footnotes(page):

    page_text = page.read()    
    out_text = []
    soup = BeautifulSoup(page_text)
    notes = soup.findAll("a", "footnote")    
    num_notes = len(notes)

    split_page = page_text.split("#footnote-")
    
    count = 0
    for l in split_page:
        out = ""
        if count == 0:
            out_text.append(l)
        else:
            out += "#footnote-"
            out += str(count)
            quote = l.index('"')
            carat = l.index('>')
            end_carat = l.index('<')

            out += l[quote:carat + 1]
            out += str(count)
            out += l[end_carat:]
            out_text.append(out)

        count += 1

    inter_text = ''.join(out_text)

    split_notes = inter_text.split('name="footnote-')
    count = 0
    out_text = []
    for n in split_notes:
        out = ""
        if count == 0:
            out_text.append(n)
        else:
            out += 'name="footnote-%s' % count
            out += n[n.index('"'):]
            out_text.append(out)
        
        count += 1
    
    new_text = ''.join(out_text)
    f = open("output/page.txt", 'w')
    f.write(new_text)


adjust_footnotes(open("input/page.txt"))

