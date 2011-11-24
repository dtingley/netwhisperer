from itertools import *
import corpus

# look at 7 letters at once
window_size = 7
# zero-indexed middle of window
window_middle = 3
# one neuron for each window/letter combination
input_neurons = list( product( corpus.all_letters, range(window_size) ) )
empty_input = (0,) * len(input_neurons)
# mapping from (letter, pos) to input neuron index
letters_to_neurons = dict({(letter_and_pos, index) for index, letter_and_pos in enumerate(input_neurons)})
# one neuron for each phoneme trait
output_neurons = corpus.all_phoneme_traits
empty_output = (0,) * len(output_neurons)
# mapping from phoneme trait to output neuron index
traits_to_neurons = dict({(trait, index) for index, trait in enumerate(output_neurons)})

def wordSamples(word):
    assert len(word.letters) == len(word.phonemes)
    # pad letters and phonemes to make our job easier
    padding_before = ' ' * window_middle
    padding_after = ' ' * (window_size - window_middle - 1)
    padded_letters = padding_before + word.letters + padding_after
    # for each letter in the sample
    for l_num in range(len(word.letters)):
        letters_window = padded_letters[l_num:l_num+window_size-1]
        current_phoneme = word.phonemes[l_num]
        inp = list(empty_input)
        for pos, letter in enumerate(letters_window):
            neuron_index = letters_to_neurons[(letter, pos)]
            inp[neuron_index] = 1
        out = list(empty_output)
        for trait in corpus.phoneme_traits[current_phoneme]:
            trait_index = traits_to_neurons[trait]
            out[trait_index] = 1
        yield inp, out        
            