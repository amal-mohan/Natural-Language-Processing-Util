# # -*- coding: utf-8 -*-
# """
# Created on Sat Dec 01 13:27:52 2018

# @author: amal, nayana
# """

from nltk.corpus import wordnet as wn

def extractRelations(wordList):
	for word in set(wordList):
		print("Word: ",word)
		synsets = wn.synsets(word)
		for synset in synsets:
			print("\tSynset: {}".format(synset.name()))
			print("\tDefinition: {}".format(synset.definition()))
			print("\tExample: {}".format(synset.examples()))
			hyponym = wn.synset(synset.name()).hyponyms()
			print("\t\tHyponymys:", hyponym)
			hypernym = wn.synset(synset.name()).hypernyms()
			print("\t\tHypernyms: ",hypernym)
			holonym_part = wn.synset(synset.name()).part_holonyms() 
			print("\t\tHolonyms_part: ",holonym_part)
			holonym_subst=wn.synset(synset.name()).substance_holonyms() 
			print("\t\tHolonyms_substance: ",holonym_subst)
			meronym_part = wn.synset(synset.name()).part_meronyms()
			print("\t\tMeronyms_part: ",meronym_part)
			meronym_subst=wn.synset(synset.name()).substance_meronyms() 
			print("\t\tMeronyms_substance: ",meronym_subst)