#!/usr/bin/env python

# This script generates a PyBrain neural network given input parameters.
# Usage:
#   generate.py trainingDictionary nPasses networkOutput

import argparse
import string
from itertools import *
import cPickle as pickle
from pybrain.datasets            import SupervisedDataSet
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import corpus
import neuralnetwork as nn

n_hidden_neurons = 120

def datasetTop1000Words():
    # build data set    
    dataset = SupervisedDataSet( len(nn.input_neurons), len(nn.output_neurons) )
    for word in corpus.top1000words:
        for sample in nn.wordSamples(word):
            dataset.addSample(*sample)
            
    return dataset

def main():
    # process command line options
    args = processOptions()

    # build network
    network = buildNetwork( len(nn.input_neurons), n_hidden_neurons, len(nn.output_neurons) )

    # get dataset
    dataset = datasetTop1000Words()

    # train network
    trainer = BackpropTrainer(network, dataset)
    for n in range(args['n_epochs']):
        print trainer.train()
    
    pickle.dump(net1, open(args['output'], 'w'))
    
def processOptions():
    parser = argparse.ArgumentParser(description='Generate neural network.')
    parser.add_argument('output', nargs=1, help='file in which to save neural network')
    return parser.parse_args()
    

    
if __name__ == '__main__':
    main()