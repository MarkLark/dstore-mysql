from dstore import Store, mod, var
from dstore.Error import InstanceNotFound
from .SQL import SQL
import MySQLdb
import MySQLdb.cursors


class MySQLStore( Store ):
    def __init__( self, models, name = "DataStore", config = None, config_prefix = "DSTORE_", con_cache = None ):
        super( MySQLStore, self ).__init__( models, name, config, config_prefix, con_cache )
        self.sql = SQL()

    def init_app( self ):
        self.set_config_defaults({
            "DSTORE_DB_HOST"       : "localhost",
            "DSTORE_DB_USER"       : None,
            "DSTORE_DB_PASSWD"     : None,
            "DSTORE_DB_DB"         : None,
            "DSTORE_DB_CURSORCLASS": MySQLdb.cursors.DictCursor
        })

        super( MySQLStore, self ).init_app()

    @staticmethod
    def table_name( model ):
        return model._namespace.replace( ".", "_" )

    def connect( self ):
        self.events.before_connect( self )
        con = MySQLdb.connect( **self.get_configs( prefix = "DSTORE_DB_" ) )
        self.events.after_connect( self )
        return con

    def disconnect( self ):
        self.events.before_disconnect( self )
        self.con.close()
        self._con = None
        self.events.after_disconnect( self )

    @property
    def cursor( self ):
        return self.con.cursor()

    def commit( self ):
        self.con.commit()

    def register_model( self, model ):
        super( MySQLStore, self ).register_model( model )
        self.sql.register_model( model )

    def execute( self, sql, autocommit = True ):
        print( "Executing: %s" % sql )
        cur = self.cursor
        cur.execute( sql )
        if autocommit: self.commit()
        return cur

    def _get_key_value_pairs( self, model, skip_vars = None ):
        keys   = []
        values = []
        assign = []

        if skip_vars is None: skip_vars = []

        for col in model._vars:
            key = col.name
            val = model.__dict__[ key ]

            if val is None: continue
            if key in skip_vars: continue

            key = str( key )
            if isinstance( col, var.Boolean ):
                if val: val = 1
                else  : val = 0
            val = str( val )

            keys.append( key )
            values.append( "'%s'" % val )
            assign.append( "%s = '%s'" % (key, val) )

        return keys, values, assign

    def create( self, model ):
        self.execute( self.sql[ model._namespace ][ "create" ] )

    def destroy( self, model ):
        self.execute( self.sql[ model._namespace ][ "destroy" ] )

    def empty( self, model ):
        super( MySQLStore, self ).empty( model )
        self.execute( self.sql[ model._namespace ][ "empty" ] )

    def add( self, instance, autocommit = True ):
        keys, values, assign = self._get_key_value_pairs( instance, [ "id" ] )
        sql = "INSERT INTO %s (%s) VALUES(%s)" % (
            MySQLStore.table_name( instance ),
            ", ".join( keys ),
            ", ".join( values )
        )

        cur = self.execute( sql, autocommit )

        instance.id = cur.lastrowid
        return instance

    def update( self, instance, autocommit = True ):
        keys, values, assign = self._get_key_value_pairs( instance, [ "id" ] )

        sql = "UPDATE %s SET %s WHERE id=%s" % (
            MySQLStore.table_name( instance ),
            ", ".join( assign ),
            instance.id
        )

        self.execute( sql, autocommit )
        return instance

    def get( self, cls, row_id ):
        cur = self.execute( self.sql[ cls._namespace ][ "get" ] % int( row_id ) )
        row = cur.fetchone()
        if row is None: raise InstanceNotFound( self, cls( id = row_id ) )

        return cls( **row )

    def all( self, cls ):
        cur = self.execute( self.sql[ cls._namespace ][ "all" ] )
        rtn = []
        for row in cur: rtn.append( cls( **row ) )
        return rtn

    def delete( self, instance, autocommit = True ):
        self.execute( self.sql[ instance._namespace ][ "delete" ] % int( instance.id ), autocommit )

    def filter( self, cls, **kwargs ):
        where = []
        for col in cls._vars:
            key = col.name
            if key not in kwargs: continue
            val = kwargs[ key ]
            if val is None: continue

            key = str( key )
            if isinstance( col, var.Boolean ):
                if val: val = 1
                else  : val = 0
            val = str( val )

            if "%" in val: where.append( "%s LIKE '%s'" % (key, val) )
            else         : where.append( "%s = '%s'" % (key, val) )

        sql = "SELECT * FROM %s WHERE %s" % ( cls._namespace.replace( ".", "_" ), " AND ".join( where ) )

        cur = self.execute( sql )

        rtn = []
        for row in cur: rtn.append( cls( **row ) )

        num_rows = len( rtn )
        if num_rows == 0:
            kwargs[ "id" ] = -1
            raise InstanceNotFound( self, cls( **kwargs ) )

        return rtn
