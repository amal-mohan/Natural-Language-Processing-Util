# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 13:07:20 2018

@author: amal mohan, nayana thomas
"""

import codecs
from tokenizer import wordTokenizer,sentenceTokenizer
from lemmatizer import wordLemmatizer

filePointer=codecs.open("a.txt",'r',encoding='utf-8')

text=filePointer.read()

print(text)
tokenizedWords=wordTokenizer(text)
print("tokenizedWords: **************\n",tokenizedWords)
tokenziedSentence=sentenceTokenizer(text)
print("tokenizedsentence: **************\n",tokenziedSentence)


lemmatizedWords=wordLemmatizer(tokenizedWords)
print("lemmatizedWords************",lemmatizedWords)