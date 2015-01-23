import sys
from collections import namedtuple

try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict

namedtuple_has_rename_kwarg = sys.version_info[:2] >= (2, 7)

def get_namedtuple(_name='AnonymousNamedtuple',
                   _data_arg=None,
                   _verbose=False,
                   _rename=False,
                   **kw):
    '''
    Creates a one-off namedtuple with a single function call, without
    explicitly instantiating it as a new class. For example, what was once:

    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> p = Point(3, 5)
    >>> p.x, p.y
    (3, 5)

    becomes:

    >>> p = get_namedtuple('Point', x=3, y=5)
    >>> p.x, p.y
    (3, 5)

    You can use this to easily make anonymous, immutable objects with
    attributes accessible by dot syntax:

    >>> me = get_namedtuple(name='Jim', language='Python')
    >>> me.name
    'Jim'
    >>> me.language
    'Python'

    The class of these objects instantiated without class names will be
    'AnonymousNamedtuple'. However, though the classes of different
    AnonymousNamedtuples share a name, the instances do not share a class!

    >>> me.__class__.__name__
    'AnonymousNamedtuple'
    >>> bdfl = get_namedtuple(name='Guido', language='Python')
    >>> bdfl.__class__.__name__
    'AnonymousNamedtuple'
    >>> me.__class__ == bdfl.__class__
    False

    This function can also take a key-value collection as input:

    >>> g = {'informal': 'Hi there!', 'formal': 'Hello; nice to meet you.'}
    >>> greetings = get_namedtuple('Greetings', g)
    >>> greetings.informal
    'Hi there!'
    >>> greetings.formal
    'Hello; nice to meet you.'

    It raises a ValueError if passed both a collection and keyword arguments
    for namedtuple fields.

    Note that, in the above ways of calling get_namedtuple, the order of the
    arguments to get_namedtuple is not necessarily preserved in the order of
    the returned namedtuple's fields. In this case, to access particular
    fields by index rather than by name, you must first determine the index of
    the attribute you want by looking at the _fields attribute:

    >>> i = greetings._fields.index('informal')
    >>> greetings[i]
    'Hi there!'

    Do not write code that depends on the order of the returned namedtuple's
    fields if you call the function in the above ways, as not all Python
    implementations guarantee deterministic order for dictionary keys and
    keyword arguments.

    You can also get namedtuples with guaranteed field order, sidestepping the
    problem entirely, by passing an ordered collection of key-value pairs:

    >>> get_namedtuple('Point', (('a', 5), ('b', 7)))._fields
    ('a', 'b')

    Internally, this is passed to the OrderedDict constructor, so inputs must
    conform to valid OrderedDict constructor arguments. You can also construct
    an OrderedDict yourself and pass it in if you prefer. See the
    documentation for OrderedDict in the collections module for more
    information.

    If _verbose and/or _rename are true, it calls namedtuple with verbose
    and/or rename, respectively; these arguments begin with an underscore to
    allow callers to specify fields called 'verbose' and 'rename'.

    This function performs no error handling around the instantiation of the
    namedtuple class or object, so it may raise any error that namedtuple
    does.

    For further documentation on verbose, rename, errors, and the returned
    namedtuple itself, see the documentation for namedtuple in the collections
    module.
    '''

    if _data_arg is not None and kw != {}:
        msg = ('get_namedtuple() called with {_data_arg} and keyword '
               'arguments{kw}, but it takes a collection or keyword '
               'arguments, not both.').format(_data_arg, kw)
        raise ValueError(msg)

    # constructing OrderedDict allows ordered inputs like
    # [('key1', 1), ('key2', 2)]
    kw = OrderedDict(_data_arg) if _data_arg is not None else kw

    # prepare keyword arguments for namedtuple() call
    nt_opts = {'verbose': _verbose}
    # rename kwarg introduced in 2.7
    if namedtuple_has_rename_kwarg:
        nt_opts['rename'] = _rename

    return namedtuple(_name, kw.keys(), **nt_opts)(**kw)
