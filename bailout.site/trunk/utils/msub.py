import re


def msub_global(source, rep_list):
    """
    Do a global, multiple substitution on the 'source' parameter. The
    'rep_list' parameter is a list of replacements, where each list item is a
    tuple: (old, new).
    
    This replacement is done in one pass. This is fast and means that we don't
    have to worry about one pass interacting with another.
    
    Borrowed code from "Replacing Multiple Patterns in a Single Pass"
    from Chapter 1 of the O'Reilly Python Cookbook.

    >>> text = 'the loan guarantee was'
    >>> xform = [('loan guarantee', '<loan guarantee>'), ('loan', '<loan>')]
    >>> msub_global(text, xform)
    'the <loan guarantee> was'

    >>> text = 'the loan guarantee was'
    >>> xform = [('loan', '<loan>'), ('loan guarantee', '<loan guarantee>')]
    >>> msub_global(text, xform)
    'the <loan> guarantee was'

    >>> text = 'abcb'
    >>> xform = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>'), ]
    >>> msub_global(text, xform)
    '<air><black><cat><black>'
    """
    old_items = [a for a, b in rep_list]
    escaped = map(re.escape, old_items)
    regex = re.compile("|".join(escaped))
    rep_dict = dict(rep_list)

    def lookup(match):
        return rep_dict[match.group(0)]

    return regex.sub(lookup, source)

def msub_first(string, rep_list):
    """
    Do a multiple substitution on the 'string' parameter. The 'rep_list'
    parameter is a list of replacements, where each list item is a tuple:
    (old, new).

    Only replaces one time for each tuple.

    Replacement is done with multiple passes.

    >>> text = 'the loan guarantee was'
    >>> xform = [('loan guarantee', '<loan guarantee>'), ('loan', '<loan>')]
    >>> msub_first(text, xform)
    'the <loan guarantee> was'

    >>> text = 'the loan guarantee was'
    >>> xform = [('loan', '<loan>'), ('loan guarantee', '<loan guarantee>')]
    >>> msub_first(text, xform)
    'the <loan> guarantee was'

    >>> text = 'abcb'
    >>> xform = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>')]
    >>> msub_first(text, xform)
    '<air><black><cat>b'
    """
    result = string
    dirties = []
    for old, new in rep_list:
        matches = re.finditer(re.escape(old), result)
        match_count = 0
        for m in matches:
            if _clean_match(m, dirties):
                a, b = m.start(), m.end()
                if match_count < 1:
                    result = result[:a] + new + result[b:]
                    b = a + len(new)
                    dirties.append((a, b))
                else:
                    dirties.append((a, b))
                match_count += 1
    return result

def _clean_match(match, dirties):
    """
    >>> m = re.search('me', '---me---')

    >>> _clean_match(m, [])
    True
    >>> _clean_match(m, [(0, 1)])
    True
    >>> _clean_match(m, [(1, 2)])
    True
    >>> _clean_match(m, [(2, 3)])
    True
    >>> _clean_match(m, [(3, 4)])
    False
    >>> _clean_match(m, [(4, 5)])
    False
    >>> _clean_match(m, [(5, 6)])
    True
    >>> _clean_match(m, [(6, 7)])
    True
    >>> _clean_match(m, [(7, 8)])
    True

    >>> _clean_match(m, [(0, 2)])
    True
    >>> _clean_match(m, [(1, 3)])
    True
    >>> _clean_match(m, [(2, 4)])
    False
    >>> _clean_match(m, [(3, 5)])
    False
    >>> _clean_match(m, [(4, 6)])
    False
    >>> _clean_match(m, [(5, 7)])
    True
    >>> _clean_match(m, [(6, 8)])
    True
    """
    ma, mb = match.start(), match.end() - 1

    # Return false if  (ma, mb) overlaps any dirties.
    for d0, d1 in dirties:
        a, b = d0, d1 - 1
        if a <= ma and ma <= b:
            return False
        elif a <= mb and mb <= b:
            return False
        elif ma <= a and a <= mb:
            return False
        elif ma <= b and b <= mb:
            return False

    # If no dirties, we have a clean match.
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
