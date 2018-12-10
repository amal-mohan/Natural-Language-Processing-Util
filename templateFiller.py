import nltk
import os
import spacy
nlp = spacy.load('en')
import codecs
from tokenizer import wordTokenizer, sentenceTokenizer
from lemmatizer import verbLemmatizer
from posTagger import wordPosTagger
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

class Template:
	templateName = ""
	filledTemplate = {}
	sentence = ""

	def changeTemplateName(self, templateName):
		self.templateName = templateName

	def changeTemplateProperties(self,  filledTemplate):
		self.filledTemplate = filledTemplate

	def changeSentence(self, sentence):
		self.sentence = sentence

def getSynlist(relation):
	synList = []
	syns = wn.synsets(relation.name().split('.')[0])
	for syn in syns:
		synList.append(syn.name())
	return synList

def getDepChildren(dependencyDict,value):
	deplist=[]
	if value not in dependencyDict:
		return deplist
	for depkey in dependencyDict[value]:
		deplist.append(dependencyDict[value][depkey])
		deplist.extend(getDepChildren(dependencyDict,dependencyDict[value][depkey]))
		
	return deplist

def calculateSubTree(dependencyDict,value):
#	deplist=[]
#	for depkey in dependencyDict[value]:
#								#print(type(x))
#		deplist.append(dependencyDict[value][depkey])
	deplist=getDepChildren(dependencyDict,value)   
	deplist.sort(key=lambda val: val.i)
	s=""
	for r in deplist:
		s=s+" "+r.text
	return s.strip()

def fillKillTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	kill_templateproperties = {"victim":"","cause":"","location":"","time":""}
	sent = nlp(sentence)
	for s_word in sent.ents:
		if s_word.label_ == "GPE":
			kill_templateproperties["location"] = s_word
		elif s_word.label_ == "DATE":
			kill_templateproperties["time"] = s_word
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token

		if WordNetLemmatizer().lemmatize(token.head.text ,'v') == intersectionWord:
			
			if "nsubj" in dependencyDict[token.head]:
				cause = dependencyDict[token.head]["nsubj"]
				kill_templateproperties["cause"] = cause
				if "dobj" in dependencyDict[token.head]:
					victim = dependencyDict[token.head]["dobj"]
					kill_templateproperties["victim"] = victim.text
					
					if victim in dependencyDict:
						s=calculateSubTree(dependencyDict,victim)
						kill_templateproperties["victim"] = s+" "+kill_templateproperties["victim"]
#						if victim in dependencyDict and "nummod" in dependencyDict[victim]:
#							kill_templateproperties["victim"] = dependencyDict[victim]["nummod"].text+" "+kill_templateproperties["victim"]


			elif "nsubjpass" in dependencyDict[token.head]:
				victim = dependencyDict[token.head]["nsubjpass"]
				kill_templateproperties["victim"] = victim.text
				if victim in dependencyDict:
					s=calculateSubTree(dependencyDict,victim)
					kill_templateproperties["victim"] = s+" "+kill_templateproperties["victim"]
					
				if "dobj" in dependencyDict[token.head]:
					cause = dependencyDict[token.head]["dobj"]
					kill_templateproperties["cause"] = cause.text

			elif "advcl" in dependencyDict[token.head]:
				advClause = dependencyDict[token.head]["advcl"]

				if "nsubj" in dependencyDict[advClause]:
					cause = dependencyDict[advClause]["nsubj"].text

				if "dobj" in dependencyDict[token.head]:
					victim = dependencyDict[token.head]["dobj"]
					kill_templateproperties["victim"] = victim.text

	x.changeTemplateName("kill")
	x.changeTemplateProperties(kill_templateproperties)
	filledKillTemplatesList.append(x)


def fillTellTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"speaker":"","listner":"","time":""}
	sent = nlp(sentence)
	for s_word in sent.ents:
		if s_word.label_ == "DATE":
			tell_templateproperties["time"] = s_word
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
		if WordNetLemmatizer().lemmatize(token.head.text ,'v') == intersectionWord:
			if "nsubj" in dependencyDict[token.head]:
				speaker = dependencyDict[token.head]["nsubj"]
				tell_templateproperties["speaker"] = speaker.text
				s=calculateSubTree(dependencyDict,speaker)
				tell_templateproperties["speaker"] = s+" "+tell_templateproperties["speaker"]
				# if speaker in dependencyDict and "nummod" in dependencyDict[speaker]:
				# 		tell_templateproperties["speaker"] = dependencyDict[speaker]["nummod"].text+" "+tell_templateproperties["listner"]
				if "dobj" in dependencyDict[token.head]:
					listner = dependencyDict[token.head]["dobj"]
					tell_templateproperties["listner"] = listner.text
					s=calculateSubTree(dependencyDict,listner)
					tell_templateproperties["listner"] = s+" "+tell_templateproperties["listner"]
					
			elif "nsubjpass" in dependencyDict[token.head]:
				listner = dependencyDict[token.head]["nsubjpass"]
				tell_templateproperties["listner"] = listner

				if "dobj" in dependencyDict[token.head]:
					speaker = dependencyDict[token.head]["dobj"]
					tell_templateproperties["speaker"] = speaker.text

			elif "advcl" in dependencyDict[token.head]:
				advClause = dependencyDict[token.head]["advcl"]

				if (advClause in dependencyDict) and ("nsubj" in dependencyDict[advClause]):
					speaker = dependencyDict[advClause]["nsubj"].text

				if "dobj" in dependencyDict[token.head]:
					listner = dependencyDict[token.head]["dobj"]
					tell_templateproperties["listner"] = listner.text
					s=calculateSubTree(dependencyDict,listner)
					tell_templateproperties["listner"] = s+" "+tell_templateproperties["listner"]

	x.changeTemplateName("tell")
	x.changeTemplateProperties(tell_templateproperties)
	filledTellTemplatesList.append(x)

def fillTemplateProperties(word, sentence, intersectionSet):
	if word == "kill":
		fillKillTemplate(word, sentence, intersectionSet)
	if word == "tell":
		fillTellTemplate(word, sentence, intersectionSet)


def fillFullTemplate():
	for template in filledKillTemplatesList:
		print(template.templateName)
		print(template.sentence)
		print(template.filledTemplate)
	for template in filledTellTemplatesList:
		print(template.templateName)
		print(template.sentence)
		print(template.filledTemplate)

def getSentence():
	with codecs.open("corpus.txt", 'r', encoding='utf-8', errors='ignore') as file:
		text = file.read()
	# text = "The temblor that struck northern Armenia on December 7, 1988, killed more than 25,000 people, injured up to 130,000, and left hundreds of thousands homeless or without basic supplies."
	sentences=sentenceTokenizer(text)
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
				fillTemplateProperties(word, sentence, intersectionSet)
	file.close()
	fillFullTemplate()

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





