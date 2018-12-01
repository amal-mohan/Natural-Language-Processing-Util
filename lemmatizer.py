# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 13:27:52 2018

@author: amal
"""

import nltk

nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

def wordLemmatizer(wordList):
    lemmatizer=WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in wordList] 