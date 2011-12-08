
#Need to add secondary and primary stress in the dictionary
def to_espeak(input):
    data = getPhonemeMapping()
    
    output = '"[['
    for letter in input:
        if letter == ' ':
            output = output[:len(output)-1] #removes a phoneme seperator before adding a word boundry
            output +=  data[letter]
        else:
            output +=  data[letter] + '|' #adds a phoneme seperator after each phoneme
    
    output += ']]"'
    #f = open('to_espeak.txt', 'w')
    #f.write(output)
    #f.close
    return output

def getPhonemeMapping():
    return dict({'a': 'A:',
                 'b':'b',
                 'c':'O:',
                 'd':'d',
                 'e':'eI',
                 'f':'f',
                 'g':'g',
                 'h':'h',
                 'i':'i',
                 'k':'k',
                 'l':'l',
                 'm':'m',
                 'n':'n',
                 'o':'oU',
                 'p':'p',
                 'r':'r',
                 's':'s',
                 't':'t',
                 'u':'u:',
                 'v':'v',
                 'w':'w',
                 'x':'a2',
                 'y':'j',
                 'z':'z',
                 'A':'aI',
                 'C':'tS',
                 'D':'D',
                 'E':'E',
                 'G':'N', 
                 'I':'I',
                 'J':'dZ',
                 'K':'kZ',
                 'L':'@L',
                 'M':'m', # I have no idea how to interpret this one from the nettalk paper [J: That's because it's not an english sound]
                 'N':'n', # I can't find an equivallent for this [J: it's just a slightly different 'n']
                 'O':'OI', # [J: was "oi"]
                 'Q':'kw', # Totally made this up [J: 'qu' in quest is pronounced 'kw' ]
                 'R':'3',
                 'S':'S',
                 'T':'T',
                 'U':'U',
                 'W':'aU',
                 'X':'ks', 
                 'Y':'ju:',
                 'Z':'Z',
                 '@':'a', # [J: was '@']
                 #From here and under a lot the translations are just made up by a non-native english speaker [J: reviewed and edited]
                 '!':'tz',
                 '#':'gz',
                 '*':'wV',
                 # not used in new data set
                 ':':'I',
                 # only in new data set
                 '+':'wa',
                 '^':'V',
                 '-':'', # [J: should not pause!]
                 ' ':'||',
                 # J: commented out
                 #'.':'',
                 #'1':'\'',
                 #'2':','
})

#http://espeak.sourceforge.net/dictionary.html - list of utility phonemes
#The left side of this dictionary can be found on page 4 in the netTalk-paper
#http://espeak.sourceforge.net/phonemes.html - a list of supported phonemes in espeak
