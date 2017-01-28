import pymysql
import pymysql.cursors


class MySQL3( object ):
    def __init__( self, store ):
        self.store = store
        self.config_defaults = {
            "DSTORE_DB_HOST"       : "localhost",
            "DSTORE_DB_USER"       : None,
            "DSTORE_DB_PASSWD"     : None,
            "DSTORE_DB_DB"         : None,
            "DSTORE_DB_CURSORCLASS": pymysql.cursors.DictCursor
        }

    def connect( self ):
        return pymysql.connect( **self.store.get_configs( prefix = "DSTORE_DB_" ) )
