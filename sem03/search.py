import json
import sqlite3
import sys

args = len(sys.argv)

if args != 2:
    raise Exception("1 arg")

name = sys.argv[1]

con = sqlite3.connect('scorelib.dat')
cur = con.cursor()
res = cur.execute("select person.name, score.name, print.id "
			"from person left join score_author on person.id=score_author.composer "
			"join score on score_author.score=score.id "
                        "join edition on edition.score = score.id "
                        "join print on print.edition = edition.id "
			"where person.name like ? order by person.name", ("%{}%".format(name),))

out = []
for row in res:
    d = {}
    d['Composer'] = row[0]
    d['Score'] = row[1]
    d['Print Number'] = row[2]
    
    out.append(d)

json.dump(out, sys.stdout, indent=2)
con.close()
