import json
import sqlite3
import sys

args = len(sys.argv)

if args != 2:
    raise Exception("1 arg")

name = sys.argv[1]

con = sqlite3.connect('scorelib.dat')
cur = con.cursor()
cur.execute("select person.name, score.name "
			"from score_author join score on score_author.score=score.id "
			"join person on person.id=score_author.composer "
			"where person.name like ? order by person.name", ("%{}%".format(name),))

scores = {}

for row in cur:

    if row[0] not in scores:
        scores[row[0]] = []

    scores[row[0]].append(row[1])

json.dump(scores, sys.stdout, indent=2)
