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
        assert len(word.letters) == len(word.phonemes)
        # step each letter/phoneme over the input window
        for i in range(len(word.letters)):
            inputWindow = (0,) * ceil(0,)
            orepr = nn.outputRepresentation(phoneme)
            dataset.addSample( word.letters, orepr )
            
    return dataset

def main():
    # process command line options
    args = processOptions()

    # build network
    network = buildNetwork( len(nn.input_neurons), n_hidden_neurons, len(nn.output_neurons) )

    # get dataset
    dataset = datasetTop1000Words(network)

    # train network
    trainer = BackpropTrainer(network, dataset)
    for n in range(args['cycles']):
        print trainer.train()
    
    
    
def processOptions():
    parser = argparse.ArgumentParser(description='Generate neural network.')
    parser.add_argument('output', nargs=1, help='file in which to save neural network')
    return parser.parse_args()
    

    
if __name__ == '__main__':
    main()