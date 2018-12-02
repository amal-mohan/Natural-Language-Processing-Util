import nltk
from nltk.tokenize import word_tokenize
def wordPosTagger(text):
	tokenizedWords=word_tokenize(text)
	return nltk.pos_tag(tokenizedWords)
