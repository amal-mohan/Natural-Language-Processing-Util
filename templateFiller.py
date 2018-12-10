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

def fillTemplateProperties(word, sentence, intersectionSet, filledKillTemplatesList):
	dependencyDict = {}
	cause = ""
	if word == "kill":
		intersectionWord = intersectionSet.pop()
		x = Template()
		x.changeSentence(sentence)
		kill_templateproperties = {"victim":"","cause":"","location":"","time":""}
        
		filledKillTemplatesList.append(kill_templateproperties)
	if word in "tell":
		tell_templateproperties = {"speaker":"","listner":"","content":""}
		filledTellTemplatesList.append(tell_templateproperties)

			if WordNetLemmatizer().lemmatize(token.head.text ,'v') == intersectionWord:
				
				if "nsubj" in dependencyDict[token.head.text]:
					# if "det" in depList:
					# 	cause = depdict["nummod"]
					# if "nummod" in depList:
					# 	cause = cause+" "+depdict["nummod"]
					# if "amod" in depList:
					# 	cause = cause+" "+depdict["amod"]
					cause = dependencyDict[token.head.text]["nsubj"]
					kill_templateproperties["cause"] = cause
					if "dobj" in dependencyDict[token.head.text]:
						victim = dependencyDict[token.head.text]["dobj"]
						kill_templateproperties["victim"] = victim

				elif "nsubjpass" in dependencyDict[token.head.text]:
					victim = dependencyDict[token.head.text]["nsubjpass"]
					kill_templateproperties["victim"] = victim

					if "dobj" in dependencyDict[token.head.text]:
						cause = dependencyDict[token.head.text]["dobj"]
						kill_templateproperties["cause"] = cause

				elif "advcl" in dependencyDict[token.head.text]:
					advClause = dependencyDict[token.head.text]["advcl"]

					if "nsubj" in dependencyDict[advClause]:
						cause = dependencyDict[advClause]["nsubj"]

					if "dobj" in dependencyDict[token.head.text]:
						victim = dependencyDict[token.head.text]["dobj"]
						kill_templateproperties["victim"] = victim


				# print("{0}/{1} <--{2}-- {3}/{4}".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))
		x.changeTemplateName("kill")
		x.changeTemplateProperties(kill_templateproperties)
		filledKillTemplatesList.append(x)
	# if word in "tell":
	# 	tell_templateproperties = {"speaker":"","listner":"","content":""}
	# 	filledTellTemplatesList.append(tell_templateproperties)

def fillFullTemplate(filledKillTemplatesList):
	for template in filledKillTemplatesList:
		print(template.templateName)
		print(template.sentence)
		print(template.filledTemplate)

def getSentence():
	filledKillTemplatesList = []
	with codecs.open("corpus.txt", 'r', encoding='utf-8', errors='ignore') as file:
		text = file.read()
	# text = "The temblor that struck northern Armenia on December 7, 1988, killed more than 25,000 people, injured up to 130,000, and left hundreds of thousands homeless or without basic supplies."
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
                    fillTemplateProperties(word, sentence, rules, intersectionSet)					print("\ntemplate : ",word," sentence: ",sentence, "intersectedSet: ",intersectionSet)
					fi.write("\n\ntemplate : "+word+" sentence: "+sentence+ "intersectedSet: "+str(intersectionSet))
	fi.close()
	file.close()

	# 			
	fillFullTemplate(filledKillTemplatesList)
	

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
getRelatedWordList()
getSentence()





