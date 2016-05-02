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
                row[10] = '#' * len(row[10])
                #row[0] = '0'
                #row[1] = '0'
                #row[4] = '0'
                #row[9] = '*'
                #row[10] = '*'
                f2.write('\t'.join(row) + '\n')

