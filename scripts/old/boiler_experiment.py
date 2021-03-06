from __future__ import print_function

import argparse
import os
import sys
import errno
import shutil
from distutils.spawn import find_executable

parser = argparse.ArgumentParser()
parser.add_argument('--unpaired', metavar='path', type=str, nargs='+', help='Unpaired read inputs')
parser.add_argument('--m1', metavar='path', type=str, nargs='+', help='Mate 1 inputs')
parser.add_argument('--m2', metavar='path', type=str, nargs='+', help='Mate 2 inputs')
parser.add_argument('--gtf', metavar='path', type=str, help='GTF file from simulation', required=True)
parser.add_argument('--pro', metavar='path', type=str, help='PRO file from simulation', required=True)
parser.add_argument('--num-threads', type=int, default=1, help='# threads to use')
parser.add_argument('--output', metavar='path', type=str, help='Output directory', required=True)
parser.add_argument('--bt2-index', metavar='path', type=str, help='Prefix of Bowtie 2 index')
parser.add_argument('--hisat-index', metavar='path', type=str, help='Prefix of HISAT index')
parser.add_argument('--cufflinks', action='store_true', help='Run Cufflinks')
parser.add_argument('--stringtie', action='store_true', help='Run StringTie')
parser.add_argument('--tophat', action='store_true', help='Run TopHat')
parser.add_argument('--hisat', action='store_true', help='Run HISAT')
parser.add_argument('--htseq', action='store_true', help='Run htseq-count')
parser.add_argument('--featurecounts', action='store_true', help='Run featureCounts')
parser.add_argument('--compress', metavar='path', type=str, help='Path to compress.py', required=True)
parser.add_argument('--samtools-exe', metavar='path', type=str, help='Path to samtools')
parser.add_argument('--python3-exe', metavar='path', type=str, help='Path to python3')
parser.add_argument('--cufflinks-exe', metavar='path', type=str, help='Path to cufflinks')
parser.add_argument('--stringtie-exe', metavar='path', type=str, help='Path to stringtie')
parser.add_argument('--tophat-exe', metavar='path', type=str, help='Path to tophat')
parser.add_argument('--hisat-exe', metavar='path', type=str, help='Path to hisat')
parser.add_argument('--htseq-exe', metavar='path', type=str, help='Path to htseq-count')
parser.add_argument('--featurecounts-exe', metavar='path', type=str, help='Path to featureCounts')
args = parser.parse_args()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def exe(st, st_arg):
    if st_arg:
        assert os.path.exists(st_arg)
        return st_arg
    ex = find_executable(st)
    if not ex:
        raise RuntimeError("Could not find '%s'; please specify --%s-exe")
    return ex


def bt2_index():
    for ext in ['.1.bt2', '.2.bt2', '.3.bt2', '.4.bt2', '.rev.1.bt2', '.rev.2.bt2']:
        assert os.path.exists(args.bt2_index + ext)
    return args.bt2_index


def hisat_index():
    for ext in ['.1.bt2', '.2.bt2', '.3.bt2', '.4.bt2', '.5.bt2', '.6.bt2',
                '.rev.1.bt2', '.rev.2.bt2', '.rev.5.bt2', '.rev.6.bt2']:
        assert os.path.exists(args.hisat_index + ext)
    return args.hisat_index


def run(cmd):
    print(cmd, file=sys.stderr)
    os.system(cmd)


def run_boiler(odir):
    uncomp_dir = os.path.join(odir, 'uncompressed')
    al_out = os.path.join(uncomp_dir, 'accepted_hits.sam')
    comp_dir = os.path.join(odir, 'compressed')
    mkdir_p(comp_dir)
    imed_dir = os.path.join(odir, 'intermediate')
    imed_out = os.path.join(imed_dir, 'accepted_hits.sam')
    mkdir_p(imed_dir)

    print('Compressing with Boiler...', file=sys.stderr)
    boiler_out = os.path.join(comp_dir, 'accepted_hits.boiled')
    python_exe = exe('python3', args.python3_exe)
    out_sam = os.path.join(comp_dir, 'accepted_hits.sam')
    cmd = '%s --compress --decompress --compress-to %s --alignments %s --intermediate %s --out %s --binary --expand-to %s' %\
          (python_exe, args.compress, al_out, imed_out, boiler_out, out_sam)
    run(cmd)

    print('Making Boiler version file...', file=sys.stderr)
    run('%s %s --version > %s' % (python_exe, args.compress, os.path.join(args.output, 'tophat', 'boiler_version.txt')))

    sam_exe = exe('samtools', args.samtools_exe)

    for dr in [comp_dir, imed_dir]:
        print('Expanded sam to bam...', file=sys.stderr)
        unsort_bam = os.path.join(dr, 'accepted_hits_name_sorted.bam')
        cmd = '%s view -Sb %s > %s' % (sam_exe, out_sam, unsort_bam)
        run(cmd)

        print('Sorting bam...', file=sys.stderr)
        sort_bam_prefix = os.path.join(dr, 'accepted_hits')
        cmd = '%s sort %s %s' % (sam_exe, unsort_bam, sort_bam_prefix)
        run(cmd)


def run_tophat():
    if os.path.exists(os.path.join(args.output, 'tophat')):
        print('TopHat directory exists, skipping...', file=sys.stderr)
        return

    sam_exe = exe('samtools', args.samtools_exe)

    print('Running TopHat...', file=sys.stderr)
    cmd = exe('tophat', args.tophat_exe)
    odir = os.path.join(args.output, 'tophat', 'uncompressed')
    mkdir_p(odir)
    cmd += ' -o ' + odir
    if args.num_threads > 1:
        cmd += ' -p %d' % args.num_threads
    cmd += ' %s' % bt2_index()
    if args.unpaired:
        cmd += (' ' + ','.join(args.unpaired))
    if args.m1:
        cmd += (' ' + ','.join(args.m1))
        cmd += (' ' + ','.join(args.m2))
    run(cmd)

    print('Making TopHat version file...', file=sys.stderr)
    run('tophat --version > %s' % os.path.join(args.output, 'tophat', 'tophat_version.txt'))

    print('Running samtools...', file=sys.stderr)
    bam_out = os.path.join(odir, 'accepted_hits.bam')
    al_out = os.path.join(odir, 'accepted_hits.sam')
    cmd = '%s view -h %s > %s' % (sam_exe, bam_out, al_out)
    run(cmd)

    print('Name-sorting bam...', file=sys.stderr)
    cmd = '%s sort -n %s %s' % (sam_exe, bam_out, os.path.join(odir, 'accepted_hits_name_sorted'))
    run(cmd)

    print('Making samtools version file...', file=sys.stderr)
    run('%s 2> %s' % (sam_exe, os.path.join(args.output, 'tophat', 'samtools_version.txt')))

    run_boiler(os.path.join(args.output, 'tophat'))


def run_hisat():
    if os.path.exists(os.path.join(args.output, 'hisat')):
        print('HISAT directory exists, skipping...', file=sys.stderr)
        return

    sam_exe = exe('samtools', args.samtools_exe)

    print('Running HISAT...', file=sys.stderr)
    mkdir_p(os.path.join(args.output, 'hisat'))
    cmd = ex = exe('hisat', args.hisat_exe)
    cmd += ' -x %s' % hisat_index()
    if args.num_threads > 1:
        cmd += ' -p %d' % args.num_threads
    odir = os.path.join(args.output, 'hisat', 'uncompressed')
    mkdir_p(odir)
    al_out = os.path.join(odir, 'accepted_hits.sam')
    cmd += ' -S ' + al_out
    if args.unpaired:
        cmd += (' -u ' + ','.join(args.unpaired))
    if args.m1:
        cmd += (' -1 ' + ','.join(args.m1))
        cmd += (' -2 ' + ','.join(args.m2))
    run(cmd)

    print('Making HISAT version file...', file=sys.stderr)
    run('%s --version > %s' % (ex, os.path.join(args.output, 'tophat', 'hisat_version.txt')))

    print('Running samtools...', file=sys.stderr)
    bam_out = os.path.join(odir, 'accepted_hits.bam')
    cmd = '%s view -h %s > %s' % (sam_exe, bam_out, al_out)
    run(cmd)

    print('Name-sorting bam...', file=sys.stderr)
    cmd = '%s sort -n %s %s' % (sam_exe, bam_out, os.path.join(odir, 'accepted_hits_name_sorted'))
    run(cmd)

    print('Making samtools version file...', file=sys.stderr)
    run('%s 2> %s' % (sam_exe, os.path.join(args.output, 'tophat', 'samtools_version.txt')))

    run_boiler(os.path.join(args.output, 'hisat'))


def run_aligners():
    if not args.tophat and not args.hisat:
        raise RuntimeError("Must specify --tophat, --hisat or both")
    if args.tophat:
        if not args.bt2_index:
            raise RuntimeError('Must specify --bt2-index when --tophat is set')
        run_tophat()
    if args.hisat:
        if not args.hisat_index:
            raise RuntimeError('Must specify --hisat-index when --hisat is set')
        run_hisat()


def run_htseq(gtf, aligner):
    if os.path.exists(os.path.join(args.output, 'htseq_' + aligner)):
        print('HTSeq+%s directory exists, skipping...' % aligner, file=sys.stderr)
        return

    for comp in ['uncompressed', 'intermediate', 'compressed']:
        print('Running htseq-count on %s %s...' % (aligner, comp), file=sys.stderr)
        cmd = ex = exe('htseq-count', args.htseq_exe)
        odir = os.path.join(args.output, 'htseq_' + aligner, comp)
        mkdir_p(odir)
        cmd += ' -f bam -s no -m union'
        cmd += ' ' + os.path.join(args.output, aligner, comp, 'accepted_hits_name_sorted.bam')
        cmd += ' ' + gtf
        cmd += ' > ' + os.path.join(odir, 'counts.tsv')
        run(cmd)

        print('Making HTSeq version file...', file=sys.stderr)
        run('%s > %s' % (ex, os.path.join(odir, 'htseq_version.txt')))


def run_featurecounts(gtf, aligner):
    if os.path.exists(os.path.join(args.output, 'featurecounts_' + aligner)):
        print('featureCounts+%s directory exists, skipping...' % aligner, file=sys.stderr)
        return

    ex = exe('featureCounts', args.featurecounts_exe)
    for comp in ['uncompressed', 'intermediate', 'compressed']:
        in_bam = os.path.join(args.output, aligner, comp, 'accepted_hits_name_sorted.bam')
        odir = os.path.join(args.output, 'featurecounts_' + aligner, comp)
        mkdir_p(odir)
        for feat_arg, feat_name in zip(['', '-f'], ['gene', 'exon']):
            print('Running featureCounts on %s level on %s %s...' % (feat_name, aligner, comp), file=sys.stderr)
            out_tsv = os.path.join(odir, 'counts_%s.tsv' % feat_name)
            run('%s -M -O -p %s -a %s -o %s %s' % (ex, feat_arg, gtf, out_tsv, in_bam))

        print('Making featureCounts version file...', file=sys.stderr)
        run('%s -v 2> %s' % (ex, os.path.join(odir, 'featurecounts_version.txt')))


def run_cufflinks(aligner):
    if os.path.exists(os.path.join(args.output, 'cufflinks_' + aligner)):
        print('Cufflinks+%s directory exists, skipping...' % aligner, file=sys.stderr)
        return

    for comp in ['uncompressed', 'intermediate', 'compressed']:
        print('Running cufflinks on %s %s...' % (aligner, comp), file=sys.stderr)
        cmd = ex = exe('cufflinks', args.cufflinks_exe)
        odir = os.path.join(args.output, 'cufflinks_' + aligner, comp)
        cmd += ' -o ' + odir
        if args.num_threads > 1:
            cmd += ' -p %d' % args.num_threads
        cmd += ' ' + os.path.join(args.output, aligner, comp, 'accepted_hits.bam')
        run(cmd)

        print('Making Cufflinks version file...', file=sys.stderr)
        run('%s 2> %s' % (ex, os.path.join(odir, 'cufflinks_version.txt')))


def run_stringtie(aligner):
    if os.path.exists(os.path.join(args.output, 'stringtie_' + aligner)):
        print('StringTie+%s directory exists, skipping...' % aligner, file=sys.stderr)
        return

    for comp in ['uncompressed', 'intermediate', 'compressed']:
        print('Running stringtie on %s %s...' % (aligner, comp), file=sys.stderr)
        cmd = ex = exe('stringtie', args.stringtie_exe)
        odir = os.path.join(args.output, 'stringtie_' + aligner, comp)
        cmd += ' ' + os.path.join(args.output, aligner, comp, 'accepted_hits.bam')
        mkdir_p(odir)
        if args.num_threads > 1:
            cmd += ' -p %d' % args.num_threads
        cmd += ' -o ' + os.path.join(odir, 'stringtie.gtf')
        run(cmd)

        print('Making StringTie version file...', file=sys.stderr)
        run('%s 2> %s' % (ex, os.path.join(odir, 'stringtie_version.txt')))


def run_counters(gtf):
    if args.htseq:
        if args.tophat:
            run_htseq(gtf, 'tophat')
        if args.hisat:
            run_htseq(gtf, 'hisat')
    if args.featurecounts:
        if args.tophat:
            run_featurecounts(gtf, 'tophat')
        if args.hisat:
            run_featurecounts(gtf, 'hisat')


def run_assemblers():
    if args.cufflinks:
        if args.tophat:
            run_cufflinks('tophat')
        if args.hisat:
            run_cufflinks('hisat')
    if args.stringtie:
        if args.tophat:
            run_stringtie('tophat')
        if args.hisat:
            run_stringtie('hisat')


if __name__ == "__main__":
    if args.unpaired is None and args.m1 is None:
        raise RuntimeError('Must specify --unpaired or --m1/--m2')
    mkdir_p(args.output)
    if args.unpaired is not None:
        for fn in args.unpaired:
            shutil.copy(fn, args.output)
    if args.m1 is not None:
        for fn in args.m1:
            shutil.copy(fn, args.output)
        for fn in args.m2:
            shutil.copy(fn, args.output)
    shutil.copy(args.gtf, args.output)
    shutil.copy(args.pro, args.output)
    run_aligners()
    run_counters(args.gtf)
    run_assemblers()
