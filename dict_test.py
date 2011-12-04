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
    for w in corpus.top1000words:
        produced_phonemes = network.lettersToPhonemes(w.letters)
        total += len(w.letters)
        correct += sum(int(a==b) for a,b in izip(produced_phonemes, w.phonemes))
    
    percent_correct = 100.0 * correct / total
    if (args.matfile):
        io.savemat(args.matfile, {'percent_correct':percent_correct}, oned_as='row')
    print '%f%% correct' % percent_correct
    
if __name__ == '__main__':
    main()