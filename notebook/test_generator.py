import pytz
from pytz import UTC as utc
from datetime import datetime, timezone, timedelta
import os, time, json
import random
import subprocess
from django.utils.timezone import now

def inp():
    with open('/Users/polygon/Desktop/in.txt', 'w+') as f:
        t = random.randint(1, 1001)
        f.write(str(t) + '\n')
        tn = 50000
        for _ in range(t):
            n = random.randint(1, max(tn - _, 2)) * 2
            tn -= n
            f.write(str(n) + '\n')
            l1 = '0' * (n // 2)
            l2 = '1' * (n // 2)
            r = l1 + l2
            f.write(''.join(random.sample(r, len(r))) + '\n')


def out():
    os.chdir('/Users/polygon/Desktop')

    # os.system('python add.py < in.txt > out.txt')
    with open('/Users/polygon/Desktop/in.txt', 'r') as f1, open('/Users/polygon/Desktop/out.txt', 'w+') as f2:
        s = time.time()
        # os.system('time ./add < in.txt > out.txt')
        r = subprocess.run(['python', 'add.py'],
                           stdin=f1,
                           stdout=f2,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           )
        print(r.stderr.split('  '))
        e = time.time()
        print((e - s))