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

    >>> fowl = 'duck duck goose duck duck'
    >>> sounds = [('duck', 'quack'), ('goose', 'honk')]
    >>> msub_global(fowl, sounds)
    'quack quack honk quack quack'

    >>> text = 'the blue dog jumped over the yellow fox'
    >>> xform = [('dog', 'cat'), ('cat jumped over', 'cat clawed')]
    >>> msub_global(text, xform)
    'the blue cat jumped over the yellow fox'
    """
    old_items = [a for a, b in rep_list]
    escaped = map(re.escape, old_items)
    regex = re.compile("|".join(escaped))
    rep_dict = dict(rep_list)

    def lookup(match):
        return rep_dict[match.group(0)]

    return regex.sub(lookup, source)

def msub_first(source, rep_list):
    """
    Do a multiple substitution on the 'source' parameter. The
    'rep_list' parameter is a list of replacements, where each list item is a
    tuple: (old, new).

    Only replaces one time for each tuple.
    
    Replacement is done with multiple passes.

    >>> fowl = 'duck duck goose duck duck'
    >>> sounds = [('duck', 'quack'), ('goose', 'honk')]
    >>> msub_first(fowl, sounds)
    'quack duck honk duck duck'

    >>> text = 'the blue dog jumped over the yellow fox'
    >>> xform = [('dog', 'cat'), ('cat jumped over', 'cat clawed')]
    >>> msub_first(text, xform)
    'the blue cat jumped over the yellow fox'
    """
    # First phase: find matches for tuples
    matches = []
    for old, new in rep_list:
        regex = re.compile(re.escape(old))
        m = regex.search(source)
        if m: matches.append(m)

    # Second phase: do replacements
    rep_dict = dict(rep_list)
    result = source
    length_correction = 0
    for m in matches:
        old = m.group(0)
        if any([old == a for a, b in rep_list]):
            new = rep_dict[old]
            a = m.start() + length_correction
            b = m.end() + length_correction
            result = result[:a] + new + result[b:]
            length_correction += len(new) - len(old)

    # Note: this function is split into two phases in order to only replace
    # the first occurrence of a given term.
    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
