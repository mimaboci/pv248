import re
from collections import Counter

f = open('scorelib.txt', 'r', encoding='utf8')
r1 = re.compile(r"Composer: (.*)")
r2 = re.compile(r"Composition Year: (.*)")
r3 = re.compile(r"Key: (.*)")
r4 = re.compile(r"Voice (.): (.*), (.*), (.*)")
byComposer = Counter()
byCentury = Counter()
byKey = Counter()
byInstrument = Counter()

def convertToCentury(year):
    try:
        century = (int(year) // 100) + 1
        return century
    except (TypeError, ValueError):
        return None

def printByComposer():
    f.seek(0,0)
    for line in f:
        composer = r1.match(line)
        if composer is not None:
            byComposer[composer.group(1)] += 1
    for i,j in byComposer.items():
        if(i is not None):
            print("{}: {}".format(i,j))

def printByCentury():
    f.seek(0,0)
    for line in f:
        year = r2.match(line)
        if year is not None:
            century = convertToCentury(year.group(1))
            byCentury[century] += 1
    for i,j in byCentury.items():
        if(i is not None):
            print("{}: {}".format(i,j))

def printByKey():
    f.seek(0,0)
    for line in f:
        key = r3.match(line)
        if key is not None:
            byKey[key.group(1)] += 1
    for i,j in byKey.items():
        if(i is not None):
            print("{}: {}".format(i,j))
 
def printByInstrument():
    f.seek(0,0)
    for line in f:
        voice = r4.match(line)
        if voice is not None:
            byInstrument[voice.group(3)] += 1
    for i,j in byInstrument.items():
        if(i is not None):
            print("{}: {}".format(i,j))
