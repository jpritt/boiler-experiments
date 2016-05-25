#! /usr/bin/env python3

import sys

with open(sys.argv[1], 'r') as f:
    with open(sys.argv[2], 'w') as f2:
        for line in f:
            if line[0] == '@':
                f2.write(line)
            else:
                row = line.rstrip().split('\t')
                flags = int(row[1])

                # Check for orphaned read
                if (flags & 8) and row[6] == '*':
                    row[1] = str(flags-8)

                f2.write('\t'.join(row) + '\n')
