import re


def multiple_sub(source, rep_list):
    """
    Do a multiple substitution on the 'source' parameter.  The 'rep_list'
    parameter is a list of replacements, where each list item is a
    tuple: (old, new).

    This replacement is done in one pass, which is faster than looping
    over multiple re.sub calls.

    Borrowed code from "Replacing Multiple Patterns in a Single Pass"
    from Chapter 1 of the O'Reilly Python Cookbook.
    """
    old_items = [a for a, b in rep_list]
    escaped = map(re.escape, old_items)
    regex = re.compile("|".join(escaped))
    rep_dict = dict(rep_list)

    def lookup(match):
        return rep_dict[match.group(0)]

    return regex.sub(lookup, source)
