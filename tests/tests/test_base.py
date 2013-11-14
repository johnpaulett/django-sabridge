from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from sabridge import Bridge
from sabridge.base import urlbuild


class URLBuildTest(TestCase):
    def test_path_only(self):
        self.assertEqual(urlbuild('sqlite', 'test.db'),
                         'sqlite:///test.db')

    def test_has_host(self):
        self.assertEqual(urlbuild('postgresql', 'test', hostname='10.0.0.1'),
                         'postgresql://10.0.0.1/test')

    def test_full_netloc(self):
        self.assertEqual(urlbuild('postgresql', 'test',
                                  hostname='10.0.0.1', port='5432',
                                  username='scott', password='tiger'),
                         'postgresql://scott:tiger@10.0.0.1:5432/test')

    def test_int_port(self):
        self.assertEqual(urlbuild('postgresql', 'test', hostname='10.0.0.1', port=5433),
                         'postgresql://10.0.0.1:5433/test')


class BridgeTest(TransactionTestCase):
    # Must use a TransactionTestCase so that inside a test, writes from Django
    # are available to SQLAlchemy.  The regular TestCase wraps each test in
    # a transaction, which it rolls back at the end. Since the data is not
    # actually committed to the database in a regular TestCase, SQLAlchemy
    # can not access it.
    #
    # The TransactionTestCase is unfortunately slower
    
    def setUp(self):
        self.bridge = Bridge()
    
    def test_maps_table(self):
        user_table = self.bridge[User]
        
        self.assertEqual(user_table.name, 'auth_user')
        self.assertEqual(user_table.c.username.name, 'username')
        
    def test_table_cached(self):
        user_table1 = self.bridge[User]
        user_table2 = self.bridge[User]

        self.assertEqual(id(user_table1), id(user_table2))
        
    def test_data_is_common_between_sa_and_django(self):
        user_table = self.bridge[User]

        # write on the Django side
        User.objects.create(username='chris')

        result = list(user_table.select().execute())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][user_table.c.username], 'chris')
