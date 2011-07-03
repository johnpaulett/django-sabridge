#!/usr/bin/env python

# based upon django-sentry/runtests.py
from django.conf import settings
from optparse import OptionParser
from os.path import dirname, abspath, join

import sys

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'TEST_NAME': 'sabridge_tests.db',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',

            'tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
        TEMPLATE_DEBUG=True,
    )

from django.test.simple import DjangoTestSuiteRunner

def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    runner = DjangoTestSuiteRunner(
        verbosity=kwargs.get('verbosity', 1),
        interactive=kwargs.get('interactive', False),
        failfast=kwargs.get('failfast')
    )
    failures = runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)
