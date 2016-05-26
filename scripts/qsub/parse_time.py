#! /usr/bin/env python
import sys

with open(sys.argv[1], 'r') as f:
    t = 0.0
    for line in f:
        row = line.rstrip().split('\t')
        if row[0] == 'user' or row[0] == 'sys':
            a = row[1].find('m')
            b = row[1].find('s')
            t += 60 * float(row[1][:a]) + float(row[1][a+1:b])

            if row[0] == 'sys':
                print(t)
                t = 0.0
