#!/usr/bin/env python

from itertools import *
import argparse
import cPickle as pickle
import scipy.io as io
import corpus
import sys

def parseArgs():
    parser = argparse.ArgumentParser(description='Test NETwhisperer network against full dictionary.')
    parser.add_argument('saved_network', type=argparse.FileType('r'))
    parser.add_argument('-o', '--matfile', dest="matfile", type=argparse.FileType('w'))
    return parser.parse_args()

def main():
    args = parseArgs()
    
    network = pickle.load(args.saved_network)
    
    print 'Testing against full dictionary...',
    
    total = 0
    correct = 0
    inputs = []
    correct_outputs = []
    produced_outputs = []
    angles = []
    for (i, w) in enumerate(corpus.dictionary.values()):
        if not i % 1000:
            print '%d..' % (i+1),
            sys.stdout.flush()
        
        # skip French phoneme that wasn't in original corpus
        if '+' in w.phonemes: continue
        res = network.lettersToPhonemesWithAngles(w.letters, w.phonemes)
        pph, angs = izip(*res)
        
        if args.matfile:
            inputs.extend(w.letters)
            correct_outputs.extend(w.phonemes)
            produced_outputs.extend(pph)
            angles.extend(angs)
        total += len(w.letters)
        correct += sum(int(a==b) for a,b in izip(pph, w.phonemes))
    
    percent_correct = 100.0 * correct / total
    if args.matfile:
        mdict = {
            'percent_correct': percent_correct,
            'inputs': inputs,
            'correct_outputs': correct_outputs,
            'produced_outputs': produced_outputs,
            'angles': angles,  
        }
        io.savemat(args.matfile, mdict, oned_as='row')
    print '%f%% correct' % percent_correct
    
if __name__ == '__main__':
    main()