# import os
# num_words = 0
# for filename in os.listdir(os.getcwd()+"/corpus"):
# 	if '.txt' in filename:
# 		with open("corpus/"+filename, 'r', encoding='utf-8', errors='ignore') as f:
# 			for line in f:
# 				words = line.split()
# 				num_words += len(words)
# 			f.close()
# print("Number of words:")
# print(num_words)
		

import os
num_words = 0
with open("corpus.txt", 'r', encoding='utf-8', errors='ignore') as f:
	for line in f:
		words = line.split()
		num_words += len(words)
f.close()
print("Number of words:")
print(num_words)