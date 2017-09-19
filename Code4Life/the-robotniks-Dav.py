import re
import sys
import collections
import copy
import time
import random


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
     def getCost(self):
          return[self.cost_a,self.cost_b,self.cost_c,self.cost_d,self.cost_e]
     #DRE
     def __eq__(self, other):
          return self.rank == other.rank and self.expertise_gain == other.expertise_gain and self.health == other.health and self.cost_a == other.cost_a and self.cost_b == other.cost_b and self.cost_c == other.cost_c and self.cost_d == other.cost_d and self.cost_e == other.cost_e

class Stats:
     def __init__(self, iNbLeft, iCostMin, iCostMax, iCostAvg, iHealthMin, iHealthMax, iHealthAvg):
          self.nb_left = iNbLeft
          self.cost_min = iCostMin
          self.cost_max = iCostMax
          self.cost_avg = iCostAvg
          self.health_min = iHealthMin
          self.health_max = iHealthMax
          self.health_avg = iHealthAvg

     def __str__(self):
          return "NbLeft:{0} | CostMin:{1} | CostMax:{2} | CostAvg:{3} \n             HealthMin:{4} | HealthMax:{5} | HealthAvg:{6}".format(self.nb_left, self.cost_min, self.cost_max, self.cost_avg, self.health_min, self.health_max, self.health_avg)

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
          # DRE: I am at the DIAGNOSIS and I have diagnosed samples of lower rank (probably blocked), let them go on the cloud
          elif aIHaveSample and self.players[aID].target=="DIAGNOSIS" and self.players[aID].distance==0 and getLowerRankofMySamples(aID) < int(getBestRank(aID)):
               aOutput="CONNECT "+getFirstRankSample(getLowerRankofMySamples(aID),aID)
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
          # DRE : tried to update to drop only if all samples are blocked... raised bugs in series, abandoned
          #elif aIHaveSample and NoneOfMySamplesAreFeasible(aID) and self.players[1-aID].target!="LABORATORY":
          elif aIHaveSample and not (isEnoughStockForSample(aMySampleId,aID) and sum(getMissingMol(aMySampleId,aID))+sum(self.players[aID].getStorage())<=10) and self.players[1-aID].target!="LABORATORY":
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
def getMySamples(iPlayerID):
     global _samples
     aMySamples = []
     for itSampleID in _samples.keys():
          if _samples[itSampleID].carried_by==iPlayerID:
               aMySamples.append(_samples[itSampleID])
     return aMySamples

# Get the table of missing molecules to produce @iSampleID
# under the form [3,1,2,3,4] for 3 "A", 1 "B", etc
def getMissingMol(iSampleID,iPlayerID):
     global _players
     return getMissingMolForPlayerStock(iSampleID,_players[iPlayerID].getStorage(),iPlayerID)

# Get the table of missing molecules to produce @iSampleID taking a storage table
# in input @iPlayerStorage
# This function is used to simulate collecting molecules for multiple samples at once
def getMissingMolForPlayerStock(iSampleID,iPlayerStorage,iPlayerID):
     global _samples,_players
     aMissingA = max(0,_samples[iSampleID].cost_a-iPlayerStorage[0]-_players[iPlayerID].expertise_a)
     aMissingB = max(0,_samples[iSampleID].cost_b-iPlayerStorage[1]-_players[iPlayerID].expertise_b)
     aMissingC = max(0,_samples[iSampleID].cost_c-iPlayerStorage[2]-_players[iPlayerID].expertise_c)
     aMissingD = max(0,_samples[iSampleID].cost_d-iPlayerStorage[3]-_players[iPlayerID].expertise_d)
     aMissingE = max(0,_samples[iSampleID].cost_e-iPlayerStorage[4]-_players[iPlayerID].expertise_e)
     return [aMissingA,aMissingB,aMissingC,aMissingD,aMissingE]

# Is there enough molecules to produce sample based on:
# player storage, game stock and player's expertise
def isEnoughStockForSample(iSampleID,iPlayerID):
     global _players
     return isEnoughStockForSampleForPlayerStock(iSampleID,_players[iPlayerID].getStorage(),iPlayerID)

# Is there enough molecules to produce sample based on:
# input storage @iPlayerStorage, game stock and player's expertise
def isEnoughStockForSampleForPlayerStock(iSampleID,iPlayerStorage,iPlayerID):
     aEnoughA = _samples[iSampleID].cost_a<=(iPlayerStorage[0]+_stock[0]+_players[iPlayerID].expertise_a)
     aEnoughB = _samples[iSampleID].cost_b<=(iPlayerStorage[1]+_stock[1]+_players[iPlayerID].expertise_b)
     aEnoughC = _samples[iSampleID].cost_c<=(iPlayerStorage[2]+_stock[2]+_players[iPlayerID].expertise_c)
     aEnoughD = _samples[iSampleID].cost_d<=(iPlayerStorage[3]+_stock[3]+_players[iPlayerID].expertise_d)
     aEnoughE = _samples[iSampleID].cost_e<=(iPlayerStorage[4]+_stock[4]+_players[iPlayerID].expertise_e)
     aEnoughStock = aEnoughA and aEnoughB and aEnoughC and aEnoughD and aEnoughE
     return  aEnoughStock

# Simulate removing the cost of a sample to @iPlayerStorage
# Used for simulating multiple collections at once
def removeSampleCostFromStorage(iSampleID,iPlayerStorage,iPlayerID):
     global _samples,_players
     aStorageA = iPlayerStorage[0]-max(0,_samples[iSampleID].cost_a-_players[iPlayerID].expertise_a)
     aStorageB = iPlayerStorage[1]-max(0,_samples[iSampleID].cost_b-_players[iPlayerID].expertise_b)
     aStorageC = iPlayerStorage[2]-max(0,_samples[iSampleID].cost_c-_players[iPlayerID].expertise_c)
     aStorageD = iPlayerStorage[3]-max(0,_samples[iSampleID].cost_d-_players[iPlayerID].expertise_d)
     aStorageE = iPlayerStorage[4]-max(0,_samples[iSampleID].cost_e-_players[iPlayerID].expertise_e)
     return  [aStorageA,aStorageB,aStorageC,aStorageD,aStorageE]

# Check if there are enough molecules in stock and storage to produce @iSampleID
def isEnoughStoredToProduce(iSampleID,iPlayerID):
     return sum(getMissingMol(iSampleID,iPlayerID))==0

# This function does the simulation of trying multiple collections
# It returns @isEnough = True if player can collect more for a collection
# It returns the @aNextSample to collect for or "-1" if I should stop and produce
def isEnoughInStockForNextSample(iSampleID,iPlayerID):
     global _stock,_samples,_players
     aNextSample = "-1"
     isEnough = False
     aRemainingStorage = [_players[iPlayerID].storage_a,_players[iPlayerID].storage_b,_players[iPlayerID].storage_c,_players[iPlayerID].storage_d,_players[iPlayerID].storage_e]
     aRemainingCapacity = 10-sum(aRemainingStorage)
     aRemainingStorage = removeSampleCostFromStorage(iSampleID,aRemainingStorage,iPlayerID)
     #logMsg("Storage after 1rst sample",aRemainingStorage)
     # Is there an unfurbished sample
     for itSample in _samples.keys():
          if itSample!=iSampleID and _samples[itSample].carried_by==iPlayerID:
               aSampleCost = _samples[itSample].getCost()
               # If I have enough stored for this smaple, don't collect more
               aMissingMol = getMissingMolForPlayerStock(itSample,aRemainingStorage,iPlayerID)
               #logMsg("Missing mol for next",aMissingMol)
               #logMsg("Remaining capacity",aRemainingCapacity)
               if sum(aMissingMol)==0:
                    aRemainingStorage = removeSampleCostFromStorage(itSample,aRemainingStorage,iPlayerID)
                    aRemainingCapacity-=sum(aSampleCost)
                    #logMsg("Already collected for",itSample)
               # If I have enough spare mol slots to collect for this sample and stock allows it
               elif sum(aMissingMol)<=aRemainingCapacity and isEnoughStockForSampleForPlayerStock(itSample,aRemainingStorage,iPlayerID):
                    isEnough = True
                    aNextSample = itSample
     return isEnough,aNextSample,aRemainingStorage

# If there are some already analysed samples in cloud, go and take
# the one bringing more health while having enough ingredients in stock
def getAnalysedSampleAvailable(iPlayerID):
     global _samples,_players
     aSampleID="-1"
     aMaxHealth = 0
     for itSampleID in _samples.keys():
          # if it's in cloud, analysed and there is enough molecules, chose it
          # DRE ... and if it matches current rank
          if _samples[itSampleID].carried_by==-1 and _samples[itSampleID].health>0 and isEnoughStockForSample(itSampleID,iPlayerID) and sum(getMissingMol(itSampleID,iPlayerID))+sum(_players[iPlayerID].getStorage())<=10 and _samples[itSampleID].rank == int(getBestRank(iPlayerID)):
               # Try to take the one bringing more health
               if _samples[itSampleID].health>=aMaxHealth:
                    aMaxHealth=_samples[itSampleID].health
                    aSampleID=itSampleID
     return aSampleID

# Chose which molecule you should collect next based on your player storage
# by default chose the rarest one
def getBestMolecule(iSampleID,iPlayerID):
     global _players
     return getBestMoleculeForPlayerStock(iSampleID,_players[iPlayerID].getStorage(),iPlayerID)


# TO BE ENHANCED (taking penury statistics and multi-player into account)
# Chose which molecule you should collect next based on @iPlayerStock
# by default chose the rarest one
def getBestMoleculeForPlayerStock(iSampleID,iPlayerStock,iPlayerID):
     global _stock,_moleculeTypes,_players
     aMissingMol = getMissingMolForPlayerStock(iSampleID,iPlayerStock,iPlayerID)
     aMinDiff = 10
     aMaxMissingMol = 0
     aFirstMolIndex = -1 #DRE : there was a bug due to "-1" as a string: when no mol found, on last line it raises an exception.
     aMolFound = False
     for itMissingMolIndex in range(len(aMissingMol)):
          if aMissingMol[itMissingMolIndex]>0 and _stock[itMissingMolIndex]>0:
               if _players[1-iPlayerID].target!="MOLECULES" or (_players[1-iPlayerID].target=="MOLECULES" and _players[1-iPlayerID].distance>1):
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
def getBestRank(iPlayerID):
     global _players
     aStatRank1 = computeSampleRankStats(1,iPlayerID)
     aStatRank2 = computeSampleRankStats(2,iPlayerID)
     aStatRank3 = computeSampleRankStats(3,iPlayerID)
     aRank = "1"
     if aStatRank2.cost_avg < 5.0 and aStatRank3.cost_avg > 7.0:
          aRank = "2"    
     if aStatRank3.cost_avg < 7.0:
          aRank = "3"    
     return aRank

# DRE: ORIGINAL FUNCTION BACKUP
# def getBestRank(iPlayerID):
#      global _players,_samples
#      aRank = "1"
#      aCountCarriedSamples = sum(map(lambda x:int(x.carried_by==iPlayerID),_samples.values()))
#      aTotalExpertize = sum(_players[iPlayerID].getExpertise())

#      if aTotalExpertize+aCountCarriedSamples>=4:
#           aRank = "2"    
#      if aTotalExpertize+aCountCarriedSamples>=8:
#           aRank = "3"    
#      return aRank

# TO BE TESTED - new method during code review
# Give the number of undiagnosed samples that I carry
def numberofCarriedUndiagnosedSamples(iPlayerID):
     return sum(map(lambda x:int(x.health<0),getMySamples(iPlayerID)))

# Get biggest ranked undiagnosed sample carried by me
def getCarriedUndiagnosedSample(iPlayerID):
     global _samples
     aSampleID = "-1"
     aMaxRank = 0
     for itSampleID in _samples.keys():
          if _samples[itSampleID].carried_by==iPlayerID and _samples[itSampleID].health<0:
               if _samples[itSampleID].rank>=aMaxRank:
                    aMaxRank=_samples[itSampleID].rank
                    aSampleID=itSampleID
     return aSampleID

# Get the sample ID of the sample I carry that:
# - has all molecules availables
# - has the maximum health
def getBestSampleToCollect(iPlayerID):
     global _samples,_players
     aIHaveSample = False
     aMySample = Sample([0,0,0,'A',0,0,0,0,0,0])
     aMySampleID = "-1"
     aMySampleWithStockDic = {}
     for itSampleID in _samples.keys():
          if _samples[itSampleID].carried_by==iPlayerID:
               aMySample = copy.deepcopy(_samples[itSampleID])
               aMySampleID = itSampleID
               aIHaveSample=True
               #log("I have sample id "+itSampleID+" : "+str(_samples[itSampleID]))
               if isEnoughStockForSample(aMySampleID,iPlayerID) and sum(getMissingMol(aMySampleID,iPlayerID))+sum(_players[iPlayerID].getStorage())<=10:
                    aMySampleWithStockDic[itSampleID]=copy.deepcopy(_samples[itSampleID])
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
  
#DRE STAT/PROBA FUNCTIONS 
# DRE TODO: compute proba to get expertise levels 
def avg(l):
     return sum(l) / len(l)

def minusList(l1,l2):
     return map(lambda x,y: max(0,x-y),l1,l2)

def computeSampleRankStats(iRank, iPlayerId):
     global _allSamples
     aSamplesList = [itSample for itSample in _allSamples.values() if itSample.rank == iRank and itSample.carried_by == -1]
     aSamplesCostsMol = [minusList(itSample.getCost(), _players[iPlayerId].getExpertise()) for itSample in aSamplesList]
     aSamplesCost = [sum(itCostsMol) for itCostsMol in aSamplesCostsMol]
     aSamplesHealth = [itSample.health for itSample in aSamplesList]
     return Stats(len(aSamplesList), min(aSamplesCost),max(aSamplesCost),avg(aSamplesCost), min(aSamplesHealth),max(aSamplesHealth),avg(aSamplesHealth))

def getLowerRankofMySamples(iPlayerId):
     aMySamples = getMySamples(iPlayerId)
     aMyRanks = [itSample.rank for itSample in aMySamples]
     return min(aMyRanks)

def getFirstRankSample(iRank,iPlayerId):
     aMySamples = getMySamples(iPlayerId)
     aMySampleIdsofRankiRank = [itSample.sample_id for itSample in aMySamples if itSample.rank == iRank]
     return aMySampleIdsofRankiRank[0]

# tried to define it to drop only samples when totally blocked. But raised too many bugs in other places.
# def NoneOfMySamplesAreFeasible(iPlayerId):
#      aMySamples = getMySamples(iPlayerId)
#      aSampleNotFeasible = [1 for itSample in aMySamples if not (isEnoughStockForSample(itSample.sample_id,iPlayerId) and sum(getMissingMol(itSample.sample_id,iPlayerId))+sum(self.players[iPlayerId].getStorage())<=10)]
#      return sum(aSampleNotFeasible) == len(aMySamples)


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
# Global vars DRE
_currentRank = 1

# DRE : All samples raw list
_allSamplesList = ["1;-1;0;A;01;[0,3,0,0,0]",
"2;-1;0;A;01;[0,0,0,2,1]",
"3;-1;0;A;01;[0,1,1,1,1]",
"4;-1;0;A;01;[0,2,0,0,2]",
"5;-1;0;A;10;[0,0,4,0,0]",
"6;-1;0;A;01;[0,1,2,1,1]",
"7;-1;0;A;01;[0,2,2,0,1]",
"8;-1;0;A;01;[3,1,0,0,1]",
"9;-1;0;B;01;[1,0,0,0,2]",
"10;-1;0;B;01;[0,0,0,0,3]",
"11;-1;0;B;01;[1,0,1,1,1]",
"12;-1;0;B;01;[0,0,2,0,2]",
"13;-1;0;B;10;[0,0,0,4,0]",
"14;-1;0;B;01;[1,0,1,2,1]",
"15;-1;0;B;01;[1,0,2,2,0]",
"16;-1;0;B;01;[0,1,3,1,0]",
"17;-1;0;C;01;[2,1,0,0,0]",
"18;-1;0;C;01;[0,0,0,3,0]",
"19;-1;0;C;01;[1,1,0,1,1]",
"20;-1;0;C;01;[0,2,0,2,0]",
"21;-1;0;C;10;[0,0,0,0,4]",
"22;-1;0;C;01;[1,1,0,1,2]",
"23;-1;0;C;01;[0,1,0,2,2]",
"24;-1;0;C;01;[1,3,1,0,0]",
"25;-1;0;D;01;[0,2,1,0,0]",
"26;-1;0;D;01;[3,0,0,0,0]",
"27;-1;0;D;01;[1,1,1,0,1]",
"28;-1;0;D;01;[2,0,0,2,0]",
"29;-1;0;D;10;[4,0,0,0,0]",
"30;-1;0;D;01;[2,1,1,0,1]",
"31;-1;0;D;01;[2,0,1,0,2]",
"32;-1;0;D;01;[1,0,0,1,3]",
"33;-1;0;E;01;[0,0,2,1,0]",
"34;-1;0;E;01;[0,0,3,0,0]",
"35;-1;0;E;01;[1,1,1,1,0]",
"36;-1;0;E;01;[2,0,2,0,0]",
"37;-1;0;E;10;[0,4,0,0,0]",
"38;-1;0;E;01;[1,2,1,1,0]",
"39;-1;0;E;01;[2,2,0,1,0]",
"40;-1;0;E;01;[0,0,1,3,1]",
"41;-1;1;A;20;[0,0,0,5,0]",
"42;-1;1;A;30;[6,0,0,0,0]",
"43;-1;1;A;10;[0,0,3,2,2]",
"44;-1;1;A;20;[0,0,1,4,2]",
"45;-1;1;A;10;[2,3,0,3,0]",
"46;-1;1;A;20;[0,0,0,5,3]",
"47;-1;1;B;20;[0,5,0,0,0]",
"48;-1;1;B;30;[0,6,0,0,0]",
"49;-1;1;B;10;[0,2,2,3,0]",
"50;-1;1;B;20;[2,0,0,1,4]",
"51;-1;1;B;20;[0,2,3,0,3]",
"52;-1;1;B;20;[5,3,0,0,0]",
"53;-1;1;C;20;[0,0,5,0,0]",
"54;-1;1;C;30;[0,0,6,0,0]",
"55;-1;1;C;10;[2,3,0,0,2]",
"56;-1;1;C;10;[3,0,2,3,0]",
"57;-1;1;C;20;[4,2,0,0,1]",
"58;-1;1;C;20;[0,5,3,0,0]",
"59;-1;1;D;20;[5,0,0,0,0]",
"60;-1;1;D;30;[0,0,0,6,0]",
"61;-1;1;D;10;[2,0,0,2,3]",
"62;-1;1;D;20;[1,4,2,0,0]",
"63;-1;1;D;10;[0,3,0,2,3]",
"64;-1;1;D;20;[3,0,0,0,5]",
"65;-1;1;E;20;[0,0,0,0,5]",
"66;-1;1;E;30;[0,0,0,0,6]",
"67;-1;1;E;10;[3,2,2,0,0]",
"68;-1;1;E;20;[0,1,4,2,0]",
"69;-1;1;E;10;[3,0,3,0,2]",
"70;-1;1;E;20;[0,0,5,3,0]",
"71;-1;2;A;40;[0,0,0,0,7]",
"72;-1;2;A;50;[3,0,0,0,7]",
"73;-1;2;A;40;[3,0,0,3,6]",
"74;-1;2;A;30;[0,3,3,5,3]",
"75;-1;2;B;40;[7,0,0,0,0]",
"76;-1;2;B;50;[7,3,0,0,0]",
"77;-1;2;B;40;[6,3,0,0,3]",
"78;-1;2;B;30;[3,0,3,3,5]",
"79;-1;2;C;40;[0,7,0,0,0]",
"80;-1;2;C;50;[0,7,3,0,0]",
"81;-1;2;C;40;[3,6,3,0,0]",
"82;-1;2;C;30;[5,3,0,3,3]",
"83;-1;2;D;40;[0,0,7,0,0]",
"84;-1;2;D;50;[0,0,7,3,0]",
"85;-1;2;D;40;[0,3,6,3,0]",
"86;-1;2;D;30;[3,5,3,0,3]",
"87;-1;2;E;40;[0,0,0,7,0]",
"88;-1;2;E;50;[0,0,0,7,3]",
"89;-1;2;E;40;[0,0,3,6,3]",
"90;-1;2;E;30;[3,3,5,3,0]"
]

# DRE: all Samples structure filling
# Necessary to have a distinct structure from _samples from input at each turn
# because of different sampleId and all logic based on _samples global in all functions
_allSamples={}
aSampleDic={}
for sample in _allSamplesList:
     aExtract = re.search("([0-9]*);",sample)
     if aExtract!=None:
          aSampleDic[aExtract.group(1)]=sample
          sample_id, carried_by, rank, expertise_gain, health, cost = sample.split(";")
          cost_a, cost_b, cost_c, cost_d, cost_e = cost[1:-1].split(",")
          sample_id = int(sample_id)
          carried_by = int(carried_by)
          rank = int(rank)+1
          health = int(health)
          cost_a = int(cost_a)
          cost_b = int(cost_b)
          cost_c = int(cost_c)
          cost_d = int(cost_d)
          cost_e = int(cost_e)
          _allSamples[str(sample_id)]=Sample([sample_id,carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e])


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
        aNewSample=Sample([sample_id,carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e])
        # find the real sample_id of all_samples, IF DIAGNOSED
        if health > 0:
            for itSampleId in _allSamples.keys():
                if _allSamples[itSampleId] == aNewSample:
                   aFoundSampleId = itSampleId
                   break
            _allSamples[aFoundSampleId].carried_by = carried_by

    # #Print sample table
    # #DRE: there's maybe a bug in CDG's engine: samples completed by the opponent are not retired from active samples list...
    # #DRE: is it expected behavior ? Anyway it prevents a simple identification of removed samples...
    # log("LOCAL SAMPLES")
    # for itSampleID in _samples.keys():
    #    log(_samples[itSampleID])

    # log("ALL SAMPLES")
    # for itSampleID in _allSamples.keys():
    #     log(_allSamples[itSampleID])
    logMsg("STATS Rank I  ",computeSampleRankStats(1,0))
    logMsg("STATS Rank II ",computeSampleRankStats(2,0))
    logMsg("STATS Rank III",computeSampleRankStats(3,0))
    #------------------------------
    # Game is starting right here #
    #------------------------------
    _output = _bots[0].getOutput()
    print(_output)


