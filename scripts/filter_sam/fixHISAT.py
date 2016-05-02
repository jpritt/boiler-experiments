#! /usr/bin/env python3

import sys
import re
import random

with open(sys.argv[1], 'r') as f:
    with open(sys.argv[2], 'w') as f2:
        lastName = None
        last = []
        for line in f:
            row = line.rstrip().split('\t')
            if line[0] == '@':
                f2.write(line)
            else:
                if not row[0] == lastName:
                    lastName = row[0]
                    last = []
                if row[5] == '*':
                    if row[2] == '*' and row[3] == '0' and row[4] == '0':
                        continue
                    else:
                        found = False
                        for r in last:
                            if row[2] == r[2] and row[3] == r[3] and row[6] == r[6] and row[7] == r[7]:
                                found = True
                                row[5] = r[5]
                                f2.write('\t'.join(row) + '\n')
                                break
                        if not found:
                            print(row[0])
                            exit()
                else:
                    f2.write(line)
                last.append(row)
