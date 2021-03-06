#! /usr/bin/env python3

import sys

with open(sys.argv[1], 'r') as f:
    with open(sys.argv[2], 'w') as f2:
        for line in f:
            if line[0] == '@':
                f2.write(line)
            else:
                row = line.rstrip().split('\t')

                l = len(row[10])
                row[10] = '#' * l

                f2.write('\t'.join(row) + '\n')
