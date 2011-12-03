#!/usr/bin/env python

import argparse
import cPickle as pickle
import scipy.io as io

def parseArgs():
    parser = argparse.ArgumentParser(description='Export NETwhisperer network to MAT file.')
    parser.add_argument('saved_network', type=argparse.FileType('r'))
    parser.add_argument('-o', '--matfile', dest="matfile", type=argparse.FileType('w'))
    return parser.parse_args()

def main():
    args = parseArgs()
    
    network = pickle.load(args.saved_network)
    
    print 'Exporting network to file %s.' % args.matfile.name
    
    mdict = {
        'training_errors': network.training_errors,
        'input_hidden_weights': network.getInputHiddenWeights(),
        'hidden_output_weights': network.getHiddenOutputWeights(),
        'output_thresholds': network.getOutputThresholds(),
        'hidden_thresholds': network.getHiddenThresholds()
    }
    io.savemat(args.matfile, mdict, oned_as='row')
    
if __name__ == '__main__':
    main()