# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 12:56:39 2018

@author: amal mohan, nayana thomas

tokenizer for text(tokenizes text to sentence and words)
"""

import nltk

nltk.download('wordnet')
nltk.download('punkt')


from nltk.tokenize import sent_tokenize,word_tokenize


def wordSentenceTokenizer(text):
    sent_tk=sent_tokenize(text)
    word_tk=word_tokenize(text)
    print(sent_tk)
    print(word_tk)


