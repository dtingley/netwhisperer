#!/usr/bin/env python

import sys
import argparse
import cPickle as pickle
import corpus
from network import Network

def parseArgs():
    parser = argparse.ArgumentParser(description='Test NETwhisperer with input.')
    parser.add_argument('saved_network', type=argparse.FileType('r'))
    return parser.parse_args()

def main():
    args = parseArgs()
    
    network = pickle.load(args.saved_network)
    
    print 'Type some text and the NETwhisperer will try and convert it to phonemes. Press return on an empty line to end.'
    
    while 1:
        line = raw_input()
        if not line: break
        
        phonemes = ''
        for window in network.windowIter(line):
            input_layer = network.letters_to_layer(window)
            output_layer = network.pybrain_network.activate(input_layer)
            phoneme = network.layer_to_phoneme(output_layer)
            phonemes += phoneme
        print phonemes

if __name__ == '__main__':
    main()