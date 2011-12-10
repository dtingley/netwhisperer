#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 David Tingley <david@david-Vostro-1520>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import corpus
import re
import string
import cPickle as pickle 

def main():
	space = ' ';
	lines = open('dataset/test2.txt','r').read().replace('\n',' ')
	words = lines.split(' ')
	
	datalines = []
	for i in words:
		if len(i) > 1: 
			thisline = i.lower().split(' ')
			thisline = filter(None,thisline)	
			for i in range(len(thisline)):
				for punct in string.punctuation:
					thisline[i] = thisline[i].replace(punct, ' ')
			thisline[i] = thisline[i].replace('\n',' ')
			thisline[i] = re.sub(r"[0-9.,]",' ', thisline[i])
			datalines.append(thisline)
		datalines = filter(None,datalines)

		
	dict = open('dataset/nettalk.data','r')
	dictlines = dict.readlines()
	wordlines = []
	phonemes = []
	
			
	for j in datalines:
		for w in range(len(j)):
			j[w] = j[w].replace(' ','')			
		for i in j:
			lineno = 0
			if i == '':
				phonemes.append('')
				break 
			if len(i) > 0:
				for line in dictlines:
					lineno = lineno + 1
					patt = re.compile(i+'\t');
					if patt.match(line):	
						p = line.split('\t')
						phonemes.append(p[1])
						break
					if lineno == len(dictlines):
						q ='';	
						for j in range(len(i)):
							q = q + ' ';
						phonemes.append(q)
	
	
	phonetic_rep = ''
	word_rep = ''
	phonetic = []	
	for i in range(len(phonemes)):
		phonetic.append(''.join(phonemes[i]))
	phonetic_rep = ' '.join(phonetic) + ' '
	
	for i in datalines:
		word_rep = word_rep + ' '.join(i) + ' '
		
	print len(word_rep)
	print len(phonetic_rep)
	
	data = []
	data.append(word_rep)
	data.append(phonetic_rep)
	file_handle = open('/home/david/Desktop/netwhisperer2/dataset/data','w')
	pickle.dump(data, file_handle)
	return 0


if __name__ == '__main__':
	
	
	main()

