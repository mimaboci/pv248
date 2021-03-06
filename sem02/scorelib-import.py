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
        self.born = None
        self.died = None

        m = re.search( "([0-9]+)--([0-9]+)", string )
        if m is not None:
            self.born = int(m.group(1).strip())
            self.died = int(m.group(2).strip())

    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ? and born = ? and died = ?", 
		(self.name, self.born, self.died) )
        
        r = self.cursor.fetchone()
        if r is None:
            return
        self.id = r[0]
        
        if(self.born is not None and self.died is not None):
            self.cursor.execute( "update person set born = {}, died = {} where id = {}"
                                 .format(self.born, self.died, self.id) )

    def do_store( self ):
        self.cursor.execute( "insert into person (name, born, died) values (?, ?, ?)", 
		(self.name, self.born, self.died) )

class Score( DBItem ):
    def __init__(self, conn, genre, key, incipit, year):
        super().__init__(conn)
        self.genre = genre
        self.key = key
        self.incipit = incipit
        self.year = year

    def fetch_id(self):
        self.cursor.execute("select id from score where genre = ? and key = ? and incipit = ? and year = ?",
                            (self.genre, self.key, self.incipit, self.year))

        r = self.cursor.fetchone()
        if r is None:
            return
        self.id = r[0]
        
    def do_store(self):
        self.cursor.execute("insert into score (genre, key, incipit, year) values (?, ?, ?, ?)",
                            (self.genre, self.key, self.incipit, self.year))

class Voice( DBItem ):
    def __init__(self, conn, number, score, name):
        super().__init__(conn)
        self.number = number
        self.score = score
        self.name = name

    def fetch_id(self):
        self.cursor.execute("select id from voice where number = {} and score = {}"
                            .format(self.number, self.score))

        r = self.cursor.fetchone()
        if r is None:
            return
        self.id = r[0]

    def do_store(self):
        self.cursor.execute("insert into voice (number, score, name) values (?, ?, ?)",
                            (self.number, self.score, self.name))

class Edition(DBItem):
    def __init__(self,conn, score, name, year):
        super().__init__(conn)
        self.score = score
        self.name = name
        self.year = year

    def fetch_id(self):
        self.cursor.execute("select id from edition where score = {}"
                            .format(self.score))

        r = self.cursor.fetchone()
        if r is None:
            return
        self.id = r[0]

    def do_store(self):
        self.cursor.execute("insert into edition (score, name, year) values (?, ?, ?)",
                            (self.score, self.name, self.year))

class ScoreAuthor(DBItem):
    def __init__(self, conn, score, composer):
        super().__init__(conn)
        self.score = score
        self.composer = composer

    def fetch_id(self):
        self.cursor.execute("select id from score_author where score = {} and composer = {}"
                            .format(self.score,self.composer))

        r = self.cursor.fetchone()
        if r is None:
            return
        self.id = r[0]

    def do_store(self):
        self.cursor.execute("insert into score_author (score, composer) values (?, ?)",
                            (self.score, self.composer))

class EditionAuthor(DBItem):
    def __init__(self, conn, edition, editor):
        super().__init__(conn)
        self.edition = edition
        self.editor = editor

    def fetch_id(self):
        self.cursor.execute("select id from edition_author where edition = {} and editor ={}"
                            .format(self.edition, self.editor))

        r = self.cursor.fetchone()
        if r is None:
            return
        self.id = r[0]

    def do_store(self):
        self.cursor.execute("insert into edition_author (edition, editor) values (?, ?)",
                            (self.edition, self.editor))

class Print(DBItem):
    def __init__(self, conn, printNumber, partiture, edition):
        super().__init__(conn)
        self.partiture = 'N'
        if partiture is not None:
            if(partiture.lower() == 'yes'):
                self.partiture = 'Y'
            elif(partiture.lower() == 'partial'):
                 self.partiture = 'P'
        self.id = printNumber
        self.edition = edition

    def fetch_id(self):
        pass

    def do_store(self):
        if self.id is not None:
            self.cursor.execute("insert into print (id, partiture, edition) values (?, ?, ?)",
                            (self.id, self.partiture, self.edition))


