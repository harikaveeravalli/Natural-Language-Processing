# use this file to learn perceptron classifier 
# Expected: generate vanillamodel.txt and averagemodel.txt
import glob
import os
import sys
import string
import random
datalist = []
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
vocabulary = set()
all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
# Creating the vocabulary
# Read the files
weights1 = {}
weights2 = {}
avgweights1 = {}
avgweights2 = {}
featurevector = {} #contains the features and the corresponding occurence counts
updatedweights1 = {}
updatedweights2 = {}
global y1 #for truthful and deceptive
global y2 #for positive / negative
global bias1
global bias2
bias1 = 0
bias2 = 0
global avgbias1
global avgbias2
avgbias1 = 0
avgbias2 = 0
global count1
count1 = 0

def createvocabulary(all_files):
    global count1
    for file in all_files:
        filename = str(file)
        foldname1 = filename.lower()
        with open(filename, 'r') as file1:
            count1 += 1
            #if "fold1" not in foldname1:
            data = file1.read().replace('\n', ' ')
            data.lower()
            replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
            data = data.translate(replace_punctuation)
            # data = ''.join(ch for ch in data if ch not in set(string.punctuation))
            wordtokens = data.split()
            for word in wordtokens:
                word1 = word.lower()
                if word1 not in stop_words:
                    if word1.isalpha():
                        if word1 not in vocabulary:
                            vocabulary.add(word1)

createvocabulary(all_files)
#print len(vocabulary)
#print count1
for word in vocabulary:
    weights1[word] = 0
    weights2[word] = 0
    avgweights1[word] = 0
    avgweights2[word] = 0
    updatedweights1[word] = 0
    updatedweights2[word] = 0

def readfiles(all_files):
    for file in all_files:
        filename = str(file)
        with open(filename, 'r') as file1:
            data = file1.read().replace('\n', ' ')
            data.lower()
            replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
            data = data.translate(replace_punctuation)
            filename1 = filename.lower()
            subdatalist=[]
            if 'README' not in filename1:
                if "positive" in filename1:
                    if "truthful" in filename1:
                        subdatalist.append("positive")
                        subdatalist.append("truthful")
                        subdatalist.append(data)
                        datalist.append(subdatalist)
                if "positive" in filename1:
                    if "deceptive" in filename1:
                        subdatalist.append("positive")
                        subdatalist.append("deceptive")
                        subdatalist.append(data)
                        datalist.append(subdatalist)
                if "negative" in filename1:
                    if "truthful" in filename1:
                        subdatalist.append("negative")
                        subdatalist.append("truthful")
                        subdatalist.append(data)
                        datalist.append(subdatalist)
                if "negative" in filename1:
                    if "deceptive" in filename1:
                        subdatalist.append("negative")
                        subdatalist.append("deceptive")
                        subdatalist.append(data)
                        datalist.append(subdatalist)


readfiles(all_files)
#print datalist[0][0]
#print datalist[5][1]
#print datalist[10][2]



#calculating the activation and updating the vaniilla perceptron


def calculateActivation(featurevector,weights1,weights2,y1,y2,counter):
    global bias1
    global bias2
    global avgbias1
    global avgbias2
    activationsum1 = 0
    #print "bias1", bias1
    #print "bias2", bias2
    #for weights1 and class y1 (truthful/deceptive)
    for word in featurevector:
        if word in weights1:
            activationsum1 += featurevector[word]*weights1[word]
    activationsum1 += bias1

    if y1*activationsum1 <= 0:
        for word in featurevector:
            if word in weights1:
                weights1[word] = weights1[word] + y1*featurevector[word]
            if word in avgweights1:
                avgweights1[word] = avgweights1[word] + y1*counter*featurevector[word]

        avgbias1 += y1*counter
        bias1 += y1
    #for weights2 and class y2 (positive/negative)
    activationsum2 = 0

    for word in featurevector:
        if word in weights2:
            activationsum2 += featurevector[word]*weights2[word]
    activationsum2 += bias2

    if y2*activationsum2 <= 0:
        for word in featurevector:
            if word in weights2:
                weights2[word] = weights2[word] + y2*featurevector[word]
            if word in avgweights2:
                avgweights2[word] = avgweights2[word] + y2*counter*featurevector[word]

        avgbias2 += y2*counter
        bias2 += y2

iterations = 0

counter = 1
while iterations < 40:
    global y1
    global y2
    random.shuffle(datalist)
    for i in range(0, len(datalist)):
        if datalist[i][0] == 'positive':
            y1 = 1
        elif datalist[i][0] == 'negative':
            y1 = -1
        if datalist[i][1] == 'truthful':
            y2 = 1
        elif datalist[i][1] == 'deceptive':
            y2 = -1

            # data = ''.join(ch for ch in data if ch not in set(string.punctuation))
        data = datalist[i][2]
        wordtokens = data.split()
        featurevector = {}

        for word in wordtokens:
            word1 = word.lower()
            if word1 not in stop_words:
                if word1.isalpha():
                        # check if word contains numbers
                    if word1 not in featurevector:
                        featurevector[word1] = 1
                    elif word1 in featurevector:
                        featurevector[word1] += 1
        calculateActivation(featurevector, weights1, weights2, y1, y2, counter)
        counter = counter + 1

    iterations += 1

#print "counter value", counter
# final average weights
for word in avgweights1:
    div_value = (float)(avgweights1[word])
    updatedweights1[word] = weights1[word] - (div_value/counter)
            #print word,updatedweights1[word]
for word in avgweights2:
    div_value2 = (float)(avgweights2[word])
    updatedweights2[word] = weights2[word] - (div_value2/counter)
            #print word, updatedweights2[word]

#finding the average bias values
fordiv_b1 = (float)(avgbias1)
fordiv_b2 = (float)(avgbias2)
finalbias1 = (bias1 - (fordiv_b1/counter))
finalbias2 = (bias2 - (fordiv_b2/counter))


#righting data into the file
writefile = open("vanillamodel.txt", "w")
writefile.write(str(bias1) + " ")
writefile.write(str(bias2) + " ")
writefile.write("\n")

for word in vocabulary:

    writefile.write(word+" "+str(weights1[word])+" "+str(weights2[word]))
    writefile.write("\n")

writefile2 = open("averagemodel.txt", "w")
writefile2.write(str(finalbias1) + " ")
writefile2.write(str(finalbias2) + " ")
writefile2.write("\n")

for word in vocabulary:

    writefile2.write(word+" "+str(updatedweights1[word])+" "+str(updatedweights2[word]))
    writefile2.write("\n")

if __name__ == "__main__":
    model_file = "vanillamodel.txt"
    avg_model_file = "averagemodel.txt"
    
    input_path = str(sys.argv[1])