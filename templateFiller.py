import nltk
import os
import codecs
from tokenizer import wordTokenizer, sentenceTokenizer
from lemmatizer import verbLemmatizer
from posTagger import wordPosTagger
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

class Template:
	templateName = ""
	filledTemplatesList = []

	def changeTemplateName(self, templateName):
		self.templateName = templateName

	def changeTemplateProperties(self, filledTemplatresList):
		self.filledTemplatesList = filledTemplatesList

def getSynlist(relation):
	synList = []
	syns = wn.synsets(relation.name().split('.')[0])
	for syn in syns:
		synList.append(syn.name())
	return synList

def fillTemplateProperties(word, sentence, rules):
	if word in "kill":
		kill_templateproperties = {"victim":"","cause":"","location":"","time":""}
		filledKillTemplatesList.append(kill_templateproperties)
	if word in "tell":
		tell_templateproperties = {"speaker":"","listner":"","content":""}
		filledTellTemplatesList.append(tell_templateproperties)

def fillFullTemplate():
	kill_template = Template()
	kill_template.changeTemplateName("kill")
	kill_template.changeTemplateProperties(filledKillTemplatesList)
		
	tell_template = Template()
	tell_template.changeTemplateName("tell")
	tell_template.changeTemplateProperties(filledTellTemplatesList)	


def getSentence():
	with codecs.open("corpus.txt", 'r', encoding='utf-8', errors='ignore') as file:
		text = file.read()
	sentences=sentenceTokenizer(text)
	with codecs.open("selectedsentences.txt",'w',encoding='utf-8',errors='ignore') as fi:
		for sentence in sentences:
			# tokenizedWords=wordTokenizer(sentence)
			# sentenceWordset = set(tokenizedWords)
			posTaggedwords = wordPosTagger(sentence)
			allVerbsTag=set(filter(lambda y: "VBG" in  y or "VB" in  y or "VBD" in  y or "VBN" in  y or "VBP" in  y or "VBZ" in  y,posTaggedwords))
			allVerbs=list(map(lambda y: y[0],allVerbsTag))
			sentenceWordset=set(verbLemmatizer(allVerbs))
			for word in wordRelDict:
				intersectionSet = sentenceWordset.intersection(wordRelDict[word])
				if len(intersectionSet) > 0:
					print("\ntemplate : ",word," sentence: ",sentence, "intersectedSet: ",intersectionSet)
					fi.write("\n\ntemplate : "+word+" sentence: "+sentence+ "intersectedSet: "+str(intersectionSet))
	fi.close()
	file.close()

	# 			fillTemplateProperties(word, sentence, rules, intersectionSet)
	# fillFullTemplate()
	

def getRelatedWordList():
	wordDefDict = {'occur':'happen.v.01','damage':'damage.v.01','visit':'visit.v.01','evacuate':'evacuate.v.01','force':'force.v.04','injure':'injure.v.01','trigger':'trip.v.04','strike':'hit.v.05','warn':'warn.v.01','experience':'experience.v.01','kill':'kill.v.01','record':'record.v.01','tell':'tell.v.02'}
	for filename in os.listdir(os.getcwd()+"/selectedVerbs"):
		wordList.append(filename.split('.')[0])
	print(wordList)
	selectedWordListForTemplate = []
	for word in set(wordList):
		print("\nWord: ",word)
		print("______________________")
		synsets = wn.synsets(word)
		relatedWordList = []
		relatedWordList.append(word)
		for synset in synsets:
			# print("Synset: {}".format(synset.name()))
			# print("Definition: {}".format(synset.definition()))
			if wordDefDict[word] in synset.name():
				print("Synset: {}".format(synset.name()))
				print("Synonyms: ")
				for l in synset.lemmas(): 
					print("\t",l.name())
				print("Definition: {}".format(synset.definition()))
				hyponyms = wn.synset(synset.name()).hyponyms()
				print("Hyponyms: ")
				for hyponym in hyponyms:
					print("\t",hyponym.name().split('.')[0])
					relatedWordList.append(hyponym.name().split('.')[0])
				hypernyms = wn.synset(synset.name()).hypernyms()
				print("Hypernyms: ")
				for hypernym in hypernyms:
					print("\t",hypernym.name().split('.')[0])
					relatedWordList.append(hypernym.name().split('.')[0])
				holonyms = wn.synset(synset.name()).part_holonyms()
				print("Holonyms: ")
				for holonym in holonyms:
					print("\t",holonym.name().split('.')[0])
					relatedWordList.append(holonym.name().split('.')[0])
				meronyms = wn.synset(synset.name()).part_meronyms()
				print("Meronyms: ")
				for meronym in meronyms:
					print("\t",meronym.name().split('.')[0])
					relatedWordList.append(meronym.name().split('.')[0])
		print("relatedWordList: ",relatedWordList)
		wordRelDict[word] = set(relatedWordList)

wordList=[]
wordRelDict = {}
filledKillTemplatesList = []
filledTellTemplatesList = []
getRelatedWordList()
getSentence()





