import sys

def permutation(anagram,input_phrase):
	n = len(input_phrase)
	if n==0:
		L.append(anagram)		
	else:
		for x in range(len(input_phrase)):
			permutation(anagram + input_phrase[x],input_phrase[0:x] + input_phrase[x+1:])

file = open('anagram_out.txt' , 'w')	
L = []		
permutation("",sys.argv[1])
output = L.sort()
for item in L:
		file.write("%s\n" % item)
file.close()