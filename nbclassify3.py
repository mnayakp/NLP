from __future__ import with_statement
import json
import fnmatch
import os
import sys
import re

import math


Class_List = ["negative","positive","truthful","deceptive"]
inputPath = sys.argv[1]

with open('nbmodel.txt') as data_file:
    data = json.load(data_file)

with open("nboutput.txt", "w") as f:
    for root, dirs, files in os.walk(inputPath):
          
        for testFileName in fnmatch.filter(files,'*.txt'):
            file = open(os.path.join(root, testFileName),"r")
            tokens = file.read().lower()
            file.close()
            tokens = re.sub('[^a-z]'," ", tokens)
            tokens = tokens.split() 
           
            Likelihood = {}
            for i in Class_List:
                Likelihood[i] = math.log(0.5) 
                for word in tokens:
                    if word in data[i]:
                        Likelihood[i] += data[i][word] 
                
                
            if Likelihood["negative"] <= Likelihood["positive"]:
                label_b = "positive"
            else:
                label_b = "negative"
                
            if Likelihood["truthful"] >= Likelihood["deceptive"]:
                label_a = "truthful"
            else:
                label_a = "deceptive"        
                
          
            f.write(label_a + " " + label_b + " " + os.path.join(root, testFileName)+"\n") 