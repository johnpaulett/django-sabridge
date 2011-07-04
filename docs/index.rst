====================================================
django-sabridge - SQLAlchemy access to Django models
====================================================

Motivation
==========

Django's ORM is wonderful and easy to use. When the standard ORM operations are
insufficient for an application, Django provides `multiple methods 
<https://docs.djangoproject.com/en/dev/topics/db/sql/>`_ for more directly
interacting with the database, including :py:meth:`django.db.models.Manager.raw` 
and :py:meth:`django.db.connection.cursor`. However, using these methods can easily
lead to vendor lock-in. Additionally, programmatically building SQL is a difficult
task (especially to do so securely).

`SQLAlchemy <http://www.sqlalchemy.org/>`_ offers an excellent SQL rendering
engine, which allows programmatic generation of SQL.  By exposing Django models
via SQLAlchemy's `Expression Language <http://www.sqlalchemy.org/docs/core/>`_, 
a developer can build extremely complex queries while retaining 
database-independence (vendor-specific features are still available).

Other `efforts <http://code.google.com/p/django-sqlalchemy/>`_ have aimed to 
replace Django's ORM with SQLAlchemy's ORM.  django-sabridge instead leaves
Django's ORM in place, while allowing SQLAlchemy Expression Language to easily 
access those Django models.

django-sabridge addresses a specific need.  It may not be the ideal solution, 
so please :doc:`contribute <develop>` better approaches.  Please also be aware
of the :ref:`sabridge-caveats`.


Usage
=====

To demonstrate sabridge, we will access 
:py:class:`django.contrib.auth.models.User` through SQLAlchemy.


First, import and initialize the :py:class:`sabridge.Bridge`::

    >>> from sabridge import Bridge
    >>> bridge = Bridge()

We use the model's class to obtain the SQLAlchemy version of the table::

    >>> from django.contrib.auth.models import User
    >>> table = bridge[model]

The :py:class:`sabridge.Bridge` returns an instance of 
:py:class:`sqlalchemy.schema.Table`. If we write data in Django, we can 
then view that data via SQLAlchemy::

    >>> User.objects.create(username='alice')
    >>> result = list(table.select().execute())
    >>> len(result)
    1
    >>> result[0][table.c.username]
    u'alice'

.. _sabridge-caveats:

Caveats
=======

Transactions
------------

sabridge does not re-use Django's connection to the database, 
thus if executing in a transaction, any data modified by either
Django or SQLAlchemy will not be visible to the other, until the 
transaction is committed.

Practically, this means that any test cases that uses both Django 
and SQLAlchemy will have to inherit from 
:py:class:`django.test.TransactionTestCase` instead of the more typical
:py:class:`django.test.TestCase`.  The TransactionTestCase does not
wrap each test in a transaction, thus the data modified by SQLAlchemy 
and Django is not isolated. Unfortunately, the TransactionTestCase
is significantly slower than the normal TestCase. Refer to the
`TransactionTestCase documentation <https://docs.djangoproject.com/en/dev/topics/testing/#django.test.TransactionTestCase>`_.


Performance
-----------

sabridge uses SQLAlchemy's reflection (``autoload=True``) to discover the
schema of the requested Django model. Efforts are made to reduce the number of
times introspection occurs, but a user of django-sabridge should make sure
that it fits within any performance requirements.

Contents
========

.. toctree::
   :maxdepth: 2
   
   api
   develop
   changelog
   license

Links
=====

 * https://github.com/johnpaulett/django-sabridge
 * http://django-sabridge.readthedocs.org
