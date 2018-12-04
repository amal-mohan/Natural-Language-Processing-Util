# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 18:54:22 2018

@author: amal
"""

import os

from posTagger import wordPosTagger
from lemmatizer import verbLemmatizer
#from operator import itemgetter
from tokenizer import wordTokenizer

def verbScoreCalculate():
    verbMap={}
    verbCount=0
    for filename in os.listdir(os.getcwd()+"\\corpus"):
        if '.txt' in filename:
            with open("corpus\\"+filename, 'r') as f:
                text=f.read()
                posTaggedwords = wordPosTagger(text)
                allVerbsTag=set(filter(lambda y: "VBG" in  y or "VB" in  y or "VBD" in  y or "VBN" in  y or "VBP" in  y or "VBZ" in  y,posTaggedwords))
                allVerbs=list(map(lambda y: y[0],allVerbsTag))
                allVerbsBaseForm=set(verbLemmatizer(allVerbs))
                for verb in allVerbsBaseForm:
                    if verb in verbMap:
                        verbMap[verb]+=1
                    else:
                        verbMap[verb]=1
                verbCount+=len(allVerbsBaseForm)
    verbTuple=[(verbMap[k],k) for k in verbMap]
    verbTuple.sort(reverse=True)
    i=0
   # sentenceMap={}
    for filename in os.listdir(os.getcwd()+"\\corpus"):
        if '.txt' in filename:
            with open("corpus\\"+filename, 'r') as f:
                text=f.read()
                
    
    for v,k in verbTuple:
        if(i==50):
            break
        print(v,k)
        i=i+1
    
verbScoreCalculate()