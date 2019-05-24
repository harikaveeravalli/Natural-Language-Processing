# use this file to classify using perceptron classifier 
# Expected: generate percepoutput.txt
from __future__ import division
import glob
import os
import sys
import string


new_file = open("percepoutput.txt", "w")
listofclasses = ["positivetruthful", "positivedeceptive", "negativetruthful", "negativedeceptive"]
all_files = glob.glob(os.path.join(sys.argv[2], '*/*/*/*.txt'))
weight1 = {}
weight2 = {}
avgweight1 = {}
avgweight2 = {}
bias1 = 0
bias2 = 0
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves']

# get the weights and bias for words from the vaniilla perceptron model
def readdata():
    filedata = open(sys.argv[1], 'r')
    for eachline in filedata:
        dataread = eachline.strip().split(" ")
        if len(dataread) == 2:
            bias1 = dataread[0]
            bias2 = dataread[1]
        if len(dataread) == 3:
            weight1[dataread[0]] = float(dataread[1])
            weight2[dataread[0]] = float(dataread[2])


readdata()
# read the test data
for file in all_files:
    filename = str(file)
    filenamel = filename.lower()
    with open(filename, 'r') as file1:
        if "README" not in filenamel.upper():
            data = file1.read().replace('\n', ' ')
            data.lower()
            # to get the count of +ve and deceptive documents
            replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
            data = data.translate(replace_punctuation)
            # data = ''.join(ch for ch in data if ch not in set(string.punctuation))
            featurevector = {}
            wordtokens = data.split()
            for word in wordtokens:
                word1 = word.lower()
                if word1 not in stop_words:
                    if word1.isalpha():
                        if word1 not in featurevector:
                            featurevector[word1] = 1
                        else:
                            featurevector[word1] += 1
            # calculate the activation value for the given review
            activationsum = bias1
            activationsum2 = bias2
    
            for word1 in featurevector:
                if word1 in weight1:
                    activationsum += weight1[word1]
                if word1 in weight2:
                    activationsum2 += weight2[word1]
            if activationsum > 0 and activationsum2 > 0 :
                new_file.write("truthful"+" "+"positive"+" "+filename)
                new_file.write("\n")
            elif activationsum < 0 and activationsum2 < 0:
                new_file.write("deceptive"+" "+"negative"+" "+filename)
                new_file.write("\n")
            elif activationsum > 0 and activationsum2 < 0:
                new_file.write("deceptive" + " " + "positive" + " " + filename)
                new_file.write("\n")
            elif activationsum < 0 and activationsum2 > 0:
                new_file.write("truthful" + " " + "negative" + " " + filename)
                new_file.write("\n")




if __name__ == "__main__":
    model_file = str(sys.argv[1])
    output_file = "percepoutput.txt"
    input_path = str(sys.argv[2])