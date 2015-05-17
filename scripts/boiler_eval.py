from __future__ import print_function

"""
Given a directory with all the runs all the comparisons.
"""

import argparse
import os
import sys
import glob
import errno

parser = argparse.ArgumentParser()
parser.add_argument('--input', metavar='path', type=str, help='Directory with boiler_experiment.py results')
parser.add_argument('--boiler-dir', metavar='path', type=str, help='Directory with boiler and associated scripts')
args = parser.parse_args()

j = os.path.join


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def run(cmd):
    print(cmd, file=sys.stderr)
    os.system(cmd)


def run_kc(pro, gtf, ref, other_gtf, fastq, kmer):
    pass


def run_compare_to_truth(pro, gtf, other_gtf, odir, ofile):
    print('Running compare_to_truth for %s...' % odir, file=sys.stderr)
    cmd = ['python %s/compareToTruth.py' % args.boiler_dir]
    cmd.extend([pro, gtf, other_gtf])
    mkdir_p(odir)
    cmd.append(' >' + os.path.join(odir, ofile))
    run(' '.join(cmd))


def run_tripartite(pro, gtf, before_gtf, after_gtf, odir, ofile, strict=True):
    print('Running tripartite for %s...' % odir, file=sys.stderr)
    cmd = ['python %s/compareTripartite.py' % args.boiler_dir]
    cmd.extend([pro, gtf, before_gtf, after_gtf, '1' if strict else '0'])
    mkdir_p(odir)
    cmd.append(' >' + os.path.join(odir, ofile))
    run(' '.join(cmd))


if __name__ == "__main__":
    assert os.path.exists(args.input)
    assert os.path.exists(args.boiler_dir)
    gtf = glob.glob(os.path.join(args.input, '*.gtf'))[0]
    pro = glob.glob(os.path.join(args.input, '*.pro'))[0]
    for aligner in ['tophat', 'hisat']:
        for assembler in ['cufflinks', 'stringtie']:
            dr = j(args.input, assembler + '_' + aligner)
            if os.path.exists(dr):
                before_gtf = glob.glob(os.path.join(dr, 'uncompressed', '*.gtf'))[0]
                after_gtf = glob.glob(os.path.join(dr, 'compressed', '*.gtf'))[0]
                run_tripartite(pro, gtf, before_gtf, after_gtf, dr, 'tripartite_nonstrict.txt', strict=False)
                run_tripartite(pro, gtf, before_gtf, after_gtf, dr, 'tripartite_strict.txt', strict=True)
                run_compare_to_truth(pro, gtf, before_gtf, os.path.join(dr, 'uncompressed'), 'compare_to_truth.txt')
                run_compare_to_truth(pro, gtf, after_gtf, os.path.join(dr, 'compressed'), 'compare_to_truth.txt')
