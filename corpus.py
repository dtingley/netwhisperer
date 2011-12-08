from collections import namedtuple
import re
import string
import logging

class Files:
    dictionary = "dataset/nettalk.data"
    top1000words = "dataset/nettalk.list"

Word = namedtuple('Word', ['letters', 'phonemes', 'structure', 'correspondance'])

all_letters = string.ascii_lowercase + ',' + '.' + ' '

all_phoneme_traits = frozenset([
    'front1', 
    'front2',
    'central1',
    'central2',
    'back1',
    'back2',
    'stop',
    'nasal',
    'fricative',
    'affricative',
    'glide',
    'liquid',
    'voiced',       # 'unvoiced' is the default
    'tensed',
    'high',
    'medium',
    'low',
    'silent',
    'elide',
    'pause',
    'full stop'
])

all_stress_traits = frozenset([
    'stress1',
    'stress3',      # 'stress2' is the default
    'syllable boundary'
])

# synonyms for the same phoneme traits
phoneme_trait_synonyms = {
    'labial' : 'front1',
    'dental' : 'front2',
    'alveolar' : 'central1',
    'palatal' : 'central2',
    'velar' : 'back1',
    'glottal' : 'back2'
}

# traits we can ignore because they are the defaults
phoneme_trait_defaults = set([
    'unvoiced'
])

phonemes_data = [
    ('a', ['low', 'tensed', 'central2']),
    ('b', ['voiced', 'labial', 'stop']),
    ('c', ['unvoiced', 'velar', 'medium']),
    ('d', ['voiced', 'alveolar', 'stop']),
    ('e', ['medium', 'tensed', 'front2']),
    ('f', ['unvoiced', 'labial', 'fricative']),
    ('g', ['voiced', 'velar', 'stop']),
    ('h', ['unvoiced', 'glottal', 'glide']),
    ('i', ['high', 'tensed', 'front1']),
    ('k', ['unvoiced', 'velar', 'stop']),
    ('l', ['voiced', 'dental', 'liquid']),
    ('m', ['voiced', 'labial', 'nasal']),
    ('n', ['voiced', 'alveolar', 'nasal']),
    ('o', ['medium', 'tensed', 'back2']),
    ('p', ['unvoiced', 'labial', 'stop']),
    ('r', ['voiced', 'palatal', 'liquid']),
    ('s', ['unvoiced', 'alveolar', 'fricative']),
    ('t', ['unvoiced', 'alveolar', 'stop']),
    ('u', ['high', 'tensed', 'back2']),
    ('v', ['voiced', 'labial', 'fricative']),
    ('w', ['voiced', 'labial', 'glide']),
    ('x', ['medium', 'central2']),
    ('y', ['voiced', 'palatal', 'glide']),
    ('z', ['voiced', 'alveolar', 'fricative']),
    ('A', ['medium', 'tensed', 'front2', 'central1']), 
    ('C', ['unvoiced', 'palatal', 'affricative']),
    ('D', ['voiced', 'dental', 'fricative']),
    ('E', ['medium', 'front1', 'front2']),
    ('G', ['voiced', 'velar', 'nasal']),
    ('I', ['high', 'front1']),
    ('J', ['voiced', 'velar', 'nasal']),
    ('K', ['unvoiced', 'palatal', 'fricative', 'velar', 'affricative']),
    ('L', ['voiced', 'alveolar', 'liquid']),
    ('M', ['voiced', 'dental', 'nasal']),
    ('N', ['voiced', 'palatal', 'nasal']),
    ('O', ['medium', 'tensed', 'central1', 'central2']),
    ('Q', ['voiced', 'labial', 'velar', 'affricative', 'stop']),
    ('R', ['voiced', 'velar', 'liquid']),
    ('S', ['unvoiced', 'palatal', 'fricative']),
    ('T', ['unvoiced', 'dental', 'fricative']),
    ('U', ['high', 'back1']),
    ('W', ['high', 'medium', 'tensed', 'central2', 'back1']),
    ('X', ['unvoiced', 'affricative', 'front2', 'central1']),
    ('Y', ['high', 'tensed', 'front1', 'front2', 'central1']),
    ('Z', ['voiced', 'palatal', 'fricative']),
    ('@', ['low', 'front2']),
    ('!', ['unvoiced', 'labial', 'dental', 'affricative']),
    ('#', ['voiced', 'palatal', 'velar', 'affricative']),
    ('*', ['voiced', 'glide', 'front1', 'low', 'central1']),
    # Not found in new data set
    #(':', ['high', 'front1', 'front2']),
    # Found only in new data set, not original paper
    ('+', ['voiced', 'glide', 'tensed', 'low', 'back2']),
    ('^', ['low', 'central1']),
    ('-', ['silent', 'elide']),
    (' ', ['pause', 'elide']),
    ('.', ['pause', 'full stop'])
]

for (name, traits) in phonemes_data:
    # map synonyms
    for (i, trait) in enumerate(traits):
        if trait in phoneme_trait_synonyms:
            traits[i] = phoneme_trait_synonyms[trait]
    # delete defaults
    for (i, trait) in enumerate(traits):
        if trait in phoneme_trait_defaults:
            del traits[i]

# encapsulate mapped traits
phoneme_traits = dict({(name, frozenset(traits)) for name, traits in phonemes_data})
    
# make sure there are no errors
for traits in phoneme_traits.itervalues():
    assert traits.issubset(all_phoneme_traits), 'one is a bad trait: %s' % traits
    
def loadDictionary():
    dictionary = {}
    with open(Files.dictionary) as f:
        for line in f:
            # break line into columns
            line = line.strip()
            cols = line.split('\t')
            # skip lines that don't appear to be dictionary entries
            if len(cols) != 4:
                logging.debug('skipping line: %s' % line)
                continue
            else:
                word = Word(*cols)
                dictionary[word.letters] = word
    return dictionary

def loadTop1000Words(dict):
    text = file(Files.top1000words).read()
    text = re.search(r'\((\w+\b\s*){1000}\)', text).group(0)
    text = text.lower()
    words = re.findall(r'\w+', text)    
    return [dict[w] for w in words]
    
dictionary = loadDictionary()
top1000words = loadTop1000Words(dictionary)
