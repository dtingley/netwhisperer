from itertools import *
from numpy import array, zeros, dot, arccos
from numpy.linalg import norm
from pybrain.tools.shortcuts import buildNetwork
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
        return max(phonemes_to_layers.iteritems(), key=cos_to_input)[0]    

    def __init__(self, window_size, window_middle, n_hidden_neurons):
        self.window_size = window_size
        self.window_middle = window_middle
        self.n_hidden_neurons = n_hidden_neurons
        self._init_layers()
        self.pybrain_network = buildNetwork(self.n_input_neurons, self.n_hidden_neurons, self.n_output_neurons)
        
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

    def windowIter(self, letters):
        assert type(letters) == str
        padding_before = ' ' * self.window_middle
        padding_after = ' ' * (self.window_size - self.window_middle - 1)
        padded_letters = padding_before + letters + padding_after
        # for each letter in the sample
        for l_num in range(len(letters)):
            letters_window = padded_letters[l_num:l_num+self.window_size]
            yield letters_window    

    def wordSamples(self, word):
        assert len(word.letters) == len(word.phonemes)
        for (letters_window, current_phoneme) in izip(self.windowIter(word.letters), word.phonemes):
            yield self._letters_to_layer(letters_window), self.phoneme_to_layer(current_phoneme)

    def _letters_to_layer(self, letters):
        assert len(letters) == self.window_size
        # start with empty layer
        layer = zeros(self.n_input_neurons)
        # loop through letters and activate each neuron
        for (pos, letter) in enumerate(letters):
            index = self.letters_to_neurons[(letter, pos)]
            layer[index] = 1
        return layer



     
            