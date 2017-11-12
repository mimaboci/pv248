import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.name = re.sub( '\([0-9+-]+\)', '', string )
        # TODO: years born/died
        self.born = re.sub('', '', string)
        self.died = re.sub('', '', string)

    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ?", (self.name,) )
        self.id = self.cursor.fetchone()

    def do_store( self ):
        self.cursor.execute( "insert into person (name) values (?)", (self.name,) )

class Score( DBItem ):
    
