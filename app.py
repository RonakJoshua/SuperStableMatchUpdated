from flask import Flask, render_template, url_for, redirect, request
import numpy as np
import random

app = Flask(__name__)

x = 7
factor = 0.8


@app.route('/')
def hello_world():  # put application's code here
    dataSet = superStableMatch(x)
    if dataSet is not None:
        matchList = []
        for m in range(x):
            matchList.append([m, dataSet.maleSet[m].engagedWith[0]])
        return render_template("algorithm.html", data=dataSet, n=x, matches=matchList)
    return render_template("algorithm.html", data=dataSet, n=x, matches=[])


if __name__ == '__main__':
    app.run()


class IndividualGenerator:
    def __init__(self, n):
        self.maleSet = []
        self.femaleSet = []
        for i in range(n):
            self.maleSet.append(Individual(i, "male", n))
            self.femaleSet.append(Individual(i, "female", n))

        # testing
        '''self.maleSet[0].preference.ranking = {0: [2, 1], 1: [0]}
        self.maleSet[1].preference.ranking = {0: [1], 1: [0], 2: [2]}
        self.maleSet[2].preference.ranking = {0: [0, 1, 2]}

        self.femaleSet[0].preference.ranking = {0: [0, 1], 1: [2]}
        self.femaleSet[1].preference.ranking = {0: [1], 1: [0, 2]}
        self.femaleSet[2].preference.ranking = {0: [2, 1, 0]}'''



    # good
    def allEngaged(self):
        for m in self.maleSet:
            if len(m.engagedWith) == 0:
                return False
        for f in self.femaleSet:
            if len(f.engagedWith) == 0:
                return False
        return True

    # good
    def someFreeMan(self):
        for individual in self.maleSet:
            if individual.isFree():
                return True
        return False

    # good
    def propose(self, man, woman):
        man.engagedWith.append(woman.index)
        woman.engagedWith.append(man.index)

    # good
    def findMan(self, index):
        return [x for x in self.maleSet if x.index == index][0]

    # good
    def findWoman(self, index):
        return [x for x in self.femaleSet if x.index == index][0]

    # good
    def deletePair(self, man, woman):
        for key in list(woman.preference.ranking.keys()):
            if woman.preference.ranking[key].count(man.index) == 1:
                woman.preference.ranking[key].remove(man.index)
                if len(woman.preference.ranking[key]) == 0:
                    del woman.preference.ranking[key]
        for key in list(man.preference.ranking.keys()):
            if man.preference.ranking[key].count(woman.index) == 1:
                man.preference.ranking[key].remove(woman.index)
                if len(man.preference.ranking[key]) == 0:
                    del man.preference.ranking[key]
        return

    # good, changed
    def deleteInferiorPairs(self, man, woman):
        for key in list(woman.preference.ranking.keys()):
            if woman.preference.ranking[key].count(man.index) == 1:
                for k in range(key + 1, list(woman.preference.ranking.keys())[-1] + 1):
                    '''for i in woman.preference.ranking[k]:
                        self.deletePair(self.findMan(i), woman)'''
                    while k in woman.preference.ranking:
                        self.deletePair(self.findMan(woman.preference.ranking[k][0]), woman)
                break
        return

    # good
    def removeEngagement(self, man, woman):
        if man.engagedWith.count(woman.index) == 1:
            man.engagedWith.remove(woman.index)
            woman.engagedWith.remove(man.index)
        return

    def multiplyEngaged(self):
        multipleEngagements = []
        for woman in self.femaleSet:
            if len(woman.engagedWith) > 1:
                multipleEngagements.append(woman)
        return multipleEngagements

    def emptyMaleList(self):
        for male in self.maleSet:
            if not male.preference.ranking:
                return True
        return False

    def validEngagement(self, man, woman):
        if len(woman.engagedWith) == 0:
            return True
        #print(woman.engagedWith)
        #print("rank engaged: " + str(woman.getRank(woman.engagedWith[0])) + "\nrank man: " + str(woman.getRank(man.index)))
        if woman.getRank(woman.engagedWith[0]) >= woman.getRank(man.index):
            return True
        return False

    def __str__(self):
        outputString = ''
        for male in self.maleSet:
            outputString += f'\nmale: {male.index}, {male.preference.ranking}, {male.engagedWith}'
        for female in self.femaleSet:
            outputString += f'\nfemale: {female.index}, {female.preference.ranking}, {female.engagedWith}'
        return outputString


class Individual:
    def __init__(self, index, sex, n):
        self.index = index  # index of male or female individual
        self.sex = sex  # sex of individual (male/female)
        self.engagedWith = []
        self.preference = RandomRanking(n)
        self.originalPreferenceText = "Preference:\n"
        for rank in self.preference.ranking:
            self.originalPreferenceText += "\n\t(Rank " + str(rank+1) + ":"
            for index in self.preference.ranking[rank]:
                if self.sex == "male":
                    self.originalPreferenceText += " w" + str(index+1) + ","
                else:
                    self.originalPreferenceText += " m" + str(index+1) + ","
            self.originalPreferenceText = self.originalPreferenceText[:-1]
            self.originalPreferenceText += ")"

                    # good
    def isFree(self):
        if len(self.engagedWith) == 0:
            return True
        return False

    # good
    def getHead(self):
        '''if len(list(self.preference.ranking.keys())) == 0:
            return []'''
        return self.preference.ranking[list(self.preference.ranking.keys())[0]]


    # good, check
    def removeInferiorEngagement(self, index):
        for key in list(self.preference.ranking.keys()):
            if self.preference.ranking[key].count(index) == 1:
                for k in range(key+1, list(self.preference.ranking.keys())[-1]+1):
                    for i in self.preference.ranking[k]:
                        if i in self.engagedWith:
                            self.engagedWith.remove(i)
                break
        return

    def getRank(self, index):
        for key in list(self.preference.ranking.keys()):
            if self.preference.ranking[key].count(index) == 1:
                return key
        # return -1


class RandomRanking:
    def __init__(self, n):
        self.indifferenceFactor = random.randrange(0, int(factor * 1000)) / 1000  # (determines probability that ranking list will have ties)
        self.rankingList = np.arange(n)
        np.random.shuffle(self.rankingList)  # shuffled list of Individual indices
        self.ranking = {0: [self.rankingList[0]]}
        self.rankingList = np.delete(self.rankingList, 0)
        while len(self.rankingList) > 0:
            if self.indifference():
                self.ranking[list(self.ranking.keys())[-1]] += [self.rankingList[0]]
            else:
                self.ranking[list(self.ranking.keys())[-1] + 1] = [self.rankingList[0]]
            self.rankingList = np.delete(self.rankingList, 0)

    def indifference(self):
        return random.random() < self.indifferenceFactor


# separate operation for populating and randomizing ranking
# allows for pre-determined or random ranking


def superStableMatch(n):
    data = IndividualGenerator(n)

    while not data.emptyMaleList():
        #print("in while loop")
        for man in data.maleSet:
            if data.emptyMaleList():
                return None
            if man.isFree():
                #print("in man for loop")
                for womanIndex in man.getHead():
                    #print("Index: " + str(womanIndex))
                    woman = data.findWoman(womanIndex)
                    #print(woman.preference.ranking)
                    data.propose(man, woman)
                    for index in list(woman.preference.ranking.keys()):
                        for mpref in woman.preference.ranking[index]:
                            if woman.getRank(mpref) > woman.getRank(man.index):  # Nonetype and int issue
                                if mpref in woman.engagedWith:
                                    data.removeEngagement(data.findMan(mpref), woman)
                                data.deletePair(data.findMan(mpref), woman)
        for woman in data.multiplyEngaged():
            for index in woman.engagedWith:
                data.removeEngagement(data.findMan(index), woman)
            for manIndex in woman.preference.ranking[list(woman.preference.ranking.keys())[-1]]:
                data.deletePair(data.findMan(manIndex), woman)
        if data.emptyMaleList():
            return None
        if data.allEngaged():
            return data
