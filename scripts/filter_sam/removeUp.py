#! /usr/bin/env python

import sys
import re

with open(sys.argv[1], 'r') as f:
  with open(sys.argv[2], 'w') as f2:
    for line in f:
      if line[0] == '@':
        f2.write(line)
      else:
        row = line.rstrip().split('\t')
        for i in range(11, len(row)):
          if row[i][:2] == 'YT':
            if row[i][5:] == 'UP':
              del row[i]
            break
        f2.write('\t'.join(row) + '\n')
