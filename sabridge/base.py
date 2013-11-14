from sqlalchemy import create_engine, MetaData, Table

# TODO support mutliple DBs via db.connections
class Bridge(object):
    def __init__(self):
        # prep the attributes, allowing them to be lazily loaded
        self._meta = None
        self._tables = {}
        
    def connection_url(self):
        """Build a URL for :py:func:`sqlalchemy.create_engine`
        based upon the database defined by :py:attr:`django.db.connection`
        """
        # we lazily import connection since it requires a DJANGO_SETTINGS_MODULE
        from django.db import connection
        
        return urlbuild(
            scheme=connection.vendor,
            path=connection.settings_dict['NAME'],
            username=connection.settings_dict['USER'],
            password=connection.settings_dict['PASSWORD'],
            hostname=connection.settings_dict['HOST'],
            port=connection.settings_dict['PORT']
        )

    def _map_model(self, model_cls):
        # TODO consider performance implications of autoloading schema
        return Table(model_cls._meta.db_table, self.meta, autoload=True)

    def __getitem__(self, model_cls):
        """Returns the :py:class:`sqlalchemy.schema.Table` representation
        of ``model_cls``, a :py:class:`django.db.models.Model` subclass.

        Use dict-notation to obtain the ``Table``::
        
            >>> from myapp.models import mymodel
            >>> brige = Bridge()
            >>> mytable = bridge[mymodel]
            >>> print type(mytable)
            <class 'sqlalchemy.schema.Table'>

        ``Bridge`` stores the ``Table`` for the lifetime of the ``Bridge``,
        thus table reflection only occurs once per model for the ``Bridge``.
        """
        # not thread-safe, but at worst, we re-autoload the table
        if model_cls not in self._tables:
            self._tables[model_cls] = self._map_model(model_cls)

        return self._tables[model_cls]

    @property
    def meta(self):
        """:py:class:`sqlalchemy.schema.MetaData` instance bound to the current
        Django database connection."""
        # Lazily connect to the database. By waiting until meta is
        # needed, we prevent capturing stale connection info from Django
        # (e.g. during a TestCase)
        if self._meta is None:
            self._meta = MetaData()
            self._meta.bind = create_engine(self.connection_url())
        return self._meta

def urlbuild(scheme, path, username=None, password=None, hostname=None, port=None):
    """Builds a URL to pass into :py:func:`sqlalchemy.create_engine`

    dialect+driver://username:password@host:port/database
    """
    # we could use urlparse.ParseResult, but we would still need to manually
    # build the whole netloc, so we don't gain much
    
    # build the netloc depending on what parts we are given,
    # later join the netloc together
    netloc = []
    if username:
        netloc.append(username)
    if password:
        netloc.append(':')
        netloc.append(password)
    if username or password:
        netloc.append('@')
    if hostname:
        netloc.append(hostname)
    if port:
        netloc.append(':')
        netloc.append(str(port))

    # put it all together
    return '{scheme}://{netloc}/{path}'.format(scheme=scheme,
                                               netloc=''.join(netloc),
                                               path=path)
