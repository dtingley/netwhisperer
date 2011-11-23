from itertools import *
import corpus

# look at 7 letters at once
window_size = 7
# zero-indexed middle of window
window_middle = 3
# one neuron for each window/letter combination
input_neurons = list( product( range(window_size), corpus.letters ) )
# one neuron for each phoneme
output_neurons = corpus.phonemes
