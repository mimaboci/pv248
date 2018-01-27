import json
import sqlite3
import sys

args = len(sys.argv)

if args != 2:
    raise Exception("1 arg")

printId = sys.argv[1]

con = sqlite3.connect('scorelib.dat')
cur = con.cursor()
cur.execute("select person.name "
			"from print join edition join score_author join score join person "
            "on print.edition = edition.id "
            "and edition.score = score.id "
            "and score_author.score = score.id "
            "and score_author.composer = person.id "
            "where print.id = ?", printId)

composers = []

for row in cur:
    composers.append(row)

json.dump(composers, sys.stdout, indent=2)
con.close()
