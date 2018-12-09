# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 18:54:22 2018

@author: amal
"""

import os

from posTagger import wordPosTagger
from lemmatizer import verbLemmatizer,wordLemmatizer
#from operator import itemgetter
from tokenizer import sentenceTokenizer,wordTokenizer

def verbScoreCalculate():
    verbMap={}
    verbCount=0
    allVerbsCorpus=set()
    for filename in os.listdir(os.getcwd()+"\\corpus"):
        if '.txt' in filename:
            with open("corpus\\"+filename, 'r') as f:
                text=f.read()
                posTaggedwords = wordPosTagger(text)
                allVerbsTag=set(filter(lambda y: "VBG" in  y or "VB" in  y or "VBD" in  y or "VBN" in  y or "VBP" in  y or "VBZ" in  y,posTaggedwords))
                allVerbs=list(map(lambda y: y[0],allVerbsTag))
                allVerbsBaseForm=set(verbLemmatizer(allVerbs))
                allVerbsCorpus=allVerbsCorpus.union(allVerbsBaseForm)
                for verb in allVerbsBaseForm:
                    if verb in verbMap:
                        verbMap[verb]+=1
                    else:
                        verbMap[verb]=1
                verbCount+=len(allVerbsBaseForm)
    verbTuple=[(verbMap[k],k) for k in verbMap]
    verbTuple.sort(reverse=True)
    i=0
    sentenceMap={}
    for verb in allVerbsCorpus:
        sentenceMap[verb]=[]
    c=0
    for filename in os.listdir(os.getcwd()+"\\corpus"):
        if '.txt' in filename:
            with open("corpus\\"+filename, 'r') as f:
                text=f.read()
                sentences=sentenceTokenizer(text)
                for sentence in sentences:
                    posTaggedwords = wordPosTagger(sentence)
                    allVerbsTag=set(filter(lambda y: "VBG" in  y or "VB" in  y or "VBD" in  y or "VBN" in  y or "VBP" in  y or "VBZ" in  y,posTaggedwords))
                    allVerbs=list(map(lambda y: y[0],allVerbsTag))
                    allVerbsBaseForm=set(verbLemmatizer(allVerbs))
              #      print(allVerbsBaseForm)
                    
                    for allVerbs in allVerbsBaseForm:
                        if(allVerbs in sentenceMap):
                            sentenceMap[allVerbs].append(sentence)             
                        else:
                            c+=1
            
                
    for v,k in verbTuple:
        if(i==50):
            break
        with open("verbs\\"+str(v)+k+".txt","w") as fp:
            for sentence in sentenceMap[k]:
                fp.write(sentence)
                fp.write("\n\n")
#            fp.writelines(sentenceMap[k])
        #print(k,len(sentenceMap[k]))
#        for x in sentenceMap[k]:
 #           print(x)
        i=i+1
  #  print(c)
   # print(sentenceMap['lose'])
verbScoreCalculate()