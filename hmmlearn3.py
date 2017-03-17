import sys
import math
import json
inputArgument = sys.argv[1]

Dict_Words = {}  
Dict_Tags = {}

WordOfTag_Frequency = {}
TagOfTag_Frequency = {}
TransitionProbability = {}
EmissionProbability = {}
count = 0
InitialTag = "start"
with open(inputArgument,'r') as f:
	for line in f:
		count += 1
		WordTagPair = line.split()
		FirstTag = WordTagPair[0].rsplit("/",1)[1]
		if InitialTag not in TagOfTag_Frequency:
			TagOfTag_Frequency[InitialTag] = {}
		TagOfTag_Frequency[InitialTag][FirstTag] = TagOfTag_Frequency[InitialTag].setdefault(FirstTag,0) + 1
		
		for each_pair in WordTagPair:
			word,tag = each_pair.rsplit("/",1)
			Dict_Words[word] = Dict_Words.setdefault(word, 0) + 1
			Dict_Tags[tag] = Dict_Tags.setdefault(tag, 0) + 1
			if word not in WordOfTag_Frequency:
				WordOfTag_Frequency[word] = {}
			WordOfTag_Frequency[word][tag] = WordOfTag_Frequency[word].setdefault(tag,0) + 1
		

		for i in range(len(WordTagPair) - 1):
			word_tag_pairOne = WordTagPair[i]
			word_tag_pairTwo = WordTagPair[i+1]
			tagOne =  word_tag_pairOne.rsplit("/",1)[1] 
			tagTwo =  word_tag_pairTwo.rsplit("/",1)[1]
			if tagOne not in TagOfTag_Frequency:
				TagOfTag_Frequency[tagOne] = {}
			TagOfTag_Frequency[tagOne][tagTwo] = TagOfTag_Frequency[tagOne].setdefault(tagTwo,0) + 1

Dict_Tags[InitialTag] = count		
for tag in Dict_Tags:
	TransitionProbability[tag] = {}
	for tagAdj in Dict_Tags:
		if tagAdj not in TagOfTag_Frequency[tag]:
			TransitionProbability[tag][tagAdj] = math.log(1/(Dict_Tags[tag] + len(Dict_Tags)))
		else:
			TransitionProbability[tag][tagAdj] = math.log((TagOfTag_Frequency[tag][tagAdj] + 1)/(Dict_Tags[tag] + len(Dict_Tags)))

for word in Dict_Words:
	EmissionProbability[word] = {}
	for tag in WordOfTag_Frequency[word]:
		EmissionProbability[word][tag] = math.log(WordOfTag_Frequency[word][tag]/Dict_Tags[tag])


Probability_List = [json.dumps(TransitionProbability,ensure_ascii=False),json.dumps(EmissionProbability,ensure_ascii=False)]

with open("hmmmodel.txt",'w') as f:
	json.dump(Probability_List,f,ensure_ascii=False)
	
	
	
	
	
	
	
	
	
	
