import re


def pluralize(noun):
    """
    >>> pluralize('loan')
    'loans'
    >>> pluralize('dog')
    'dogs'
    >>> pluralize('dairy')
    'dairies'
    >>> pluralize('Box')
    'Boxes'
    >>> pluralize('Debt Security')
    'Debt Securities'
    >>> pluralize('')
    ''
    
    Borrowed heavily from an example from "Diving into Python":
    http://www.diveintopython.org/dynamic_functions/stage6.html
    """
    if noun == '': return ''
    rules = [
        ('^(sheep|deer|fish|moose)$' , '($)'   , '\1'   ),
        ('^(aircraft|series|haiku)$' , '($)'   , '\1'   ),
        ('[ml]ouse$'                 , 'ouse$' , 'ice'  ),
        ('child$'                    , '$'     , 'ren'  ),
        ('booth$'                    , '$'     , 's'    ),
        ('foot$'                     , 'oot$'  , 'eet'  ),
        ('ooth$'                     , 'ooth$' , 'eeth' ),
        ('l[eo]af$'                  , 'af$'   , 'aves' ),
        ('sis$'                      , 'sis$'  , 'ses'  ),
        ('^(hu|ro)man$'              , '$'     , 's'    ),
        ('man$'                      , 'man$'  , 'men'  ),
        ('^lowlife$'                 , '$'     , 's'    ),
        ('ife$'                      , 'ife$'  , 'ives' ),
        ('eau$'                      , '$'     , 'x'    ),
        ('^[dp]elf$'                 , '$'     , 's'    ),
        ('lf$'                       , 'lf$'   , 'lves' ),
        ('[sxz]$'                    , '$'     , 'es'   ),
        ('[^aeioudgkprt]h$'          , '$'     , 'es'   ),
        ('(qu|[^aeiou])y$'           , 'y$'    , 'ies'  ),
        ('$'                         , '$'     , 's'    )
    ]
    for pattern, search, replace in rules:
        result = re.search(pattern, noun) and re.sub(search, replace, noun)
        if result: return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
