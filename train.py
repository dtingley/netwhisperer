#!/usr/bin/env python

import sys
import string
import argparse
from itertools import *
import cPickle as pickle
import corpus
from network import Network

DEFAULT_N_HIDDEN_NEURONS = 120

def datasetDictionary(net):
    for w in corpus.top1000words:
        yield w.letters, w.phonemes

def datasetGeneratedText(net):
    letters = ''
    phonemes = ''
    for word in corpus.top1000words:
        letters += word.letters + ' '
        phonemes += word.phonemes + ' '
            
    return [corpus.Word(letters, phonemes, None, None)]

def parseArgs():
    parser = argparse.ArgumentParser(description='Train a NETwhisperer network.')
    parser.add_argument('outfile', type=argparse.FileType('w'))
    parser.add_argument('--dict', action='store_true', help='train against individual words in dictionary')
    parser.add_argument('-e', '--epochs', dest="n_epochs", type=int, default=10)
    parser.add_argument('-n', '--n-hidden-neurons', dest="n_hidden_neurons", type=int, default=DEFAULT_N_HIDDEN_NEURONS)
    parser.add_argument('-w', '--window-size', dest="window_size", type=int, default=7)
    return parser.parse_args()

def main():
    args = parseArgs()
        
    network = Network(args.window_size, (args.window_size-1)/2, args.n_hidden_neurons)
    if args.dict:
        print 'Training using individual words from top 1000 dictionary.'
        training_set = datasetDictionary(network)
    else:
        print 'Training using generated strings from dictionary.'
        training_set = datasetGeneratedText(network)

    print 'Your network is being trained..',
    def print_dot():
        print '%d..' % (network.n_trainings+1),
        sys.stdout.flush()
    network.train(training_set, args.n_epochs, callback=print_dot)
    
    pickle.dump(network, args.outfile)
        
if __name__ == '__main__':
    main()