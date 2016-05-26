#!/usr/bin/env python
import sys
import argparse
import random

"""
Split the given fastq file into 2 files
"""

def split_replicates(input, dir_prefix, num, split_random, prob):
    with open(input, 'r') as f:
        output = []
        for i in range(num):
            output.append([open(dir_prefix+str(i)+'/reads1.fastq', 'w'), open(dir_prefix+str(i)+'/reads2.fastq', 'w')])

        i = 0
        descriptor1 = f.readline()
        while descriptor1:
            for _ in range(3):
                descriptor1 += f.readline()
            descriptor2 = ''
            for _ in range(4):
                descriptor2 += f.readline()

            if split_random:
                for id in range(num):
                    if random.random() < prob:
                        output[id][0].write(descriptor1)
                        output[id][1].write(descriptor2)
            else:
                output[i][0].write(descriptor1)
                output[i][1].write(descriptor2)
                i = (i+1) % num

            descriptor1 = f.readline()

        for i in range(num):
            output[i][0].close()
            output[i][1].close()

if __name__ == '__main__':
    # Print file's docstring if -h is invoked
    parser = argparse.ArgumentParser(description=__doc__, 
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input-fastq', type=str, required=True, 
        help='Full path of fastq file containing paired end reads')
    parser.add_argument('--output-dir', type=str, required=True, 
        help='Full path to location and prefix to write output file')
    parser.add_argument('--n', type=int, required=True, help='Number of files to split into')
    parser.add_argument('--random', action='store_true', help='Assign each read to each file with probability specified by --prob')
    parser.add_argument('--prob', type=float, required=False, help='If random flag is set, assign each read to each file with this probability')

    args = parser.parse_args(sys.argv[1:])

    if args.random and not args.prob:
        args.prob = 1.0 / float(args.n)
    split_replicates(args.input_fastq, args.output_dir, args.n, args.random, args.prob)
