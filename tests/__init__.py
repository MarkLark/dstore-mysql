from dstore import Model, var, mod
from dstore_mysql import MySQLStore
from unittest import TestCase
from os import environ


class Car( Model ):
    _namespace = "cars.make"
    _vars = [
        var.RowID,
        var.String( "manufacturer", 32, mods = [ mod.NotNull() ] ),
        var.String( "make", 32, mods = [ mod.NotNull() ] ),
        var.Number( "year", mods = [ mod.NotNull(), mod.Min( 1950 ), mod.Max( 2017 ) ] ),
    ]


class BaseTest( TestCase ):
    models      = [ Car ]#, AllVars ]
    auto_create = True
    auto_init   = True

    def setUp( self ):
        if self.auto_init:
            self.store = MySQLStore( self.models )
            self.store.init_app()

            if environ.get( "VM" ) is None:
                self.store.set_config({
                    "DSTORE_DB_HOST"  : "localhost",
                    "DSTORE_DB_USER"  : "root",
                    "DSTORE_DB_PASSWD": "",
                    "DSTORE_DB_DB"    : "dstore_test"
                })
            else:
                self.store.set_config({
                    "DSTORE_DB_HOST"  : "localhost",
                    "DSTORE_DB_USER"  : "flask",
                    "DSTORE_DB_PASSWD": "flask123",
                    "DSTORE_DB_DB"    : "flask"
                })
            self.store.connect()
        if self.auto_create: self.store.create_all()

    def tearDown( self ):
        if self.auto_create: self.store.destroy_all()
        if self.auto_init:
            self.store.disconnect()
            self.store.destroy_app()
