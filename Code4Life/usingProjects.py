import re
import sys
import collections
import copy
import time
import random
import math

class Player:
     def __init__(self,iInitParameter):
          self.target= iInitParameter[0]
          self.distance = iInitParameter[1]
          self.score = iInitParameter[2]
          self.storage_a = iInitParameter[3]
          self.storage_b = iInitParameter[4]
          self.storage_c = iInitParameter[5]
          self.storage_d = iInitParameter[6]
          self.storage_e = iInitParameter[7]
          self.expertise_a = iInitParameter[8]
          self.expertise_b = iInitParameter[9]
          self.expertise_c = iInitParameter[10]
          self.expertise_d = iInitParameter[11]
          self.expertise_e = iInitParameter[12]
     def __str__(self):
          return ";".join(map(str,[self.target, self.distance, self.score, [self.storage_a, self.storage_b, self.storage_c, self.storage_d, self.storage_e], [self.expertise_a, self.expertise_b, self.expertise_c, self.expertise_d, self.expertise_e]]))
     def getStorage(self):
          return [self.storage_a, self.storage_b, self.storage_c, self.storage_d, self.storage_e]
     def getExpertise(self):
          return [self.expertise_a, self.expertise_b, self.expertise_c, self.expertise_d, self.expertise_e]
     def addMolToStorage(self,iMolType,iNumber):
          if iMolType=="A":
               self.storage_a+=iNumber
          elif iMolType=="B":
               self.storage_b+=iNumber
          elif iMolType=="C":
               self.storage_c+=iNumber
          elif iMolType=="D":
               self.storage_d+=iNumber
          elif iMolType=="E":
               self.storage_e+=iNumber

     def addXP(self,iMolType):
          if iMolType=="A":
               self.expertise_a+=1
          elif iMolType=="B":
               self.expertise_b+=1
          elif iMolType=="C":
               self.expertise_c+=1
          elif iMolType=="D":
               self.expertise_d+=1
          elif iMolType=="E":
               self.expertise_e+=1


class Sample:
     def __init__(self,iInitParameter):
          self.sample_id = iInitParameter[0]
          self.carried_by = iInitParameter[1]
          self.rank = iInitParameter[2]
          self.expertise_gain = iInitParameter[3]
          self.health = iInitParameter[4]
          self.cost_a = iInitParameter[5]
          self.cost_b = iInitParameter[6]
          self.cost_c = iInitParameter[7]
          self.cost_d = iInitParameter[8]
          self.cost_e = iInitParameter[9]
          self.hiddenRef="-1"
     def __str__(self):
          return ";".join(map(str,[self.sample_id, self.carried_by, self.rank, self.expertise_gain, self.health, [self.cost_a, self.cost_b, self.cost_c, self.cost_d, self.cost_e]]))
     def __repr__(self):
          return str(self)
     def getCost(self):
          return[self.cost_a,self.cost_b,self.cost_c,self.cost_d,self.cost_e]

class Bot:
     def __init__(self,iSamples,iPlayers,iStock,iID):
          self.samples = iSamples
          self.players = iPlayers
          self.stock=iStock
          self.ID=iID
     def getOutput(self):
          aID=self.ID
          aOutput="WAIT"
          #------------------------------
          # Game is starting right here #
          #------------------------------
          # First I check if I have samples
          aIHaveSample,aMySampleId,aMySample = getBestSampleToCollect(aID)
          # I check if there is one available analysed sample on the cloud to get
          aAnalysedSampleID = getAnalysedSampleAvailable(aID)
          # Then I check if I miss ingredients for my sample
          aMissingIngredients = [0,0,0,0,0]
          if aIHaveSample:
               aMissingIngredients=getMissingMol(aMySampleId,aID)
               #logMsg("Missing ingredients: ",aMissingIngredients)

          # I am at the SAMPLE and I have spare spots, take more
          if aIHaveSample and self.players[aID].target=="SAMPLES" and self.players[aID].distance==0 and len(getMySamples(aID))<3:
               aOutput="CONNECT "+getBestRank(aID)
          # I am at the DIAGNOSIS and I have undiagnosed samples, diagnose them
          elif aIHaveSample and self.players[aID].target=="DIAGNOSIS" and self.players[aID].distance==0 and numberofCarriedUndiagnosedSamples(aID)!=0:
               aOutput="CONNECT "+getCarriedUndiagnosedSample(aID)
          # I am at the DIAGNOSIS and I have spare spots and there are available samples, get them
          elif aIHaveSample and self.players[aID].target=="DIAGNOSIS" and self.players[aID].distance==0 and len(getMySamples(aID))<3 and aAnalysedSampleID!="-1":
               aOutput="CONNECT "+aAnalysedSampleID
          # If I have a diagnosed sample and all ingredients, go to LABORATORY and connect
          elif aIHaveSample and self.samples[aMySampleId].health>0 and isEnoughStoredToProduce(aMySampleId,aID):
               #log("I miss no ingredient")
               # I am at molecules, I have enough to go to lab but I have other samples, get their molecules
               isEnough,aNextSampleID,aRemainingStorage = isEnoughInStockForNextSample(aMySampleId,aID)
               #logMsg("Is there enough",isEnough)
               #logMsg("Next sample ID", aNextSampleID)
               #logMsg("Remaining storage",aRemainingStorage)
               if self.players[aID].target=="MOLECULES" and self.players[aID].distance==0 and isEnough:
                    # To avoid penury and competition, take rarest molecules first
                    aIGotMolecules,aMolToCollect = getBestMoleculeForPlayerStock(aNextSampleID,aRemainingStorage,aID)
                    aOutput="CONNECT "+aMolToCollect
               # I am at LABORATORY, produce
               elif self.players[aID].target=="LABORATORY" and self.players[aID].distance==0:
                    aOutput="CONNECT "+aMySampleId
                    del self.samples[aMySampleId]
               else:
                    aOutput = "GOTO LABORATORY"
          # I have an undiagnosed sample, go to DIAGNOSIS
          elif aIHaveSample and aMySample.health==-1:
               if self.players[aID].target=="DIAGNOSIS" and self.players[aID].distance==0:
                    aOutput="CONNECT "+aMySampleId
               else:
                    aOutput = "GOTO DIAGNOSIS"
          # I have a diagnosed sample but there are unavailable ingredients
          # give back the sample
          # TO DO : keep sample with you, maybe adversary will give back molecules
          elif aIHaveSample and not (isEnoughStockForSample(aMySampleId,aID) and sum(getMissingMol(aMySampleId,aID))+sum(self.players[aID].getStorage())<=10):
               if self.players[aID].target=="DIAGNOSIS" and self.players[aID].distance==0:
                    aOutput="CONNECT "+aMySampleId
               else:
                    aOutput = "GOTO DIAGNOSIS"
          # If I have a sample and missing ingedients, go to MOLECULES and connect
          # If I have only rank 1 sample, go get some more
          #elif aIHaveSample and (aMySample.rank>1 or len(getMySamples())>1):
          elif aIHaveSample:
               if self.players[aID].target=="MOLECULES" and self.players[aID].distance==0:
                    # To avoid penury and competition, take rarest molecules first
                    aIGotMolecules,aMolToCollect = getBestMolecule(aMySampleId,aID)
                    if aIGotMolecules:
                         aOutput="CONNECT "+aMolToCollect
                    else:
                         aOutput="WAIT"
               else:
                    aOutput="GOTO MOLECULES"
          # If I have no sample and there is one available on the cloud with enough ingredients
          elif aAnalysedSampleID!="-1":
               if self.players[aID].target=="DIAGNOSIS" and self.players[aID].distance==0:
                    aOutput="CONNECT "+aAnalysedSampleID
               else:
                    aOutput = "GOTO DIAGNOSIS"
          # If I have no sample, go to SAMPLES and collect one
          else:
               #log("I have no sample")
               if self.players[aID].target=="SAMPLES" and self.players[aID].distance==0:
                    aOutput="CONNECT "+getBestRank(aID)
               elif self.players[aID].target=="SAMPLES":
                    aOutput = "WAIT"
               else:
                    aOutput = "GOTO SAMPLES"

          return aOutput



def log(iObj):
    print(str(iObj),file=sys.stderr)
def logMsg(iMsg, iVar):
    print(iMsg + ": " + str(iVar), file=sys.stderr)


#-----------------#
# JLC's functions #
#-----------------#

# Filter on me carrying samples
def getMySamples(iPlayerId):
     global _samples
     aMySamples = []
     for itSampleID in _samples.keys():
          if _samples[itSampleID].carried_by==iPlayerId:
               aMySamples.append(_samples[itSampleID])
     return aMySamples

# Get the table of missing molecules to produce @iSampleID
# under the form [3,1,2,3,4] for 3 "A", 1 "B", etc
def getMissingMol(iSampleID,iPlayerId):
     global _players
     return getMissingMolForPlayerStock(iSampleID,_players[iPlayerId].getStorage(),iPlayerId)

# Get the table of missing molecules to produce @iSampleID taking a storage table
# in input @iPlayerStorage
# This function is used to simulate collecting molecules for multiple samples at once
def getMissingMolForPlayerStock(iSampleID,iPlayerStorage,iPlayerId):
     global _samples,_players
     aMissingA = max(0,_samples[iSampleID].cost_a-iPlayerStorage[0]-_players[iPlayerId].expertise_a)
     aMissingB = max(0,_samples[iSampleID].cost_b-iPlayerStorage[1]-_players[iPlayerId].expertise_b)
     aMissingC = max(0,_samples[iSampleID].cost_c-iPlayerStorage[2]-_players[iPlayerId].expertise_c)
     aMissingD = max(0,_samples[iSampleID].cost_d-iPlayerStorage[3]-_players[iPlayerId].expertise_d)
     aMissingE = max(0,_samples[iSampleID].cost_e-iPlayerStorage[4]-_players[iPlayerId].expertise_e)
     return [aMissingA,aMissingB,aMissingC,aMissingD,aMissingE]

# Is there enough molecules to produce sample based on:
# player storage, game stock and player's expertise
def isEnoughStockForSample(iSampleID,iPlayerId):
     global _players
     return isEnoughStockForSampleForPlayerStock(iSampleID,_players[iPlayerId].getStorage(),iPlayerId)

# Is there enough molecules to produce sample based on:
# input storage @iPlayerStorage, game stock and player's expertise
def isEnoughStockForSampleForPlayerStock(iSampleID,iPlayerStorage,iPlayerId):
     aEnoughA = _samples[iSampleID].cost_a<=(iPlayerStorage[0]+_stock[0]+_players[iPlayerId].expertise_a)
     aEnoughB = _samples[iSampleID].cost_b<=(iPlayerStorage[1]+_stock[1]+_players[iPlayerId].expertise_b)
     aEnoughC = _samples[iSampleID].cost_c<=(iPlayerStorage[2]+_stock[2]+_players[iPlayerId].expertise_c)
     aEnoughD = _samples[iSampleID].cost_d<=(iPlayerStorage[3]+_stock[3]+_players[iPlayerId].expertise_d)
     aEnoughE = _samples[iSampleID].cost_e<=(iPlayerStorage[4]+_stock[4]+_players[iPlayerId].expertise_e)
     aEnoughStock = aEnoughA and aEnoughB and aEnoughC and aEnoughD and aEnoughE
     return  aEnoughStock

# Simulate removing the cost of a sample to @iPlayerStorage
# Used for simulating multiple collections at once
def removeSampleCostFromStorage(iSampleID,iPlayerStorage,iPlayerId):
     global _samples,_players
     aStorageA = iPlayerStorage[0]-max(0,_samples[iSampleID].cost_a-_players[iPlayerId].expertise_a)
     aStorageB = iPlayerStorage[1]-max(0,_samples[iSampleID].cost_b-_players[iPlayerId].expertise_b)
     aStorageC = iPlayerStorage[2]-max(0,_samples[iSampleID].cost_c-_players[iPlayerId].expertise_c)
     aStorageD = iPlayerStorage[3]-max(0,_samples[iSampleID].cost_d-_players[iPlayerId].expertise_d)
     aStorageE = iPlayerStorage[4]-max(0,_samples[iSampleID].cost_e-_players[iPlayerId].expertise_e)
     return  [aStorageA,aStorageB,aStorageC,aStorageD,aStorageE]

# Check if there are enough molecules in stock and storage to produce @iSampleID
def isEnoughStoredToProduce(iSampleID,iPlayerId):
     return sum(getMissingMol(iSampleID,iPlayerId))==0

# This function does the simulation of trying multiple collections
# It returns @isEnough = True if player can collect more for a collection
# It returns the @aNextSample to collect for or "-1" if I should stop and produce
def isEnoughInStockForNextSample(iSampleID,iPlayerId):
     global _stock,_samples,_players
     aNextSample = "-1"
     isEnough = False
     aRemainingStorage = [_players[iPlayerId].storage_a,_players[iPlayerId].storage_b,_players[iPlayerId].storage_c,_players[iPlayerId].storage_d,_players[iPlayerId].storage_e]
     aRemainingCapacity = 10-sum(aRemainingStorage)
     aRemainingStorage = removeSampleCostFromStorage(iSampleID,aRemainingStorage,iPlayerId)
     #logMsg("Storage after 1rst sample",aRemainingStorage)
     # Is there an unfurbished sample
     for itSample in _samples.keys():
          if itSample!=iSampleID and _samples[itSample].carried_by==iPlayerId:
               aSampleCost = _samples[itSample].getCost()
               # If I have enough stored for this smaple, don't collect more
               aMissingMol = getMissingMolForPlayerStock(itSample,aRemainingStorage,iPlayerId)
               #logMsg("Missing mol for next",aMissingMol)
               #logMsg("Remaining capacity",aRemainingCapacity)
               if sum(aMissingMol)==0:
                    aRemainingStorage = removeSampleCostFromStorage(itSample,aRemainingStorage,iPlayerId)
                    aRemainingCapacity-=sum(aSampleCost)
                    #logMsg("Already collected for",itSample)
               # If I have enough spare mol slots to collect for this sample and stock allows it
               elif sum(aMissingMol)<=aRemainingCapacity and isEnoughStockForSampleForPlayerStock(itSample,aRemainingStorage,iPlayerId):
                    isEnough = True
                    aNextSample = itSample
     return isEnough,aNextSample,aRemainingStorage

# If there are some already analysed samples in cloud, go and take
# the one bringing more health while having enough ingredients in stock
def getAnalysedSampleAvailable(iPlayerId):
     global _samples,_players
     aSampleID="-1"
     aMaxHealth = 0
     for itSampleID in _samples.keys():
          # if it's in cloud, analysed and there is enough molecules, chose it
          if _samples[itSampleID].carried_by==-1 and _samples[itSampleID].health>0 and isEnoughStockForSample(itSampleID,iPlayerId) and sum(getMissingMol(itSampleID,iPlayerId))+sum(_players[iPlayerId].getStorage())<=10:
               # Try to take the one bringing more health
               if _samples[itSampleID].health>=aMaxHealth:
                    aMaxHealth=_samples[itSampleID].health
                    aSampleID=itSampleID
     return aSampleID

# Chose which molecule you should collect next based on your player storage
# by default chose the rarest one
def getBestMolecule(iSampleID,iPlayerId):
     global _players
     return getBestMoleculeForPlayerStock(iSampleID,_players[iPlayerId].getStorage(),iPlayerId)


# TO BE ENHANCED (taking penury statistics and multi-player into account)
# Chose which molecule you should collect next based on @iPlayerStock
# by default chose the rarest one
def getBestMoleculeForPlayerStock(iSampleID,iPlayerStock,iPlayerId):
     global _stock,_moleculeTypes,_players
     aMissingMol = getMissingMolForPlayerStock(iSampleID,iPlayerStock,iPlayerId)
     aMinDiff = 10
     aMaxMissingMol = 0
     aFirstMolIndex = "-1"
     aMolFound = False
     for itMissingMolIndex in range(len(aMissingMol)):
          if aMissingMol[itMissingMolIndex]>0 and _stock[itMissingMolIndex]>0:
               if _players[1-iPlayerId].target!="MOLECULES" or (_players[1-iPlayerId].target=="MOLECULES" and _players[1-iPlayerId].distance>1):
                    if aMissingMol[itMissingMolIndex]>aMaxMissingMol:
                         aFirstMolIndex=itMissingMolIndex
                         aMaxMissingMol=aMissingMol[itMissingMolIndex]
                         aMolFound = True
               else:
                    aDiff = _stock[itMissingMolIndex]-aMissingMol[itMissingMolIndex]
                    if aDiff<=aMinDiff:
                         aMinDiff=aDiff
                         aFirstMolIndex = itMissingMolIndex
                         aMolFound = True
     return aMolFound,_moleculeTypes[aFirstMolIndex]


# TO BE BENCHMARKED (critical function to optimise according to game balance)
# Tell which sample ranks you should chose each time you go collect any
def getBestRank(iPlayerId):
     global _players,_samples
     aRank = "1"
     aCountCarriedSamples = sum(map(lambda x:int(x.carried_by==iPlayerId),_samples.values()))
     aTotalExpertize = sum(_players[iPlayerId].getExpertise())

     if aTotalExpertize+aCountCarriedSamples>=4:
          aRank = "2"
     if aTotalExpertize+aCountCarriedSamples>=8:
          aRank = "3"
     return aRank


# TO BE TESTED - new method during code review
# Give the number of undiagnosed samples that I carry
def numberofCarriedUndiagnosedSamples(iPlayerId):
     return sum(map(lambda x:int(x.health<0),getMySamples(iPlayerId)))

# Get biggest ranked undiagnosed sample carried by me
def getCarriedUndiagnosedSample(iPlayerId):
     global _samples
     aSampleID = "-1"
     aMaxRank = 0
     for itSampleID in _samples.keys():
          if _samples[itSampleID].carried_by==iPlayerId and _samples[itSampleID].health<0:
               if _samples[itSampleID].rank>=aMaxRank:
                    aMaxRank=_samples[itSampleID].rank
                    aSampleID=itSampleID
     return aSampleID

# Get the sample ID of the sample I carry that:
# - has all molecules availables
# - has the maximum health
def getBestSampleToCollect(iPlayerId):
    global _samples,_players
    aIHaveSample = False
    aMySample = Sample([0,0,0,'A',0,0,0,0,0,0])
    aMySampleID = "-1"
    aMySampleWithStockDic = {}
    for itSampleID in _samples.keys():
        if _samples[itSampleID].carried_by==iPlayerId:
            aMySample = copy.deepcopy(_samples[itSampleID])
            aMySampleID = itSampleID
            aIHaveSample=True
            #log("I have sample id "+itSampleID+" : "+str(_samples[itSampleID]))
            if isEnoughStockForSample(aMySampleID,iPlayerId) and sum(getMissingMol(aMySampleID,iPlayerId))+sum(_players[iPlayerId].getStorage())<=10:
                aMySampleWithStockDic[itSampleID]=copy.deepcopy(_samples[itSampleID])
    logMsg("feasible samples", aMySampleWithStockDic)

    aBestRank = int(getBestRank(iPlayerId))
    aProjectSampleFound = False
    # -> towards end of game, focusing on expertise
    if aBestRank == 3 or _turnCounter > 100:
        aSamples = [aMySampleWithStockDic[itSampleID] for itSampleID in aMySampleWithStockDic.keys()]
        aTargetProject, aMissingExpertise = getTargetProject(iPlayerId)
        if aMissingExpertise is None:
            aRankedSamples = []
        else:
            aRankedSamples = rankSamplesForProject(aSamples, aMissingExpertise)
        if len(aRankedSamples) != 0:
            aMySampleID = str(aRankedSamples[0].sample_id)
            aMySample = aRankedSamples[0]
            aProjectSampleFound = True
            logMsg("project mode best sample Id", aMySampleID)

    if not aProjectSampleFound:
        aMaxHealth=0
        for itSampleID in aMySampleWithStockDic.keys():
            if aMySampleWithStockDic[itSampleID].health>=aMaxHealth:
                aMaxHealth=aMySampleWithStockDic[itSampleID].health
                aMySample=aMySampleWithStockDic[itSampleID]
                aMySampleID=itSampleID

    return aIHaveSample,aMySampleID,aMySample

def getRandomSample(iRank):
     global _samplesHidden
     aEligibleSamples=[]
     for itSampleID in _samplesHidden.keys():
          if _samplesHidden[itSampleID].rank==iRank:
               aEligibleSamples.append(_samplesHidden[itSampleID])
     aInt = random.randrange(len(aEligibleSamples))
     return aEligibleSamples[max(aInt,len(aEligibleSamples)-1)]

def getNextSampleID():
     global _sampleIDCounter
     _sampleIDCounter+=1
     return _sampleIDCounter

def getDistanceToProjects(iPlayerId):
    """
    Computes the distances to the projects in terms of total number of missing expertise.
    """
    aDistanceToProjects = [[0 for itExpertise in itProject] for itProject in _projects]
    aPlayerExpertise = _players[iPlayerId].getExpertise()
    for itProject in range(len(_projects)):
        for itExpertise in range(len(_projects[itProject])):
            aDelta = _projects[itProject][itExpertise] - aPlayerExpertise[itExpertise]
            if aDelta > 0:
                aDistanceToProjects[itProject][itExpertise] = aDelta
            else:
                aDistanceToProjects[itProject][itExpertise] = 0
    logMsg("Missing expertise for projects", aDistanceToProjects)
    return aDistanceToProjects

def getTargetProject(iPlayerId):
    """
    Returns the project (array of expertise) to focus on, along with the missing expertise for this project.
    """
    aDistances = getDistanceToProjects(iPlayerId)
    aMinProjectIndex = None
    for itProject in range(len(_projects)):
        aCurrentDist = sum(aDistances[itProject])
        if aCurrentDist > 0 and (aMinProjectIndex is None or aCurrentDist < sum(aDistances[aMinProjectIndex])):
            aMinProjectIndex = itProject
    if aMinProjectIndex is None:
        log("projects cleared")
        return None, None
    else:
        logMsg("targer project", _projects[aMinProjectIndex])
        return _projects[aMinProjectIndex], aDistances[aMinProjectIndex]

def rankSamplesForProject(iSamples, iMissingExpertise):
    """
    Ranks the samples from the collections by
    1. keeping the ones with an expertise gain in the missing expersise
    2. ranking them by decreasing health
    """
    aRankedSamples = []
    for itSample in iSamples:
        if ord(itSample.expertise_gain) - ord("A") in range(len(iMissingExpertise)) and iMissingExpertise[ord(itSample.expertise_gain) - ord("A")] > 0:
            rank = 0
            for itRankedSample in range(len(aRankedSamples)):
                if aRankedSamples[itRankedSample].health <= itSample.health:
                    break
                rank += 1
            aRankedSamples.insert(rank, itSample)
    logMsg("ranked samples", aRankedSamples)
    return aRankedSamples



# Global vars JLC
_output = ""
_projects = []
_players=[]
aPlayer1=Player(["START_POS",0,0,0,0,0,0,0,0,0,0,0,0])
aPlayer2=Player(["START_POS",0,0,0,0,0,0,0,0,0,0,0,0])
_players.append(aPlayer1)
_players.append(aPlayer2)
_samplesHidden={}
_samples={}
_cloud={}
_stock=[5,5,5,5,5]
aBot0=Bot(_samples,_players,_stock,0)
aBot1=Bot(_samples,_players,_stock,1)
_bots = [aBot0,aBot1]
_moleculeTypes = ['A','B','C','D','E']

_sampleIDCounter=0
_turnCounter = 0

#####################
# START OF THE GAME #
#####################

# TO DO: I don't take adversary into consideration
# TO DO: I don't optimize the last rounds

# TO DO : I don't care about projects
# init input parsing
_ProjectCount = int(input())
for i in range(_ProjectCount):
    _projects.append([int(j) for j in input().split()])

logMsg("Projects",_projects)


#---------------#
# game loop JLC #
#---------------#
while True:
    logMsg("turn", _turnCounter)
    _turnCounter += 1
    for i in range(2):
        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
        eta = int(eta)
        score = int(score)
        storage_a = int(storage_a)
        storage_b = int(storage_b)
        storage_c = int(storage_c)
        storage_d = int(storage_d)
        storage_e = int(storage_e)
        expertise_a = int(expertise_a)
        expertise_b = int(expertise_b)
        expertise_c = int(expertise_c)
        expertise_d = int(expertise_d)
        expertise_e = int(expertise_e)
        if len(_players)==i:
            _players.append(Player([target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e]))
        else:
            _players[i].__init__([target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e])
    logMsg("Player 0",_players[0])
    logMsg("Player 1",_players[1])

    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    _stock = [available_a, available_b, available_c, available_d, available_e]
    #logMsg("Stock",_stock)
    sample_count = int(input())
    for i in range(sample_count):
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
        sample_id = int(sample_id)
        carried_by = int(carried_by)
        rank = int(rank)
        health = int(health)
        cost_a = int(cost_a)
        cost_b = int(cost_b)
        cost_c = int(cost_c)
        cost_d = int(cost_d)
        cost_e = int(cost_e)

        _samples[str(sample_id)]=Sample([sample_id,carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e])
    # Print sample table
    for itSampleID in _samples.keys():
        log(_samples[itSampleID])
    #------------------------------
    # Game is starting right here #
    #------------------------------
    _output = _bots[0].getOutput()
    print(_output)


