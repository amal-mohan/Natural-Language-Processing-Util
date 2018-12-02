from nltk.corpus import wordnet as wn

def extractRelations(wordList):
	for word in wordList:
		print("Word: ",word)
		synsets = wn.synsets(word)
		for synset in synsets:
			print("\tLemma: {}".format(synset.name()))
			print("\tDefinition: {}".format(synset.definition()))
			print("\tExample: {}".format(synset.examples()))
			hyponym = wn.synset(synset.name()).hyponyms()
			print("\t\tHyponymys:", hyponym)
			hypernym = wn.synset(synset.name()).hypernyms()
			print("\t\tHypernyms: ",hypernym)
			holonym = wn.synset(synset.name()).part_holonyms() 
			print("\t\tHolonyms: ",holonym)
			meronym = wn.synset(synset.name()).part_meronyms()
			print("\t\tMeronyms: ",meronym)