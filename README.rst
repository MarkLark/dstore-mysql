Welcome To DStore-MySQL
#######################

DStore-MySQL is a MySQL storage layer for DStore.
This allows you to use the same Model descriptions to Create, Read, Update and Delete from a MySQL DataBase.


Installing
==========

PyMan is available from the PyPi repository.

This means that all you have to do to install DStore-MySQL is run the following in a console:

.. code-block:: console

    $ pip install dstore-mysql

Minimal Example
===============

.. code-block:: python

    from dstore import Model, var, mod
    from dstore_mysql import MySQLStore

    class Car( Model ):
        _namespace = "cars.make"
        _vars = [
            var.RowID,
            var.String( "manufacturer", 32, mods = [ mod.NotNull() ] ),
            var.String( "make", 32, mods = [ mod.NotNull() ] ),
            var.Number( "year", mods = [ mod.NotNull(), mod.Min( 1950 ), mod.Max( 2017 ) ] ),
        ]

    # Create the MemoryStore instance, and add Models to it
    store = MySQLStore( self.models )
    store.init_app()
    store.set_config({
        "DSTORE_DB_HOST"  : "localhost",
        "DSTORE_DB_USER"  : "username",
        "DSTORE_DB_PASSWD": "password",
        "DSTORE_DB_DB"    : "dstoredb"
    })
    store.connect()
    store.create_all()

    # Destroy all instances and shut down the application
    store.destroy_all()
    store.disconnect()
    store.destroy_app()


Documentation: `ReadTheDocs <http://dstore-mysql.readthedocs.io/>`_

Source Code: `GitHub <https://github.com/MarkLark/dstore-mysql>`_
