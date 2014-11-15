from collections import namedtuple


def get_namedtuple(name, d=None, _verbose=False, _rename=False, **kw):
    '''
    Creates a one-off namedtuple without explicitly instantiating it as a new
    class. For example, what was once:

    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> p = Point(3, 5)
    >>> p.x, p.y
    (3, 5)

    becomes:

    >>> s = get_namedtuple('Point', x=3, y=5)
    >>> s.x, s.y
    (3, 5)

    Note that the ordering of the fields is not preserved from the order
    of the arguments. To access the fields by index, you must first determine
    the index of the attribute you want by looking at the _fields attribute:

    >>> i = s._fields.index('y')
    >>> s[i]
    5

    This function can also take a dictionary as input:

    >>> g = {'informal': 'Hi there!', 'formal': 'Hello; nice to meet you.'}
    >>> get_namedtuple('Greetings', g)
    Greetings(formal='Hello; nice to meet you.', informal='Hi there!')

    If _verbose and/or _rename are true, it calls namedtuple with verbose and
    rename respectively; these arguments begin with an underscore to allow
    callers to specify fields called 'verbose' and 'rename'.

    It raises a ValueError if passed both a dictionary and keyword arguments
    for namedtuple fields.

    This function performs no error handling around the namedtuple call, and
    may raise any error that namedtuple does.
    '''
    if d is not None and kw != {}:
        msg = 'get_namedtuple() called with {} and {}, but '.format(d, kw)
        msg += 'it takes a dictionary or keyword arguments, not both.'
        raise ValueError(msg)

    ntkw = d if d is not None else kw

    return namedtuple(name, ntkw.keys(),
                      verbose=_verbose, rename=_rename)(**ntkw)
