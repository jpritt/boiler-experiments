#! /usr/bin/env python3
import sys

'''
Replaces all read names with simple integers

Usage: ./remove_read_names.py input.sam output.sam
'''

with open(sys.argv[1], 'r') as f_in:
    with open(sys.argv[2], 'w') as f_out:
        i = 0
        for line in f_in:
            row = line.rstrip().split('\t')
            if len(row) < 6:
                f_out.write(line)
            else:
                row[0] = str(i)
                f_out.write('\t'.join(row) + '\n')
                #i += 1
