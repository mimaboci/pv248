import re
from collections import Counter

r1 = re.compile(r"Composer: (.*)")
r2 = re.compile(r"Composition Year: (.*)")
byComposer = Counter()

for line in open('scorelib.txt', 'r'):
    composer = r1.match(line)
    century = r2.match(line)
    if composer is not None:
        byComposer[composer.group(1)] += 1

for i,j in dict.items():
    print("{}: {}".format(i,j))
