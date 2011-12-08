#!/usr/bin/env python

from itertools import *
import argparse
import cPickle as pickle
import scipy.io as io
import corpus

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
    for w in corpus.top1000words:
        res = network.lettersToPhonemesWithAngles(w.letters, w.phonemes)
        pph, angs = izip(*res)
        
        inputs.extend(w.letters)
        correct_outputs.extend(w.phonemes)
        produced_outputs.extend(pph)
        angles.extend(angs)
        total += len(w.letters)
        correct += sum(int(a==b) for a,b in izip(pph, w.phonemes))
    
    percent_correct = 100.0 * correct / total
    mdict = {
        'percent_correct': percent_correct,
        'inputs': inputs,
        'correct_outputs': correct_outputs,
        'produced_outputs': produced_outputs,
        'angles': angles,  
    }
    if (args.matfile):
        io.savemat(args.matfile, mdict, oned_as='row')
    print '%f%% correct' % percent_correct
    
if __name__ == '__main__':
    main()