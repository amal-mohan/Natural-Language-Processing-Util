import os
import codecs
text = ""
for filename in os.listdir(os.getcwd()+"/corpus"):
	if '.txt' in filename:
		with codecs.open("corpus/"+filename, 'r', encoding='utf-8', errors='ignore') as f:
			text= text+f.read()
with codecs.open("corpus.txt", 'w', encoding='utf-8', errors='ignore') as file:
	file.write(text)           
