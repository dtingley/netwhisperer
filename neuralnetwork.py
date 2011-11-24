from itertools import *
from numpy import array, zeros, dot, arccos
from numpy.linalg import norm
import corpus

######### THESE SHOULD BE CONFIGURATION OPTIONS
# look at 7 letters at once
window_size = 7
# zero-indexed middle of window
window_middle = 3
######### 

# one neuron for each window/letter combination
letter_neuron_names = list( product( corpus.all_letters, range(window_size) ) )

# mapping from (letter, pos) to input neuron index
letters_to_neurons = dict(
    {(letter_and_pos, index) for index, letter_and_pos in enumerate(letter_neuron_names)}
)

def windowIter(letters):
    assert type(letters) == str
    padding_before = ' ' * window_middle
    padding_after = ' ' * (window_size - window_middle - 1)
    padded_letters = padding_before + letters + padding_after
    # for each letter in the sample
    for l_num in range(len(letters)):
        letters_window = padded_letters[l_num:l_num+window_size]
        yield letters_window

def letters_to_layer(letters):
    assert len(letters) == window_size
    # start with empty layer
    layer = zeros(len(letter_neuron_names))
    # loop through letters and activate each neuron
    for (pos, letter) in enumerate(letters):
        index = letters_to_neurons[(letter, pos)]
        layer[index] = 1
    return layer

# one neuron for each phoneme trait
phoneme_trait_neuron_names = list(corpus.all_phoneme_traits)

# mapping from trait to neuron
traits_to_neurons = dict(
    {(trait, index) for index, trait in enumerate(phoneme_trait_neuron_names)}
)

# mapping from phoneme to layer
phonemes_to_layers = {}
for (phoneme, traits) in corpus.phoneme_traits.iteritems():
    layer = zeros(len(phoneme_trait_neuron_names))
    for trait in traits:
        index = traits_to_neurons[trait]
        layer[index] = 1
    phonemes_to_layers[phoneme] = layer

# reverse the mapping
#layers_to_phonemes = dict({(l,p) for p,l in phonemes_to_layers.iteritems()})

def phoneme_to_layer(phoneme):
    return phonemes_to_layers[phoneme]

def layer_to_phoneme(layer):
    def cos_to_input(item):
        phoneme, phoneme_layer = item
        return dot(layer,phoneme_layer) / norm(layer) / norm(phoneme_layer)
    # minimum angle should be maximum cos    
    return max(phonemes_to_layers.iteritems(), key=cos_to_input)[0]

def wordSamples(word):
    assert len(word.letters) == len(word.phonemes)
    for (letters_window, current_phoneme) in izip(windowIter(word.letters), word.phonemes):
        yield letters_to_layer(letters_window), phoneme_to_layer(current_phoneme)        
            