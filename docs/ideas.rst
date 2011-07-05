Ideas
=====

A collection of some random ideas & thoughts for future implementations

* Easier access for the `through` table for :py:class:`django.db.models.ManyToManyFields`
  than requiring the user to manually access ``Model.column._through()``
* We could use SQLAlchemy to generate the SQL for :py:func:`django.db.connection.cursor`,
  allowing reuse of Django's current transaction.  This should currently work,
  but we could add some sugar for making it easier & documenting it.  It would
  mean that you no longer get a SQLAlchemy ResultProxy back.
