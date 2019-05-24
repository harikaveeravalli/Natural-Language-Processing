import sys
import json
import glob
import os
import math
import ast

output_file="hmmoutput.txt"
model_file="hmmmodel.txt"
transitionprobabilities = {}
emissionprobability = {}
globaldictionary = {}
tag_count = {}
viterbialgo = {}
backpointer = {}
#json_data = []
#file1=[]
# get the details from the file
with open(model_file,"r") as modeldata:
    data = modeldata.read()
    all_dict = ast.literal_eval(data)
    transitionprobabilities = all_dict['transition_prob']
    emissionprobability = all_dict['emission_prob']
    tag_count = all_dict['tag_count']
    globaldictionary = all_dict['globaldict']
    lasttagcount = all_dict['lasttagcount']

new_file = open("hmmoutput.txt", "w")

def write_output(finaltaglist, sentencelength, wordlist):

    newsentence = ""
    insertspace = " "
    for i in range(0, sentencelength):
        if i != sentencelength-1:
            newsentence += wordlist[i]+"/"+finaltaglist[i]+insertspace
        else:
            newsentence += wordlist[i]+"/"+finaltaglist[i]
    new_file.write(newsentence)
    new_file.write("\n")

    
def calculate():

    file1 = open(sys.argv[1], mode='r',encoding='utf-8')
    data = file1.read()
    sentences = data.splitlines()
    for sentence in sentences:

        sentencelength = len(sentence.split(' '))
        counter = 0
        wordlist = sentence.split(' ')
        
        for j in range(0, sentencelength):
            backpointer[j] = {}
            viterbialgo[j] = {}
        for word in sentence.split(' '):
            if counter == 0:
                for tag in tag_count:
                    if word in emissionprobability:
                        if tag in emissionprobability[word]:
                            viterbialgo[0][tag] = transitionprobabilities['START_STATE'][tag]*emissionprobability[word][tag]
                            backpointer[0][tag] = ""
                        else:
                            viterbialgo[0][tag] = transitionprobabilities['START_STATE'][tag]
                            backpointer[0][tag] = ""
                    else:
                        viterbialgo[0][tag] = transitionprobabilities['START_STATE'][tag]
                        #viterbialgo[0][tag] = transitionprobabilities['START_STATE'][tag] * (
                        #                    0 / float(len(tag_count) + tag_count[tag]))
                        backpointer[0][tag] = ""

            counter = counter + 1

        for val in range(1, sentencelength):
            prevparenttag = ""
            calculateprob = 0
            for tag1 in tag_count:
                        # print "tag1", tag1
                maxvalue = float("-inf")
                for secondtag in tag_count:

                    calculateprob = viterbialgo[val - 1][secondtag] * transitionprobabilities[secondtag][tag1]
                    if calculateprob > maxvalue:
                        maxvalue = calculateprob
                        prevparenttag = secondtag

                if wordlist[val] in emissionprobability:
                    if tag1 in emissionprobability[wordlist[val]]:
                        viterbialgo[val][tag1] = maxvalue * emissionprobability[wordlist[val]][tag1]
                        backpointer[val][tag1] = prevparenttag
                    else:
                        viterbialgo[val][tag1] = maxvalue
                        backpointer[val][tag1] = prevparenttag
                else:
                    viterbialgo[val][tag1] = maxvalue
                    backpointer[val][tag1] = prevparenttag


        finaltag = ""
        finaltaglist = []
        #print(viterbialgo)
        maxx = float("-inf")
        ttag = ""
        for t in tag_count:
            if viterbialgo[sentencelength - 1][t] > maxx:
                maxx = viterbialgo[sentencelength-1][t]
                tagg = t


        end_tag = tagg
        finaltaglist = []
        finaltaglist.append(tagg)

        for counter in range((sentencelength - 1), 0, -1):
                    # print(counter)
            backtag = backpointer[counter][end_tag]
            finaltaglist.append(backtag)
            end_tag = backtag

        finaltaglist.reverse()

        write_output(finaltaglist, sentencelength, wordlist)


calculate()


if __name__=="__main__":
    input_file = sys.argv[1]
    #print(input_file)



    
