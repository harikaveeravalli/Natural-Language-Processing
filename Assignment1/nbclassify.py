# use this file to classify using naive-bayes classifier 
# Expected: generate nboutput.txt
from __future__ import division
import glob
import os
import sys
import string

new_file = open("nboutput.txt", "w")
listofclasses = ["positivetruthful", "positivedeceptive", "negativetruthful", "negativedeceptive"]
all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))

stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves']

condprob = {}
priorprobability={}
classifysum={}

def readdata():
    filedata = open('nbmodel.txt', 'r')
    for eachline in filedata:
        dataread = eachline.strip().split(" ")
        if len(dataread) == 4:
            priorprobability['positivetruthful'] = float(dataread[0])
            priorprobability['positivedeceptive'] = float(dataread[1])
            priorprobability['negativetruthful'] = float(dataread[2])
            priorprobability['negativedeceptive'] = float(dataread[3])
        elif len(dataread) == 5:
            condprob[dataread[0]] = [float(dataread[1]), float(dataread[2]), float(dataread[3]), float(dataread[4])]

#read the nbmodel.txt file
readdata()
correct = 0
documentcount = 0
for file in all_files:
    filename = str(file)
    for c in listofclasses:
        classifysum[c] = priorprobability[c]
    #print filename
    #readme should not be used for learning or classifying the .txt files
    temp = filename
    temp1 = temp.upper()
    if filename.endswith(".txt") and "README" not in temp1:
        #if "fold1" in filename:
        filenamel = filename.lower()
            # separate out the fold1 data that is going to be used as development data
        documentcount += 1
        with open(filename, 'r') as file1:
            data = file1.read().replace('\n', ' ')
            data.lower()
            replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
            data = data.translate(replace_punctuation)
            wordtokens = [word for word in data.split() if word not in stop_words]
                #print wordtokens
            postruth = priorprobability['positivetruthful']
            posdecep = priorprobability['positivedeceptive']
            negtruth = priorprobability['negativetruthful']
            negdecep = priorprobability['negativedeceptive']
            for word1 in wordtokens:
                if word1 in condprob:
                    postruth += condprob[word1][0]
                    posdecep += condprob[word1][1]
                    negtruth += condprob[word1][2]
                    negdecep += condprob[word1][3]
            max_value = max(postruth, posdecep, negtruth, negdecep)
            #print max_value

            predictclass=""
            llist = []
            llist.append(postruth)
            llist.append(posdecep)
            llist.append(negtruth)
            llist.append(negdecep)
            max_value = llist[0]
            index = 0
            for val in llist:
                #print "entered the for loop"
                if max_value < val:
                    max_value = val
                    index = llist.index(max_value)
                    #print "entered", index
                        #print index

                #index = classifysum[max_value]
            if index == 0:
                predictclass = "truthful positive"
                new_file.write(predictclass + " " + filename + "\n")


            elif index == 1:
                predictclass = "deceptive positive"
                new_file.write(predictclass + " " + filename + "\n")


            elif index == 2:
                predictclass = "truthful negative"
                new_file.write(predictclass + " " + filename + "\n")


            elif index == 3:
                predictclass = "deceptive negative"
                new_file.write(predictclass + " " + filename + "\n")


if __name__ == "main":
    model_file = "nbmodel.txt"
    output_file = "nboutput.txt"
    input_path = str(sys.argv[1])