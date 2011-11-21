from collections import namedtuple
import re
import string

class Files:
    dictionary = "dataset/nettalk.data"
    top1000words = "dataset/nettalk.list"

Word = namedtuple('Word', ['letters', 'phonemes', 'structure', 'correspondance'])

letters = string.ascii_lowercase

phoneme_traits = frozenset([
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
    'voiced',
    'tensed',
    'high',
    'medium',
    'low',
    'silent',
    'elide',
    'pause',
    'full_stop',
    'stress1',
    'stress2',
    'syllable_boundary'
])

phoeneme_ignore_traits = frozenset([
    'unvoiced'
])

phonemes_data = [
    ('a', ['low', 'tensed', 'central2']),
    ('b', ['voiced', 'labial', 'stop']),
]
# encapsulate traits in frozenset
phonemes = dict({(n, frozenset(f)) for n, f in phonemes_data})

def loadDictionary():
    dictionary = {}
    with open(Files.dictionary) as f:
        for line in f:
            # break line into columns
            line = line.strip()
            cols = line.split('\t')
            # skip lines that don't appear to be dictionary entries
            if len(cols) != 4:
                print 'skipping line "%s"' % line
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
