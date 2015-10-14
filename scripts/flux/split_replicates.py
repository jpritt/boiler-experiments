#!/usr/bin/env python
import sys
import argparse
import random

"""
Split the given fastq file into 2 files
"""

def split_replicates(reads1, reads2, output_prefix):
    lines1 = []
    lines2 = []

    descriptor = reads1.readline().rstrip()
    while descriptor:
        lines1 += [descriptor + '\n' + reads1.readline() + reads1.readline() + reads1.readline()]
        lines2 += [reads2.readline() + reads2.readline() + reads2.readline() + reads2.readline()]

        descriptor = reads1.readline().rstrip()


    len1 = len(lines1) / 2
    order = [0] * len1 + [1] * (len(lines1)-len1)
    random.shuffle(order)

    f1_1 = open(output_prefix + '1_1.fastq', 'w')
    f1_2 = open(output_prefix + '1_2.fastq', 'w')
    f2_1 = open(output_prefix + '2_1.fastq', 'w')
    f2_2 = open(output_prefix + '2_2.fastq', 'w')

    for i in xrange(len(order)):
        if (order[i] == 0):
            f1_1.write(lines1[i])
            f1_2.write(lines2[i])
        else:
            f2_1.write(lines1[i])
            f2_2.write(lines2[i])


    f1_1.close()
    f1_2.close()
    f2_1.close()
    f2_2.close()


if __name__ == '__main__':
    # Print file's docstring if -h is invoked
    parser = argparse.ArgumentParser(description=__doc__, 
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input-prefix', type=str, required=True, 
        help='Full path of fastq file containing paired end reads')
    parser.add_argument('--output-prefix', type=str, required=False, 
        help='Full path to location and prefix to write output file')

    args = parser.parse_args(sys.argv[1:])

    if args.output_prefix:
        output_prefix = args.output_prefix
    else:
        output_prefix = args.input_name.split('.')[0]

    with open(args.input_prefix + '_1.fastq') as reads1:
        with open(args.input_prefix + '_2.fastq') as reads2:
            split_replicates(reads1, reads2, output_prefix)