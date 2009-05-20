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

    >>> s = 'abcb'
    >>> xform = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>'), ]
    >>> msub_global(s, xform)
    '<air><black><cat><black>'

    >>> s = 'Equity considerations mean that'
    >>> xform = [('equity', '<*>')]
    >>> msub_global(s, xform)
    '<Equity> considerations mean that'

    >>> s = 'the Loan Guarantee was'
    >>> xform = [('loan guarantee', '<*>'), ('loan', '<*>')]
    >>> msub_global(s, xform)
    'the <Loan Guarantee> was'

    >>> s = 'the Loan Guarantee was'
    >>> xform = [('loan', '<*>'), ('loan guarantee', '<*>')]
    >>> msub_global(s, xform)
    'the <Loan> Guarantee was'

    >>> s = 'the Federal Deposit Insurance Corporation acted'
    >>> xform = [('Federal Deposit Insurance Corporation', '<*>'), ('Deposit Insurance', '<*>')]
    >>> msub_first(s, xform)
    'the <Federal Deposit Insurance Corporation> acted'
    """
    old_items = [a for a, b in rep_list]
    escaped = map(re.escape, old_items)
    regex = re.compile("|".join(escaped), re.IGNORECASE)
    rep_dict = dict(rep_list)

    def lookup(match):
        key = match.group(0).lower()
        return _replace_token(match, rep_dict[key])

    return regex.sub(lookup, source)

def msub_first(string, rep_list):
    """
    Do a multiple substitution on the 'string' parameter. The 'rep_list'
    parameter is a list of replacements, where each list item is a tuple:
    (old, new).

    Only replaces one time for each tuple.

    Replacement is done with multiple passes.

    >>> s = 'abcb'
    >>> xform = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>')]
    >>> msub_first(s, xform)
    '<air><black><cat>b'

    >>> s = 'Equity considerations mean that'
    >>> xform = [('equity', '<*>')]
    >>> msub_first(s, xform)
    '<Equity> considerations mean that'

    >>> s = 'the Loan Guarantee was'
    >>> xform = [('loan guarantee', '<*>'), ('loan', '<*>')]
    >>> msub_first(s, xform)
    'the <Loan Guarantee> was'

    >>> s = 'the Loan Guarantee was'
    >>> xform = [('loan', '<*>'), ('loan guarantee', '<*>')]
    >>> msub_first(s, xform)
    'the <Loan> Guarantee was'
    
    >>> s = 'the Federal Deposit Insurance Corporation acted'
    >>> xform = [('Federal Deposit Insurance Corporation', '<*>'), ('Deposit Insurance', '<*>')]
    >>> msub_first(s, xform)
    'the <Federal Deposit Insurance Corporation> acted'
    
    >>> s = 'showing <a href="/media/20090131.csv">evidence</a> that'
    >>> xform = [('csv', '<*>'), ('media', '<*>')]
    >>> msub_first(s, xform)
    'showing <a href="/media/20090131.csv">evidence</a> that'
    """
    dirties = _selected_html_tag_spans(string)
    result = string
    for pattern, replace in rep_list:
        matches = re.finditer(pattern, result, re.IGNORECASE)
        match_count = 0
        for m in matches:
            if _clean_match(m, dirties):
                a, b = m.start(), m.end()
                if match_count < 1:
                    new = _replace_token(m, replace)
                    result = result[:a] + new + result[b:]
                    dirties.append((a, a + len(new)))
                else:
                    dirties.append((a, b))
                match_count += 1
    return result

def _selected_html_tag_spans(string):
    """
    This is a very naive and lightweight way to find the spans (i.e. the
    start and finish) of fragments.  By fragment I mean a start tag,
    its contents, and its end tag.  Only certain HTML tags are considered.
    
    For example:
    >>> f = _selected_html_tag_spans
    >>> s1 = "According to <a href='http://cnn.com'>CNN</a>, "
    >>> f(s1)
    [(13, 45)]
    >>> s2 = "the <a name='p02'>anchor</a> reported"
    >>> f(s1 + s2)
    [(13, 45), (51, 75)]
    >>> f("<strong>hello</strong> there <div>world</div>!")
    []
    >>> s = 'showing <a href="/media/20090131.csv">evidence</a> that'
    >>> f(s)
    [(8, 50)]
    """
    pattern = '<a[^>]*>.*?</a>'
    matches = re.finditer(pattern, string, re.IGNORECASE)
    return [m.span() for m in matches]

def _replace_token(match, new):
    """
    Replaces the token (*) with the match result.
    """
    token = re.escape('*')
    return re.sub(token, match.group(0), new, 1)

def _clean_match(match, dirties):
    """
    Is the match clean, e.g. does the string match occur in
    a place that does not overlap any of the dirty spans?
    
    >>> m = re.search('me', '---me---')
    >>> f = _clean_match
    >>> f(m, [])
    True
    >>> f(m, [(0, 1)])
    True
    >>> f(m, [(1, 2)])
    True
    >>> f(m, [(2, 3)])
    True
    >>> f(m, [(3, 4)])
    False
    >>> f(m, [(4, 5)])
    False
    >>> f(m, [(5, 6)])
    True
    >>> f(m, [(6, 7)])
    True
    >>> f(m, [(7, 8)])
    True
    
    >>> f(m, [(0, 1), (2, 3)])
    True
    >>> f(m, [(0, 1), (3, 4)])
    False
    >>> f(m, [(3, 4), (0, 1)])
    False

    >>> f(m, [(0, 2)])
    True
    >>> f(m, [(1, 3)])
    True
    >>> f(m, [(2, 4)])
    False
    >>> f(m, [(3, 5)])
    False
    >>> f(m, [(4, 6)])
    False
    >>> f(m, [(5, 7)])
    True
    >>> f(m, [(6, 8)])
    True
    """
    ma, mb = match.start(), match.end() - 1

    # Return false if (ma, mb) overlaps any dirties.
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
