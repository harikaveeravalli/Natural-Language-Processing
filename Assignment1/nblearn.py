# use this file to learn naive-bayes classifier 
# Expected: generate nbmodel.txt
from __future__ import division
import sys
import glob
import os
import string
import math
#t0 = time.time()
x=0
PTdictcount = int(0)
PDdictcount = int(0)
NTdictcount = int(0)
NDdictcount = int(0)
combinedDict = {}
combinedDict['positivetruthful'] = {}
combinedDict['positivedeceptive'] = {}
combinedDict['negativetruthful'] = {}
combinedDict['negativedeceptive'] = {}

#to Store log probabilities
logpriorprobability={}
#logpriorprobability = {"positivetruthful": 0.0, "positivedeceptive": 0.0, "negativetruthful": 0.0, "negativedeceptive": 0.0}
#count for the number of documents
listofclasses = ['positivetruthful', 'positivedeceptive', 'negativetruthful', 'negativedeceptive']
documentcount = 0
#set of all unique words in the from .txt file

vocabulary = set()

stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves']

all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))

for file in all_files:
    filename = str(file)
    #print filename
    temp = filename
    temp1 = temp.upper()

    if filename.endswith(".txt") and 'README' not in temp1:
        filenamel = filename.lower()

        #if "fold1" not in filenamel:
        if "positive" in filenamel:
            if "truthful" in filenamel:
                with open(filename, 'r') as file1:
                    data = file1.read().replace('\n', ' ')
                    documentcount += 1
                    data.lower()
                    # to get the count of +ve and deceptive documents
                    PTdictcount += 1
                    replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
                    data = data.translate(replace_punctuation)
                        #data = ''.join(ch for ch in data if ch not in set(string.punctuation))
                    wordtokens = data.split()
                    for word in wordtokens:
                        word1 = word.lower()
                        if word1 not in stop_words:
                            if word1.isalpha():
                                    #check if word contains numbers
                                if word1 not in vocabulary:
                                    vocabulary.add(word1)
                                if word1 in combinedDict['positivetruthful']:
                                    combinedDict['positivetruthful'][word1] += 1
                                elif word1 not in combinedDict['positivetruthful']:
                                    combinedDict['positivetruthful'][word1] = 1
            elif "deceptive" in filenamel:
                with open(filename, 'r') as file1:
                    PDdictcount += 1
                    data = file1.read().replace('\n',' ')
                    documentcount += 1
                    data.lower()
                    data = ''.join(ch for ch in data if ch not in set(string.punctuation))
                    wordtokens = data.split()
                    for word in wordtokens:
                        word1 = word.lower()
                        if word1 not in stop_words:
                            if word1.isalpha():
                                    #PositiveDeceptiveDict[word1] += 1
                                   # combinedDict['positivedeceptive'][word1] +=1
                                if word1 not in vocabulary:
                                    vocabulary.add(word1)
                                if word1 in combinedDict['positivedeceptive']:
                                    combinedDict['positivedeceptive'][word1] += 1
                                elif word1 not in combinedDict['positivedeceptive']:
                                    combinedDict['positivedeceptive'][word1] = 1
        if "negative" in filenamel:
            if "truthful" in filenamel:
                with open(filename, 'r') as file1:
                    NTdictcount += 1
                    data = file1.read().replace('\n', ' ')
                    documentcount += 1
                    data.lower()
                    data = ''.join(ch for ch in data if ch not in set(string.punctuation))
                    wordtokens = data.split()
                    for word in wordtokens:
                        word1 = word.lower()
                        if word1 not in stop_words:
                            if word1.isalpha():
                                    #NegativeTruthfulDict[word1] += 1
                                if word1 not in vocabulary:
                                    vocabulary.add(word1)
                                if word1 in combinedDict['negativetruthful']:
                                    combinedDict['negativetruthful'][word1] += 1
                                elif word1 not in combinedDict['negativetruthful']:
                                    combinedDict['negativetruthful'][word1] = 1
            elif "deceptive" in filenamel:
                with open(filename, 'r') as file1:
                    NDdictcount += 1
                    data = file1.read().replace('\n', ' ')
                    documentcount += 1
                    data.lower()
                    data = ''.join(ch for ch in data if ch not in set(string.punctuation))
                    wordtokens = data.split()
                    for word in wordtokens:
                        word1 = word.lower()
                        if word1 not in stop_words:
                            #preprocessing: eliminating stop words and non-alphabetic characters from the strings
                            if word1.isalpha():
                                    #NegativeDeceptiveDict[word1] += 1
                                if word1 not in vocabulary:
                                    vocabulary.add(word1)
                                if word1 in combinedDict['negativedeceptive']:
                                    combinedDict['negativedeceptive'][word1] += 1
                                elif word1 not in combinedDict['negativedeceptive']:
                                    combinedDict['negativedeceptive'][word1] = 1



#print "document count", documentcount

# calculate prior probability of each class


def priorprobability():

    priorPT = PTdictcount/documentcount
    logpriorprobability["positivetruthful"] = math.log(priorPT)
    priorPD = PDdictcount/documentcount
    logpriorprobability["postivedeceptive"] = math.log(priorPD)
    priorNT = NTdictcount / documentcount
    logpriorprobability["negativetruthful"] = math.log(priorNT)
    priorND = NDdictcount / documentcount
    logpriorprobability["negativedeceptive"] = math.log(priorND)


priorprobability()
count = 0
# calculating the conditional probability
condprob = {}
condprob[''] = {}

#add 0 for words that don't occur in the given the given class
for c in listofclasses:
    for word in vocabulary:
        if word not in combinedDict[c]:
            combinedDict[c][word] = 0

#calculating the count(w,c), for every class
sumofwords={}
for c in listofclasses:
    sumofwords[c] = 0
    condprob[c] = {}

for c in listofclasses:

    for word in vocabulary:
        if word in combinedDict[c]:
            sumofwords[c] += combinedDict[c][word]
    #print c, "sum value,", sumofwords[c]
# calculating the log-likelihood probabilities for every class and storing them in condprob matrix
for c in listofclasses:
    for word in vocabulary:
        #if word in combinedDict[c]:
            #print "global dict count", combinedDict[c][word]

        condprob[c][word] = math.log((combinedDict[c][word]+1)/(sumofwords[c]+(len(vocabulary))))
            #if(condprob[c][word] > 0):
            #print "conditional probability", word, condprob[c][word]

#t1 = time.time()



#writing prior probabilitites
new_file = open("nbmodel.txt","w")
for key, value in logpriorprobability.items():
    new_file.write(str(value) + " ")
new_file.write("\n")

#writing the words and conditional probababilities in python
for word in vocabulary:
    new_file.write(word+" ")
    for c in listofclasses:
        if word in condprob[c]:
            new_file.write(str(condprob[c][word])+" ")
    new_file.write("\n")
new_file.close()

if __name__ == "main":
    model_file = "nbmodel.txt"
    input_path = str(sys.argv[1])