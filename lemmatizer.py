# # -*- coding: utf-8 -*-
# """
# Created on Sat Dec 01 13:27:52 2018

# @author: amal
# """

import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.stem import WordNetLemmatizer

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    print(nltk.pos_tag([word]))
    print(tag)
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def wordLemmatizer(wordList):
    lemmatizer=WordNetLemmatizer()
    lemmatized_output = ' '.join(lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in wordList)
    print(lemmatized_output)
    return lemmatized_output
    
