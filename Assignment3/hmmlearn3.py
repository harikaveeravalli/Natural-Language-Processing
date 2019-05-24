import glob
import os
import sys
output_file="hmmoutput.txt"
model_file="hmmmodel.txt"
#all_files = glob.glob(os.path.join(sys.argv[1], '*.txt'))
wordtag = []
wordlist = []
taglist = []
tagdict = {}
globaldict = {}
wordset = set()
totaltagcount = {}
#all_files = glob.glob(os.path.join(sys.argv[1], '*.txt'))
transitionprobcount = {}
transitionProbability = {}
emission_probability = {}
global start_state_count
start_state_count = 0
last_word_set = set()
last_tag_count = {}
startToTagCount = {}
transition_Tag = {} # gives the denominator for transition probabilities
# read the data and create wordlist and taglist of the entire data available
smoothing_factor = 0


def readfile():
    global start_state_count
    file1 = open(sys.argv[1], mode='r', encoding='utf-8')
    data = file1.read()
    sentences = data.splitlines()
    for sentence in sentences:
        counter = 0
        start_state_count = start_state_count + 1
        prevtag = "START_STATE"
        sentencelength = len(sentence.split(" "))
        for wordtag in sentence.split(" "):

            extractdata = wordtag.rsplit('/', 1)

            word = extractdata[0]
            tag = extractdata[1]

            currenttag = tag
            if prevtag == "START_STATE":
                currenttag = tag

                #calculate no of type of tags from start state
                if currenttag in startToTagCount:
                    startToTagCount[currenttag] += 1
                else:
                    startToTagCount[currenttag] = 1

            wordlist.append(extractdata[0])
            wordset.add(extractdata[0])
            taglist.append(extractdata[1])


            # total tag counts including the end states
            if tag in totaltagcount:
                totaltagcount[tag] += 1
            else:
                totaltagcount[tag] = 1
             #count of tags other than the last tag that will not have transition probabilities

            if counter != sentencelength-1:
                if tag in tagdict:
                    tagdict[tag] += 1
                else:
                    tagdict[tag] = 1

            for tag1 in totaltagcount:
                if tag1 not in transitionprobcount:
                    transitionprobcount[tag1] = {}
            if word in globaldict:
                if tag in globaldict[word]:
                    globaldict[word][tag] = globaldict[word][tag] + 1
                else:
                    globaldict[word][tag] = 1
            else:
                globaldict[word] = {}
                if tag in globaldict[word]:
                    globaldict[word][tag] += 1
                else:
                    globaldict[word][tag] = 1

            if prevtag in transitionprobcount:
                if currenttag in transitionprobcount[prevtag]:
                    transitionprobcount[prevtag][currenttag] += 1
                else:
                    transitionprobcount[prevtag][currenttag] = 1
            else:

                transitionprobcount[prevtag] = {}
                if currenttag in transitionprobcount[prevtag]:
                    transitionprobcount[prevtag][currenttag] += 1
                else:
                    transitionprobcount[prevtag][currenttag] = 1
            prevtag = tag

            if tag in transition_Tag:
                transition_Tag[tag] += 1
            else:
                transition_Tag[tag] = 1

            if counter == sentencelength-1:
                if tag in last_tag_count:
                    last_tag_count[tag] += 1
                else:
                    last_tag_count[tag] = 1

                if word not in last_word_set:
                    last_word_set.add(word)
            counter = counter + 1

def transition_endstate():

    tagdict_count = len(totaltagcount)  #with end state
    for tag in last_tag_count:
        transitionProbability[tag] = {}
    last_State = "END_STATE"

    #without smoothing
    for tag in totaltagcount:

        if tag in last_tag_count:
            transitionProbability[tag][last_State] = (last_tag_count[tag] + 1)/(float(start_state_count+tagdict_count))
        else:
            transitionProbability[tag][last_State] = 1/(float(start_state_count+tagdict_count))

    #with smoothing

    if smoothing_factor == 1:
        for tag in totaltagcount:
            if tag in last_tag_count:
                transitionProbability[tag][last_State] = (last_tag_count[tag])/(float(start_state_count))
            else:
                transitionProbability[tag][last_State] = 0/(float(start_state_count))


def calculate_transition():


    transitionProbability['START_STATE'] = {}
    # transition from start state to rest of the states
    for tag in totaltagcount:
        if tag not in transitionProbability['START_STATE']:
            if tag in startToTagCount:
                #transitionProbability['START_STATE'][tag] = ((startToTagCount[tag])/float(start_state_count))
                transitionProbability['START_STATE'][tag] = ((startToTagCount[tag] + 1) / float(start_state_count + len(totaltagcount)))
            else:
                transitionProbability['START_STATE'][tag] = (1/(float(start_state_count + len(totaltagcount))))
    # for rest of the states
    for tag in totaltagcount:
        transitionProbability[tag] = {}
        for secondtag in totaltagcount:
            if tag in transitionprobcount:
                if secondtag in transitionprobcount[tag]:
                    if tag in last_tag_count:
                        denominator = float(transition_Tag[tag] - last_tag_count[tag] + len(totaltagcount))
                        transitionProbability[tag][secondtag] = (transitionprobcount[tag][secondtag] + 1)/denominator

                    else:
                        denominator = float(transition_Tag[tag] + len(totaltagcount))
                        transitionProbability[tag][secondtag] = (transitionprobcount[tag][secondtag] + 1) / denominator

                else:
                    value = 1/(float(transition_Tag[tag]+len(totaltagcount)))
                    transitionProbability[tag][secondtag] = value
            else:
                value = 1/float(len(totaltagcount))
                transitionProbability[tag][secondtag] = value


def calculate_emissionprobability():

    for word in wordset:
        emission_probability[word] = {}
    for word in wordset:
        for tag in totaltagcount:
            if tag in globaldict[word]:
                emission_probability[word][tag] = (globaldict[word][tag])/totaltagcount[tag]
            else:
                emission_probability[word][tag] = 0/totaltagcount[tag]

    #emission with smoothing factor 1 in numerator and len of tagset in the denominator

    if smoothing_factor == 1:
        for word in wordset:
            emission_probability[word] = {}
        for word in wordset:
            for tag in totaltagcount:
                if tag in globaldict[word]:
                    emission_probability[word][tag] = (float(globaldict[word][tag]+1)/(totaltagcount[tag]+len(totaltagcount)))
                else:
                    emission_probability[word][tag] = (float(1)/(totaltagcount[tag]+len(totaltagcount)))



readfile()
calculate_transition()
calculate_emissionprobability()

modeldata = open('hmmmodel.txt', 'w')
all_dict = {'transition_prob': transitionProbability, 'emission_prob': emission_probability, 'tag_count': totaltagcount,'globaldict': globaldict, 'lasttagcount': last_tag_count}
modeldata.write(str(all_dict))
modeldata.close()


if __name__=="__main__":
    train_file = sys.argv[1]
    #print(train_file)
    #open(model_file, "w")
