import nltk
import re
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
import sys

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

def getDepChildren(dependencyDict,value,count):
	deplist=[]
	deplist.append(value)
	if value not in dependencyDict or count==100:
		return deplist
	for depkey in dependencyDict[value]:
		deplist.append(dependencyDict[value][depkey])
		deplist.extend(getDepChildren(dependencyDict,dependencyDict[value][depkey],count+1))
		
	return list(set(deplist))

def calculateSubTree(dependencyDict,value):
	deplist=getDepChildren(dependencyDict,value,0)   
	deplist.sort(key=lambda val: val.i)
	s=""
	for r in deplist:
		s=s+" "+r.text
	return s.strip()

def findProperty(dependencyDict,token,findSubtree,prop):
	subjectToken = dependencyDict[token][prop]
	subject=""
	if subjectToken in dependencyDict and findSubtree:
		s=calculateSubTree(dependencyDict,subjectToken)
		subject = s+" "+subject
	else:
		subject=subjectToken.text
	return subject


def dependencyWordObject(dependencyDict,word):
    for x in dependencyDict:
        if x.text==word:
            return x

def findLocation(sent,dependencyDict):
	locList=["area","island","district","capital","country","city","town","village"] 
	for word in sent:
		if WordNetLemmatizer().lemmatize(word.text,'n') in locList:
			loc=dependencyWordObject(dependencyDict,word.text)
			if loc is None:
				return word.text
			return calculateSubTree(dependencyDict,dependencyWordObject(dependencyDict,word.text))
	return ""

def findNamedEntity(sent,label,dependencyDict):
	if label=="GPE":
		for s_word in sent.ents:
			if s_word.label_ == "GPE":
				return s_word
		return findLocation(sent,dependencyDict)
	if label == "DATE":
		for s_word in sent.ents:
			if s_word.label_ == "DATE":
				return s_word
		return ""

def preopositionHandler(dependencyDict,token):
	subject=""
	if "agent" in dependencyDict[token]:
		agent = dependencyDict[token]["agent"]
		if "pobj" in dependencyDict[agent]:
			subject = findProperty(dependencyDict,agent,True,"pobj")
	elif "prep" in dependencyDict[token]:
		prep = dependencyDict[token]["prep"]
		if "pobj" in dependencyDict[prep]:
			subject = findProperty(dependencyDict,prep,True,"pobj")
	return subject

def findSubjectObject(dependencyDict,intersectionWord,checkPrep=False,prep=[]):
	subject=""
	obj=""
	prepuse=0
	usewords=["from","which","that","in"]
	for token in dependencyDict:
		if ('v' in token.tag_ or 'V' in token.tag_) and WordNetLemmatizer().lemmatize(token.text ,'v') == intersectionWord:
			if "advcl" in dependencyDict[token.head] and "nsubjpass" not in dependencyDict[token] and "nsubj" not in dependencyDict[token] and dependencyDict[token.head]["advcl"]==token:
				advClause = token.head
				if "nsubj" in dependencyDict[advClause]:
					subject = findProperty(dependencyDict,advClause,True,"nsubj")                   
				if "dobj" in dependencyDict[token]:
					obj = findProperty(dependencyDict,token,True,"dobj")
				elif "dobj" in dependencyDict[advClause]:
					obj = findProperty(dependencyDict,advClause,True,"dobj")
			else:
				if "nsubjpass" in dependencyDict[token]:
					obj = findProperty(dependencyDict,token,True,"nsubjpass")	
					if(obj in usewords):
						if  "advcl" in dependencyDict[token.head] and dependencyDict[token.head]["advcl"]==token and "dobj" in dependencyDict[token.head]:
							obj=findProperty(dependencyDict,token.head,True,"dobj")
						elif  "relcl" in dependencyDict[token.head] and dependencyDict[token.head]["relcl"]==token:
								obj=calculateSubTree(dependencyDict,token.head)
					if "dobj" in dependencyDict[token]:
						subject = findProperty(dependencyDict,token,True,"dobj")
					else:
						subject=preopositionHandler(dependencyDict,token)
				else:
					if "nsubj" in dependencyDict[token]:
						subject=findProperty(dependencyDict,token,True,"nsubj")
						if subject=="that" or subject=="which" or subject=="who":
							if  "advcl" in dependencyDict[token.head] and dependencyDict[token.head]["advcl"]==token and "dobj" in dependencyDict[token.head]:
								subject=findProperty(dependencyDict,token.head,True,"dobj")
							elif  "relcl" in dependencyDict[token.head] and dependencyDict[token.head]["relcl"]==token:
								subject=calculateSubTree(dependencyDict,token.head)
					else:
						prepuse=0
						subject=preopositionHandler(dependencyDict,token)
						if subject!="":
							prepuse=1
						if subject =="" and token.head in dependencyDict:
							if "nsubj" in dependencyDict[token.head]:
								subject=findProperty(dependencyDict,token.head,True,"nsubj")
							elif  "xcomp" in dependencyDict[token.head] and dependencyDict[token.head]["xcomp"]==token and "nsubjpass" in dependencyDict[token.head]:
								subject=findProperty(dependencyDict,token.head,True,"nsubjpass")
							elif 'conj' in dependencyDict[token.head] and dependencyDict[token.head]["conj"]==token and "nsubjpass" in dependencyDict[token.head]:
								subject=findProperty(dependencyDict,token.head,True,"nsubjpass")
							else:
								head=token.head
								i=0
								while(head.head in dependencyDict and i<=3):
									i+=1
									head=head.head
									if("nsubj" in dependencyDict[head]):
										subject=findProperty(dependencyDict,head,True,"nsubj")
										break
					if "dobj" in dependencyDict[token]:
						obj = findProperty(dependencyDict,token,True,"dobj")
					elif "ccomp" in dependencyDict[token] and dependencyDict[token]['ccomp'] in dependencyDict and "nsubjpass" in dependencyDict[dependencyDict[token]['ccomp']]:
						obj=findProperty(dependencyDict,dependencyDict[token]['ccomp'],True,"nsubjpass")
					elif checkPrep==True and "prep" in dependencyDict[token] and dependencyDict[token]["prep"].text in prep and  "pobj" in dependencyDict[dependencyDict[token]["prep"]]:
						obj=findProperty(dependencyDict,dependencyDict[token]["prep"],True,"pobj")
					elif 'conj' in dependencyDict[token.head] and dependencyDict[token.head]["conj"]==token and "nsubjpass" in dependencyDict[token.head]:
						obj=findProperty(dependencyDict,token.head,True,"nsubjpass")
					elif 'xcomp' in dependencyDict[token.head] and dependencyDict[token.head]["xcomp"]==token and "dobj" in dependencyDict[token.head]:
						obj=findProperty(dependencyDict,token.head,True,"dobj")
					else:
						head=token.head
						i=0
						while(head.head in dependencyDict and i<=3):
							i+=1
							head=head.head
							if("nsubjpass" in dependencyDict[head]):
								obj=findProperty(dependencyDict,head,True,"nsubjpass")
								break
							elif("dobj" in dependencyDict[head]):
								obj=findProperty(dependencyDict,head,True,"dobj")
								break
			break
	for useword in usewords:
		subject=subject.split(" "+useword+" ")[0]
		obj=obj.split(" "+useword+" ")[0]
	return[subject,obj]
				
def fillKillTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	kill_templateproperties = {"victim":"","cause":"","location":"","time":""}
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	sent = nlp(sentence)
	kill_templateproperties["location"]=findNamedEntity(sent,"GPE",dependencyDict)
	kill_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	kill_templateproperties["cause"]=subObj[0]
	kill_templateproperties["victim"]=subObj[1]

	x.changeTemplateName("kill")
	x.changeTemplateProperties(kill_templateproperties)
	filledTemplate.append(x)

def fillTellTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"speaker":"","listener":"","time":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["speaker"]=subObj[0]
	tell_templateproperties["listener"]=subObj[1]
	x.changeTemplateName("tell")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)

def fillTriggerTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"instigator":"","incident":"","location":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["instigator"]=subObj[0]
	tell_templateproperties["incident"]=subObj[1]
	x.changeTemplateName("trigger")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)

def fillInjuredTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	kill_templateproperties = {"victim":"","cause":"","location":"","time":""}
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	sent = nlp(sentence)
	kill_templateproperties["location"]=findNamedEntity(sent,"GPE",dependencyDict)
	kill_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	kill_templateproperties["cause"]=subObj[0]
	kill_templateproperties["victim"]=subObj[1]

	x.changeTemplateName("injure")
	x.changeTemplateProperties(kill_templateproperties)
	filledTemplate.append(x)

def fillForcedTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	kill_templateproperties = {"forced-entity":"","cause":"","action":""}
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	sent = nlp(sentence)
#	kill_templateproperties["location"]=findNamedEntity(sent,"GPE",dependencyDict)
#	kill_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	kill_templateproperties["forced-entity"]=subObj[0]
	kill_templateproperties["cause"]=""
	kill_templateproperties["action"]=""
	for token in doc:
		if 'to' in token.text and "PRE" in token.tag_:
			kill_templateproperties["action"]=calculateSubTree(dependencyDict,dependencyDict[token]["pobj"])
			break
	if kill_templateproperties["action"]=="":
		for token in dependencyDict:
			if WordNetLemmatizer().lemmatize(token.text ,'v') == intersectionWord:
				if "xcomp" in dependencyDict[token]:
					kill_templateproperties["action"]=calculateSubTree(dependencyDict,dependencyDict[token]["xcomp"])
					break
	if kill_templateproperties["cause"]=="":
		for token in dependencyDict:
			if WordNetLemmatizer().lemmatize(token.text ,'v') == intersectionWord:
				if "advcl" in dependencyDict[token]:
					kill_templateproperties["cause"]=calculateSubTree(dependencyDict,dependencyDict[token]["advcl"])
					break
	x.changeTemplateName("force")
	x.changeTemplateProperties(kill_templateproperties)
	filledTemplate.append(x)

	
def fillOccuredTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	kill_templateproperties = {"event":"","location":"","time":""}
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	sent = nlp(sentence)
	kill_templateproperties["location"]=findNamedEntity(sent,"GPE",dependencyDict)
	kill_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	kill_templateproperties["event"]=subObj[0]

	x.changeTemplateName("occured")
	x.changeTemplateProperties(kill_templateproperties)
	filledTemplate.append(x)

	
def fillTemplateProperties(word, sentence, intersectionSet):
	if word == "kill":
		a=1
		fillKillTemplate(word, sentence, intersectionSet)
	if word == "tell":
		a=2
		fillTellTemplate(word, sentence, intersectionSet)
	if word=="experience":
		a=3
		fillExperienceTemplate(word, sentence, intersectionSet)
	if word=="trigger":
		a=4
		fillTriggerTemplate(word, sentence, intersectionSet)
	if word=="visit":
		a=5
		fillVisitTemplate(word, sentence, intersectionSet)
	if word=="record":
		a=6
		fillRecordTemplate(word, sentence, intersectionSet)
	if word=="warn":
		a=7
		fillWarnTemplate(word, sentence, intersectionSet)
	if word=="evacuate":
		a=8
		fillEvacuateTemplate(word, sentence, intersectionSet)
	if word=="damage":
		a=9
		fillDamageTemplate(word, sentence, intersectionSet)
	if word=="strike":
		a=10
		fillStrikeTemplate(word, sentence, intersectionSet)
	if word=="injure":
		a=10
		fillInjuredTemplate(word, sentence, intersectionSet)
	if word=="force":
		a=10
		fillForcedTemplate(word, sentence, intersectionSet)
	if word=="occur":
		a=10
		fillOccuredTemplate(word, sentence, intersectionSet)


def fillVisitTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"visitor":"","location":"","time":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["visitor"]=subObj[0]
	#tell_templateproperties["experience"]=subObj[1]
	x.changeTemplateName("visit")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)

def fillWarnTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"admonisher":"","location":"","warning":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord,True,['of','against'])
	tell_templateproperties["admonisher"]=subObj[0]
	tell_templateproperties["warning"]=subObj[1]
	x.changeTemplateName("warn")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)
	
def fillRecordTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"recorder":"","incident":"","location":"","time":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["recorder"]=subObj[0]
	tell_templateproperties["incident"]=subObj[1]
	x.changeTemplateName("record")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)
		
def fillExperienceTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"experiencer":"","experience":"","time":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["experiencer"]=subObj[0]
	tell_templateproperties["experience"]=subObj[1]
	x.changeTemplateName("experience")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)
	
def fillEvacuateTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"evacuating-entity":"","evacuated-entity":"","location":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["evacuating-entity"]=subObj[0]
	tell_templateproperties["evacuated-entity"]=subObj[1]
	x.changeTemplateName("evacuate")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)
	
def fillDamageTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"cause":"","damaged-object":"","location":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["cause"]=subObj[0]
	tell_templateproperties["damaged-object"]=subObj[1]
	if subObj[0]=="":
		for token in dependencyDict:
			if WordNetLemmatizer().lemmatize(token.text ,'v') == intersectionWord:
				head=token.head
				i=0
				while(head.head in dependencyDict and i<=3):
					i+=1
					head=head.head
					if("nsubj" in dependencyDict[head]):
						tell_templateproperties["cause"]=findProperty(dependencyDict,head,True,"nsubj")
						break
			break
	x.changeTemplateName("damage")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)
	
def fillStrikeTemplate(word, sentence, intersectionSet):
	dependencyDict = {}
	intersectionWord = intersectionSet.pop()
	x = Template()
	x.changeSentence(sentence)
	tell_templateproperties = {"location":"","magnitude":"","time":"","disaster":""}
	sent = nlp(sentence)
	doc = nlp(sentence)
	for token in doc:
		if token.head not in dependencyDict:
			dependencyDict[token.head]={}
		dependencyDict[token.head][token.dep_] = token
	
	tell_templateproperties["time"] = findNamedEntity(sent,"DATE",dependencyDict)
	tell_templateproperties["location"] = findNamedEntity(sent,"GPE",dependencyDict)
	subObj=findSubjectObject(dependencyDict,intersectionWord)
	tell_templateproperties["disaster"]=subObj[0]
	mag=""
	for token in doc:
		if "magnitude" in token.text:
			exp=re.findall('\d+\.\d+',token.text)
			if(len(exp)>0):
				mag=exp[0]
				break
			elif token in dependencyDict and 'nummod' in dependencyDict[token]:
				mag=dependencyDict[token]['nummod']
				break
	tell_templateproperties["magnitude"]=mag
	x.changeTemplateName("strike")
	x.changeTemplateProperties(tell_templateproperties)
	filledTemplate.append(x)


	
def fillFullTemplate():
	filledTemplate.sort(key=lambda val: val.templateName)
	for template in filledTemplate:
		print(template.templateName+"("+str(template.filledTemplate)+")")
		#print(template.templateName)
#		print(template.sentence)
		print()
		
		

def getSentence(word):
	if word is None:
		with codecs.open("corpus.txt", 'r', encoding='utf-8', errors='ignore') as file:
			text=file.read()
	else:
		text=word
#	text = "I forced her to find the lock because I needed it"
#	print(text)
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
	
    #file.close()
	fillFullTemplate()

def getRelatedWordList():
	wordDefDict = {'occur':'happen.v.01','damage':'damage.v.01','visit':'visit.v.01','evacuate':'evacuate.v.01','force':'force.v.04','injure':'injure.v.01','trigger':'trip.v.04','strike':'hit.v.05','warn':'warn.v.01','experience':'experience.v.01','kill':'kill.v.01','record':'record.v.01','tell':'tell.v.02'}
	for filename in os.listdir(os.getcwd()+"/selectedVerbs"):
		wordList.append(filename.split('.')[0])
#	print(wordList)
	print()
	selectedWordListForTemplate = []
	for word in set(wordList):
#		print("\nWord: ",word)
#		print("______________________")
		synsets = wn.synsets(word)
		relatedWordList = []
		relatedWordList.append(word)
		for synset in synsets:
#			print(synset)
			#print(synset.definition)
			# print("Synset: {}".format(synset.name()))
#			print("Definition: {}".format(synset.definition()))
			if wordDefDict[word] in synset.name():
				#print("Synset: {}".format(synset.name()))
				#print("Synonyms: ")
				#for l in synset.lemmas(): 
				#	print("\t",l.name())
				#print("Definition: {}".format(synset.definition()))
				hyponyms = wn.synset(synset.name()).hyponyms()
				#print("Hyponyms: ")
				for hyponym in hyponyms:
					#print("\t",hyponym.name().split('.')[0])
					relatedWordList.append(hyponym.name().split('.')[0])
				hypernyms = wn.synset(synset.name()).hypernyms()
				#print("Hypernyms: ")
				for hypernym in hypernyms:
					if "damage" in synset.name():
						break
				#	print("\t",hypernym.name().split('.')[0])
					#relatedWordList.append(hypernym.name().split('.')[0])
				holonyms = wn.synset(synset.name()).part_holonyms()
#				print("Holonyms: ")
				for holonym in holonyms:
					#print("\t",holonym.name().split('.')[0])
					relatedWordList.append(holonym.name().split('.')[0])
				meronyms = wn.synset(synset.name()).part_meronyms()
				#print("Meronyms: ")
				for meronym in meronyms:
				#	print("\t",meronym.name().split('.')[0])
					relatedWordList.append(meronym.name().split('.')[0])
		#print("relatedWordList: ",relatedWordList)
		wordRelDict[word] = set(relatedWordList)


try:
    word=sys.argv[1]
except:
    word=None

wordList=[]
wordRelDict = {}
filledTemplate=[]
getRelatedWordList()
getSentence(word)