# # -*- coding: utf-8 -*-
# """
# Created on Sat Dec 01 13:27:52 2018

# @author: amal, nayana
# """

import nltk
from nltk.tokenize import word_tokenize
def wordPosTagger(text):
	tokenizedWords=word_tokenize(text)
	return nltk.pos_tag(tokenizedWords)
