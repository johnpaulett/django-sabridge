====================================================
django-sabridge - SQLAlchemy access to Django models
====================================================

Motivation
==========

Usage
=====

To demonstrate sabridge, we will access 
:py:class:`django.contrib.auth.models.User` through SQLAlchemy.


Import and initialize the :py:class:`sabridge.Bridge`::

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
schema of the requested Django model.    

Contents
========

.. toctree::
   :maxdepth: 2
   
   api
   license
