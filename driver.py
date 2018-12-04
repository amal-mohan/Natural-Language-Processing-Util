# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 13:07:20 2018

@author: amal mohan, nayana thomas
"""

import codecs
from tokenizer import wordTokenizer,sentenceTokenizer
from lemmatizer import wordLemmatizer
from posTagger import wordPosTagger
from dependencyParser import dependencyParse
from relationExtractor import extractRelations

filePointer=codecs.open("a.txt",'r',encoding='utf-8')
text=filePointer.read()

print(text)
tokenizedWords=wordTokenizer(text)
print("Tokenized Words: \n",tokenizedWords)
tokenziedSentence=sentenceTokenizer(text)
print("\n\nTokenized Sentence: \n",tokenziedSentence)

lemmatizedWords=wordLemmatizer(tokenizedWords)
print("\n\nLemmatized Words: \n",lemmatizedWords)

posTaggedwords = wordPosTagger(text)
print("\n\nPOS Tagged Words: \n",posTaggedwords)

#dependencyParse(text)

#extractRelations(tokenizedWords)