VERSION = (0, 1, 0, 'dev')

def get_version():
    return '%s.%s.%s%s' % VERSION

__version__ = get_version()
