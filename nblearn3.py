from __future__ import with_statement
import json
import fnmatch
import os
import sys
import re
from collections import Counter
import math

rootPath = sys.argv[1]
Class_List = ["positive","negative","deceptive","truthful"]
Dict_Classes_Tokens = {}
Dict_Tokens_Count = {}
Vocabulary_List =[]
   
Dict_Token_Probability = {}

def Tokenizer():
    for i in Class_List:
        global Dict_Classes_Tokens
        global Vocabulary_List    
        Dict_Classes_Tokens[i] = []
        for root, dirs, files in os.walk(rootPath):
            for filename in fnmatch.filter(dirs, "*" + i +"*"):
               for root_sub, dirs_sub, files_sub in os.walk(os.path.join(root, filename)):
                    for filename_sub in fnmatch.filter(files_sub,'*.txt'):
                        
                        file = open(os.path.join(root_sub, filename_sub),"r")
                        tokens = file.read().lower()
                        file.close()
                        tokens = re.sub('[^a-z]'," ", tokens)
                        tokens = tokens.split()                        
                       
                        Dict_Classes_Tokens[i] += tokens
                        
                        Vocabulary_List += tokens
        global Dict_Tokens_Count 
        Dict_Tokens_Count[i] = Counter(Dict_Classes_Tokens[i])
    
    Vocabulary_List = set(Vocabulary_List)

def Compute_Probability():
    for j in Class_List:
        Dict_Token_Probability[j] = {}
        token_count_len = float(len(Dict_Classes_Tokens[j])) 
        Vocab_Inc_one = float(len(Vocabulary_List)) 
        
        for item in Vocabulary_List:
            if item in Dict_Tokens_Count[j]: 
                probability = math.log((Dict_Tokens_Count[j][item] + 1)/(token_count_len + Vocab_Inc_one ))   
            else:
                probability = math.log(1 / (token_count_len + Vocab_Inc_one )) 
            Dict_Token_Probability[j][item] = probability
def main():
    Tokenizer()
    Compute_Probability()
    with open("nbmodel.txt", "w") as f:
        json.dump(Dict_Token_Probability,f, sort_keys=True, indent=4)
           
    
if __name__ == "__main__": main()
