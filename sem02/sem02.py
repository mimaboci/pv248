import sqlite3

con = sqlite3.connect('D:\School\School\_magister\python\scorelib.dat')
f = open('D:\School\School\_magister\python\scorelib.sql','r')
con.cursor().executescript(f.read())
con.commit()

f = open('D:\School\School\_magister\python\scorelib.txt','r')
r = re.compile(r"(.*): (.*)")
for line in f:
    m = r.match(line)
    if m is None: continue
    k = m.group(1)
    v = m.group(2)
    if k == 'Composer':
        for c in v.split(':'):
            p = Person(conn, c.strip())
            p.store()
            
    
con.commit()
