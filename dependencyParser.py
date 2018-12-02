import spacy
from spacy import displacy
nlp = spacy.load('en')

def dependencyParse(text):
	doc = nlp(text)
	for token in doc:
		print("{0}/{1} <--{2}-- {3}/{4}".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))
	sentence_spans = list(doc.sents)
	options = {'compact': True, 'bg': '#09a3d5',
           'color': 'white', 'font': 'Source Sans Pro'}
    # options = {'compact': True,
    #        'color': 'black', 'font': 'Source Sans Pro'}
	displacy.serve(sentence_spans, style='dep', options=options)
	# , jupyter=True, options={'distance': 90})