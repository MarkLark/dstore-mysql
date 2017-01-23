from dstore import var, mod


class SQL( dict ):
    @staticmethod
    def table_name( model ):
        return model._namespace.replace( ".", "_" )

    def register_model( self, model ):
        self[ model._namespace ] = {
            "create" : self._sql_create( model ),
            "destroy": self._sql_destroy( model ),
            "get"    : self._sql_get( model ),
            "delete" : self._sql_delete( model ),
            "all"    : self._sql_all( model ),
            "empty"  : self._sql_empty( model )
        }

    def _sql_create( self, model ):
        cols = [ ]
        cons = [ ]

        for v in model._vars:
            cols.append( "    %s" % self._sql_create_col( v ) )
            con = self._sql_create_constraints( v )
            for c in con: cons.append( "    %s" % c )

        sql_cols = ",\n".join( cols )
        sql_cons = ",\n".join( cons )

        return """
CREATE TABLE IF NOT EXISTS %s
(
    %s,
    %s
)
""" % (
    SQL.table_name( model ),
    sql_cols,
    sql_cons
)

    def _sql_create_col( self, v ):
        mods = " ".join( self._sql_create_mod( m ) for m in v._mods )
        if v.default is not None:
            # Implement more default values (Float)
            if   isinstance( v, var.Number  ): mods += " DEFAULT %d" % v.default
            elif isinstance( v, var.Boolean ): mods += " DEFAULT %s" % ("TRUE" if v.default else "FALSE")
            else                             : mods += " DEFAULT '%s'" % v.default

        if   isinstance( v, var.Number    ): return "%s INT %s"         % ( v.name, mods )
        elif isinstance( v, var.String    ): return "%s VARCHAR(%d) %s" % ( v.name, v.length, mods )
        elif isinstance( v, var.Enum      ): return "%s ENUM('%s') %s"  % ( v.name, "', '".join( v.values ), mods )
        elif isinstance( v, var.Character ): return "%s CHAR(%s) %s"    % ( v.name, v.length, mods )
        elif isinstance( v, var.Binary    ): return "%s BINARY(%s) %s"  % ( v.name, v.length, mods )
        elif isinstance( v, var.Text      ): return "%s TEXT %s"        % ( v.name, mods )
        elif isinstance( v, var.Float     ): return "%s FLOAT %s"       % ( v.name, mods )
        elif isinstance( v, var.Boolean   ): return "%s BOOL %s"        % ( v.name, mods )
        elif isinstance( v, var.Date      ): return "%s DATE %s"        % ( v.name, mods )
        elif isinstance( v, var.Time      ): return "%s TIME %s"        % ( v.name, mods )
        elif isinstance( v, var.DateTime  ): return "%s DATETIME %s"    % ( v.name, mods )
        return ""

    def _sql_create_mod( self, m ):
        if   isinstance( m, mod.NotNull       ): return "NOT NULL"
        elif isinstance( m, mod.AutoIncrement ): return "AUTO_INCREMENT"
        return ""

    def _sql_create_constraints( self, v ):
        cons = []
        for m in v._mods:
            if   isinstance( m, mod.PrimaryKey ): cons.append( "PRIMARY KEY (%s)" % v.name )
            elif isinstance( m, mod.Unique     ): cons.append( "UNIQUE (%s)" % v.name )
            elif isinstance( m, mod.ForeignKey ): cons.append(
                "FOREIGN KEY (%s) REFERENCES %s(id)" % (
                    v.name, m.namespace.replace( ".", "_" )
                ))
        return cons

    def _sql_destroy( self, model ):
        return "DROP TABLE IF EXISTS %s" % SQL.table_name( model )

    def _sql_get( self, model ):
        rtn = "SELECT * FROM %s WHERE id=" % SQL.table_name( model )
        return rtn + "%d"

    def _sql_delete( self, model ):
        rtn = "DELETE FROM %s WHERE id=" % SQL.table_name( model )
        return rtn + "%d"

    def _sql_all( self, model ):
        return "SELECT * FROM %s" % SQL.table_name( model )

    def _sql_empty( self, model ):
        return "TRUNCATE TABLE %s" % SQL.table_name( model )
