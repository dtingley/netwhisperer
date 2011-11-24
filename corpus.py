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
    'full_stop',
    'stress1',
    'stress3',      # 'stress2' is the default
    'syllable_boundary'
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

# Mikkel will finish this
phonemes_data = [
    ('a', ['low', 'tensed', 'central2']),
    ('b', ['voiced', 'labial', 'stop']),
]
# map synonyms
for traits in phonemes_data.values:
    for (i, trait) in enumerate(traits):
        if trait in phoneme_trait_synonyms:
            traits[i] = phoneme_trait_synonyms[trait]

# encapsulate mapped traits
phoneme_traits = dict(phonemes_data)
    
# make sure there are no errors
assert all({traits.issubset(all_phoneme_traits) for traits in phoneme_traits.itervalues()})

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
