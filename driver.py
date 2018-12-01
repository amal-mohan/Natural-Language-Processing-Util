# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 13:07:20 2018

@author: amal mohan, nayana thomas
"""

import codecs
from tokenizer import wordTokenizer,sentenceTokenizer
from lemmatizer import wordLemmatizer

filePointer=codecs.open("a.txt",'r',encoding='ascii')

text=filePointer.read()

print(text)
tokenizedWords=wordTokenizer(text)
tokenziedSentence=sentenceTokenizer(text)



#lemmatizedWords=wordLemmatizer(tokenizedWords)
#print(lemmatizedWords)