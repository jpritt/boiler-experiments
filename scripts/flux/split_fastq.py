#!/usr/bin/env python
import sys
import argparse

"""
Split the given fastq file into 2 files
"""

def split_paired_fastq(paired_reads, output_prefix):
    f1 = open(output_prefix + '_1.fastq', 'w')
    f2 = open(output_prefix + '_2.fastq', 'w')

    descriptor = paired_reads.readline().rstrip()
    while descriptor:
        if int(descriptor[-1]) == 1:
            outfile = f1
        else:
            outfile = f2

        outfile.write(descriptor + '\n')
        outfile.write(paired_reads.readline())
        outfile.write(paired_reads.readline())
        outfile.write(paired_reads.readline())

        descriptor = paired_reads.readline().rstrip()

    f1.close()
    f2.close()


if __name__ == '__main__':
    # Print file's docstring if -h is invoked
    parser = argparse.ArgumentParser(description=__doc__, 
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input-name', type=str, required=True, 
        help='Full path of fastq file containing paired end reads')
    parser.add_argument('--output-prefix', type=str, required=False, 
        help='Full path to location and prefix to write output file')

    args = parser.parse_args(sys.argv[1:])

    if args.output_prefix:
        output_prefix = args.output_prefix
    else:
        output_prefix = args.input_name.split('.')[0]

    with open(args.input_name) as paired_reads:
        split_paired_fastq(paired_reads, output_prefix)