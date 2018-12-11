# # -*- coding: utf-8 -*-
# """
# Created on Sat Dec 01 13:27:52 2018

# @author: amal
# """

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def wordLemmatizer(wordList):
    lemmatizer=WordNetLemmatizer()
    lemmatized_output = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in wordList]
    return lemmatized_output

def verbLemmatizer(wordList):
    lemmatizer=WordNetLemmatizer()
    lemmatized_output = [lemmatizer.lemmatize(word, 'v') for word in wordList]
    return lemmatized_output
