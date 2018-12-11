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

print("Reading corpus")
filePointer=codecs.open("corpus.txt",'r',encoding='utf-8',errors="ignore")
text=filePointer.read()
print("Fetched corpus successfully")

def extractNLPFeatures():
	#Tokenize the corpus into words
	input("Press Enter to tokenize the corpus into words...")
	tokenizedWords=wordTokenizer(text)
	print("Tokenized Words: \n",tokenizedWords)

	input("Press Enter to tokenize the corpus into sentences...")
	tokenziedSentence=sentenceTokenizer(text)
	print("\n\nTokenized Sentence: \n",tokenziedSentence)

	#Lemmatize the words to extract lemma as features
	input("Press Enter to extract lemma as features...")
	lemmatizedWords=wordLemmatizer(tokenizedWords)
	print("\n\nLemmatized Words: \n",lemmatizedWords)

	input("Press Enter to extract POS tag features...")
	#POS tag the words to extract POS tag features
	posTaggedwords = wordPosTagger(text)
	print("\n\nPOS Tagged Words: \n",posTaggedwords)

	input("Press Enter to extract hypernymns, hyponyms, meronyms, AND holonyms as features ...")
	#Using WordNet, extracting hypernymns, hyponyms, meronyms, AND holonyms as features 
	extractRelations(tokenizedWords)

	input("Press Enter to perform dependency parsing...")
	#Perform dependency parsing or full-syntactic parsing to parse-tree based patterns as features 
	dependencyParse(text)

if __name__ == '__main__':
	extractNLPFeatures()