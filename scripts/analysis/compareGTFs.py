#! /usr/bin/env python
import sys
from transcript import Transcript

'''
Compare a Cufflinks GTF file to the .pro output by flux
'''

def compareGTFs(truthGTF, compGTF):
    transcriptsTruth = dict()
    with open(truthGTF, 'r') as tsv:
        for line in tsv:
            row = line.strip().split('\t')
            if len(row) < 5:
                continue

            covIndex = row[8].find('cov')
            covStart = row[8].find('"', covIndex) + 1
            covEnd = row[8].find('"', covStart)
            cov = float(row[8][covStart:covEnd])

            transcriptIdIndex = row[8].find('transcript_id')
            transcriptIdStart = row[8].find('"', transcriptIdIndex) + 1
            transcriptIdEnd = row[8].find('"', transcriptIdStart)
            transcriptId = row[8][transcriptIdStart : transcriptIdEnd]

            if row[2] == 'transcript':
                transcriptsTruth[transcriptId] = Transcript(row[0], int(row[3]), int(row[4]), cov, transcriptId)
            elif row[2] == 'exon':
                transcriptsTruth[transcriptId].exons.append( (int(row[3]), int(row[4])) )

    transcriptsTruth = transcriptsTruth.values()

    transcriptsComp = dict()
    with open(compGTF, 'r') as tsv:
        for line in tsv:
            row = line.strip().split('\t')
            if len(row) < 5:
                continue

            covIndex = row[8].find('cov')
            covStart = row[8].find('"', covIndex) + 1
            covEnd = row[8].find('"', covStart)
            cov = float(row[8][covStart:covEnd])

            transcriptIdIndex = row[8].find('transcript_id')
            transcriptIdStart = row[8].find('"', transcriptIdIndex) + 1
            transcriptIdEnd = row[8].find('"', transcriptIdStart)
            transcriptId = row[8][transcriptIdStart : transcriptIdEnd]

            if row[2] == 'transcript':
                transcriptsComp[transcriptId] = Transcript(row[0], int(row[3]), int(row[4]), cov, transcriptId)
            elif row[2] == 'exon':
                transcriptsComp[transcriptId].exons.append( (int(row[3]), int(row[4])) )

    transcriptsComp = transcriptsComp.values()

    compareAll(transcriptsTruth, transcriptsComp)

def parsePro(filename):
    ''' Return a dictionary with transcript id (e.g. 0300689) pointing to coverage level
    '''
    transcripts = dict()
    with open(filename, 'r') as f:
        for line in f:
            row = line.strip().split('\t')
            if len(row) < 8:
                continue

            tag = row[1]
            sep1 = row[0].find(':')
            sep2 = row[0].find('-', sep1)
            sep3 = row[0].find('W', sep2)
            chrom = row[0][:sep1]
            start = int(row[0][sep1+1:sep2])
            end = int(row[0][sep2+1:sep3])
            fraction = float(row[8])
            transcripts[tag] = Transcript(chrom, start, end, fraction, tag)
    return transcripts


def compareAll(transcriptsTrue, transcriptsPredicted):
    ''' Compare 
    '''
    
    totalScore = 0.0
    threshold = 10

    transcriptsTrueCount = 0
    line = 0
    for t1 in transcriptsTrue:
        line += 1

        if t1.cov < .000001:
            continue


        closestScore = 0
        closestT = None
        
        for t2 in transcriptsPredicted:
            score = t1.scoreTranscript(t2, threshold)
            if score > closestScore:
                closestScore = score
                closestT = t2

        if weightByCov:
            if closestScore > 0:
                totalScore += closestScore * t1.cov
            transcriptsTrueCount += t1.cov
        else:
            if closestScore > 0:
                totalScore += closestScore
            transcriptsTrueCount += 1
    recall = float(totalScore) / float(transcriptsTrueCount)
    print('Recall    = TP/T = ' + str(recall))
    
    line = 0
    totalScore = 0
    transcriptsPredictedCount = 0
    for t1 in transcriptsPredicted:
        line += 1

        if t1.cov < .000001:
            continue


        closestScore = 0
        closestT = None
        
        for t2 in transcriptsTrue:
            score = t1.scoreTranscript(t2, threshold)
            if score > closestScore:
                closestScore = score
                closestT = t2

        if weightByCov:
            if closestScore > 0:
                totalScore += closestScore * t1.cov
            transcriptsPredictedCount += t1.cov
        else:
            if closestScore > 0:
                totalScore += closestScore
            transcriptsPredictedCount += 1
    precision = float(totalScore) / float(transcriptsPredictedCount)
    print('Precision    = TP/P = ' + str(precision))

weightByCov = False
if sys.argv[3] == '1':
    weightByCov = True
compareGTFs(sys.argv[1], sys.argv[2])

