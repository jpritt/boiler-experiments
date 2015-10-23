#! /usr/bin/env python3
import sys

'''
Replaces all read names with simple integers

Usage: ./remove_read_names.py input.sam output.sam
'''

with open(sys.argv[1], 'r') as f_in:
    with open(sys.argv[2], 'w') as f_out:
        read_names = []

        for line in f_in:
            row = line.rstrip().split('\t')
            if len(row) < 6:
                f_out.write(line)
            else:
                name = row[0]
                found = False
                for i in range(len(read_names)):
                    if read_names[i] == name:
                        row[0] = str(i)
                        found = True
                if not found:
                    row[0] = str(len(read_names))
                    read_names.append(name)
                f_out.write('\t'.join(row) + '\n')