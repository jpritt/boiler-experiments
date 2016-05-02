#! /usr/bin/env python3

import sys
import re
import random

#name_map = dict()
#i = 0
with open(sys.argv[1], 'r') as f:
    with open(sys.argv[2], 'w') as f2:
        for line in f:
            if line[0] == '@':
                f2.write(line)
            else:
                row = line.rstrip().split('\t')
                #if row[0] in name_map:
                #    row[0] = name_map[row[0]]
                #else:
                #    name_map[row[0]] = str(i)
                #    row[0] = str(i)
                #    i += 1
                row[0] = '0'
                #row[9] = '*'
                #row[10] = '*'
                f2.write('\t'.join(row) + '\n')

