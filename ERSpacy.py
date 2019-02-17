import spacy
from spacy import displacy
nlp = spacy.load('en')
file = open("selectedsentences.txt","r")
text = nlp(file.read())
# text = nlp("The earthquake comes on the heels of a deadly typhoon lashing the west of Japan over the past few days")

for word in text.ents:
	print(word.text, word.label_)
displacy.serve(text,style="ent")
