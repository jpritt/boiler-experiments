#! /usr/bin/env python3

import sys
import re

nts = ['A', 'C', 'G', 'T']
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

                seq = list(row[9])

                for i in range(11, len(row)):
                    if row[i][:5] == 'MD:Z:':
                        MD = row[i][5:]
                        pos = 0
                        match = re.search("\D", MD)
                        while match:
                            index = match.start()
                            if index > 0:
                                pos += int(MD[:index])
                            if MD[index] == '^':
                                index += 1
                                seq = seq[:pos] + [MD[index]] + seq[pos:]
                                pos += 1
                            elif MD[index] in nts:
                                seq[pos] = MD[index]
                            else:
                                print(row[i])
                                exit()

                            MD = MD[index+1:]
                            match = re.search("\D", MD)
                        
                        row[i] = 'MD:Z:' + str(len(seq))
                        row[9] = ''.join(seq)
                        break
                f2.write('\t'.join(row) + '\n')
