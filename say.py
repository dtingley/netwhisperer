#!/usr/bin/env python

import subprocess
import sys
import argparse
import cPickle as pickle
import corpus
from network import Network
from to_espeak import to_espeak, getPhonemeMapping

def parseArgs():
    parser = argparse.ArgumentParser(description='Speak something using network from the NETwhisperer')
    parser.add_argument('saved_network', type=argparse.FileType('r'))
    return parser.parse_args()

def main():
    args = parseArgs()
    
    network = pickle.load(args.saved_network)
    
    print 'Type some text and the NETwhisperer will try to say it.'
    
    while 1:
        line = raw_input()
        if not line: break
        text = line.lower()
        speech = ''.join(network.lettersToPhonemes(text))
        espeech = to_espeak(speech)
        print 'Passing to espeak phoneme %s as %s' % (speech, espeech)
        subprocess.call('espeak ' + espeech, shell=True)

if __name__ == '__main__':
    main()