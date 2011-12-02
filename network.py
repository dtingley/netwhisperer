from itertools import *
from numpy import array, zeros, dot, arccos
from numpy.linalg import norm

from pybrain.structure.networks.feedforward import FeedForwardNetwork
from pybrain.structure.modules import BiasUnit, SigmoidLayer, LinearLayer
from pybrain.structure.connections import FullConnection
from pybrain.datasets import SupervisedDataSet as DataSet
from pybrain.supervised.trainers import BackpropTrainer as Trainer

import corpus

class Network:
    "NETwhisperer neural network"
    
    def phoneme_to_layer(self, phoneme):
        return self.phonemes_to_layers[phoneme]

    def layer_to_phoneme(self, layer):
        def cos_to_input(item):
            phoneme, phoneme_layer = item
            return dot(layer,phoneme_layer) / norm(layer) / norm(phoneme_layer)
        # minimum angle should be maximum cos    
        return max(self.phonemes_to_layers.iteritems(), key=cos_to_input)[0]    

    def __init__(self, window_size, window_middle, n_hidden_neurons):
        self.window_size = window_size
        self.window_middle = window_middle
        self.n_hidden_neurons = n_hidden_neurons
        self.n_trainings = 0
        self.training_errors = []
        self._init_layers()
        self._generate_pybrain_network()
        
    def _init_layers(self):
        # one neuron for each window/letter combination
        self.letter_neuron_names = list(product(corpus.all_letters, range(self.window_size)))
        # one neuron for each phoneme trait
        self.phoneme_trait_neuron_names = list(corpus.all_phoneme_traits)
        # neuron counts
        self.n_input_neurons = len(self.letter_neuron_names)
        self.n_output_neurons = len(self.phoneme_trait_neuron_names)        
        # mapping from (letter, pos) to input neuron index
        self.letters_to_neurons = dict({(letter_and_pos, index) for index, letter_and_pos in enumerate(self.letter_neuron_names)})
        # mapping from trait to neuron
        self.traits_to_neurons = dict({(trait, index) for index, trait in enumerate(self.phoneme_trait_neuron_names)})
        # mapping from phoneme to layer
        self.phonemes_to_layers = {}
        for (phoneme, traits) in corpus.phoneme_traits.iteritems():
            layer = zeros(self.n_output_neurons)
            for trait in traits:
                index = self.traits_to_neurons[trait]
                layer[index] = 1
            self.phonemes_to_layers[phoneme] = layer
            
    def _generate_pybrain_network(self):
        # make network
        self._pybrain_network = FeedForwardNetwork()
        # make layers
        self._in_layer = LinearLayer(self.n_input_neurons, name='in')
        self._hidden_layer = SigmoidLayer(self.n_hidden_neurons, name='hidden')
        self._out_layer = LinearLayer(self.n_output_neurons, name='out')
        self._bias_neuron = BiasUnit(name='bias')
        # make connections between layers
        self._in_hidden_connection = FullConnection(self._in_layer, self._hidden_layer)
        self._hidden_out_connection = FullConnection(self._hidden_layer, self._out_layer)
        self._bias_hidden_connection = FullConnection(self._bias_neuron, self._hidden_layer)
        self._bias_out_connection = FullConnection(self._bias_neuron, self._out_layer)
        # add modules to network
        self._pybrain_network.addInputModule(self._in_layer)
        self._pybrain_network.addModule(self._hidden_layer)
        self._pybrain_network.addOutputModule(self._out_layer)
        self._pybrain_network.addModule(self._bias_neuron)
        # add connections to network
        for c in (self._in_hidden_connection, self._hidden_out_connection, self._bias_hidden_connection, self._bias_out_connection):
            self._pybrain_network.addConnection(c)
        # initialize network with added modules/connections
        self._pybrain_network.sortModules()

    def windowIter(self, letters):
        assert type(letters) == str
        padding_before = ' ' * self.window_middle
        padding_after = ' ' * (self.window_size - self.window_middle - 1)
        padded_letters = padding_before + letters + padding_after
        # for each letter in the sample
        for l_num in range(len(letters)):
            letters_window = padded_letters[l_num:l_num+self.window_size]
            yield letters_window    

    def generateSamples(self, letters, phonemes):
        assert len(letters) == len(phonemes)
        for (letters_window, current_phoneme) in izip(self.windowIter(letters), phonemes):
            yield self.letters_to_layer(letters_window), self.phoneme_to_layer(current_phoneme)

    def letters_to_layer(self, letters):
        assert len(letters) == self.window_size
        # start with empty layer
        layer = zeros(self.n_input_neurons)
        # loop through letters and activate each neuron
        for (pos, letter) in enumerate(letters):
            index = self.letters_to_neurons[(letter, pos)]
            layer[index] = 1
        return layer
        
    def train(self, training_set, n_epochs=1, callback=None):
        # build dataset
        dataset = DataSet(self.n_input_neurons, self.n_output_neurons)
        for (ltr,ph) in training_set:
            for sample in self.generateSamples(ltr,ph):
                dataset.addSample(*sample)
        # build trainer
        trainer = Trainer(self._pybrain_network, dataset, 0.01, 1.0, 0.9)
        for i in xrange(n_epochs):
            # run callback if present
            if callback: callback()
            # train network
            error = trainer.train()
            # record training errors
            self.n_trainings = self.n_trainings + 1
            self.training_errors.append(error)
            
    def getInputHiddenWeights(self):
        return self._in_hidden_connection.params.reshape((self.n_hidden_neurons, self.n_input_neurons))
        
    def getHiddenOutputWeights(self):
        return self._hidden_out_connection.params.reshape((self.n_output_neurons, self.n_hidden_neurons))

    def getHiddenThresholds(self):
        return self._bias_hidden_connection.params
        
    def getOutputThresholds(self):
        return self._bias_out_connection.params
        
    def lettersToPhonemes(self, letters):
        for window in self.windowIter(letters):
            input_layer = self.letters_to_layer(window)
            output_layer = self._pybrain_network.activate(input_layer)
            phoneme = self.layer_to_phoneme(output_layer)
            yield phoneme
