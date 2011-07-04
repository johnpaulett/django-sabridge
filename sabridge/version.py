VERSION = (0, 1, 0, 'dev')

def get_version():
    base = '.'.join((str(x) for x in VERSION[0:3]))
    if VERSION[3] == 'final':
        return base
    return '%s%s' % (base, VERSION[3])

__version__ = get_version()
