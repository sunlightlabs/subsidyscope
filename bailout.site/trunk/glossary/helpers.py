import models

def glossarize(instring):
    # run through each possibility in the glossary
    outstring = instring.replace("TARP", """<a href="/glossary#tarp">TARP</a>""")
    return outstring

# TODO: write a function that:
# * takes a string as input
# * returns a string, where certain keywords are transformed
#   into hyperlinks to the glossary
