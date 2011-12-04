#!/usr/bin/env python

from itertools import *
import argparse
import cPickle as pickle
import scipy.io as io
from numpy import random
import corpus

def parseArgs():
    parser = argparse.ArgumentParser(description='Damage network with random weights')
    parser.add_argument('saved_network', type=argparse.FileType('r'))
    parser.add_argument('-o', dest="damaged_network", type=argparse.FileType('w'))    
    parser.add_argument('-d', '--damage', dest="d", type=float)
    return parser.parse_args()

def main():
    args = parseArgs()
    
    network = pickle.load(args.saved_network)
    
    print 'Damaging network...',
    def rand_fn():
        damage = random.uniform(-args.d, args.d)
        print "%f.." % damage,
        return damage
    network.addRandomWeights(rand_fn)
    
    pickle.dump(network, args.damaged_network)
    
if __name__ == '__main__':
    main()