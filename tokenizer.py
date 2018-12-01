# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 12:56:39 2018

@author: amal mohan, nayana thomas

tokenizer for text(tokenizes text to sentence and words)
"""

import nltk

nltk.download('punkt')

from nltk.tokenize import sent_tokenize,word_tokenize


def wordTokenizer(text):
    tokenizedWords=word_tokenize(text)
    return tokenizedWords

def sentenceTokenizer(text):
    tokenziedSentence=sent_tokenize(text)
    return tokenziedSentence
