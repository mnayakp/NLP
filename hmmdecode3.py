import json
import sys
TransitionProbability = {}
EmissionProbability = {}
Probability = {}
BackPointer = {}
inputArgument = sys.argv[1]
with open('hmmmodel.txt') as data_file:    
    OutputData = json.load(data_file)


TransitionProbability = json.loads(OutputData[0])
EmissionProbability = json.loads(OutputData[1])


with open(inputArgument,'r') as f:
	for line in f:
		WordsToBetagged = line.split()
		for q in TransitionProbability:
			Probability[q] = {}
			BackPointer[q] = {}

			if WordsToBetagged[0] in EmissionProbability and q in EmissionProbability[WordsToBetagged[0]]:
				Probability[q][1] = TransitionProbability["start"][q] + EmissionProbability[WordsToBetagged[0]][q]
				BackPointer[q][1] = "start"
			else:
				Probability[q][1] = TransitionProbability["start"][q] - 99999
				BackPointer[q][1] = "start"

		for t in range(2,len(WordsToBetagged) + 1):
			if WordsToBetagged[t-1] in EmissionProbability:
				for q in TransitionProbability:
					Probability[q][t] = float("-inf")
					BackPointer[q][t] = ""
					maxVal = float("-inf")
					maxInt = float("-inf")
					if q in EmissionProbability[WordsToBetagged[t-1]]:
						for qp in TransitionProbability:
							TempBackPointer =  Probability[qp][t-1] + TransitionProbability[qp][q]
							Temp = TempBackPointer + EmissionProbability[WordsToBetagged[t-1]][q]
							if Temp > maxInt:
								maxInt = Temp
								Probability[q][t] = Temp
							
							if TempBackPointer > maxVal:
								maxVal = TempBackPointer
								BackPointer[q][t] = qp
					
			else:
				for q in TransitionProbability:
					Probability[q][t] = float("-inf")
					BackPointer[q][t] = ""
					maxVal = float("-inf")
					maxInt = float("-inf")
					for qp in TransitionProbability:
						TempBackPointer =  Probability[qp][t-1] + TransitionProbability[qp][q]
						if TempBackPointer > maxInt:
							maxInt = TempBackPointer
							Probability[q][t] = TempBackPointer
						if TempBackPointer > maxVal:
							maxVal = TempBackPointer
							BackPointer[q][t] = qp
		maxProb = float("-inf")
		lastTime = len(WordsToBetagged)
		most_probable_state = ""
		for tag in TransitionProbability:
			if Probability[tag][lastTime] > maxProb:
				maxProb = Probability[tag][lastTime]
				most_probable_state = tag
		PointerPath = {}
		PointerPath[WordsToBetagged[lastTime-1]] = most_probable_state
		
		for t in range(lastTime-1,0,-1):
			PointerPath[WordsToBetagged[t-1]] = BackPointer[most_probable_state][t+1]
			most_probable_state = BackPointer[most_probable_state][t+1]
	
		StringPath = ""	
		for word in WordsToBetagged:
			StringPath += word + "/" + PointerPath[word] + " "
				
	
		with open("hmmoutput.txt",'a') as f:
			f.write(StringPath.strip() + "\n")
					


