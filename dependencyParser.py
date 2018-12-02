import spacy
from spacy import displacy
nlp = spacy.load('en')

def dependencyParse(text):
	doc = nlp(text)
	for token in doc:
		print("{0}/{1} <--{2}-- {3}/{4}".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))
	displacy.serve(doc, style='dep')
	# , jupyter=True, options={'distance': 90})