import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]

_samples = {}
_players = []
_output = ""
_molecules = ["A","B","C","D","E"]

def log(iObj):
    print(str(iObj),file=sys.stderr)

def getSampleFromCloud():
    global _samples
    aMaxEfficiency = 0
    aSampleId = -1
    for itSampleId in _samples.keys():
        if _samples[itSampleId][0]==-1:
            aEfficiency = _samples[itSampleId][3]/sum(_samples[itSampleId][4:])
            if aEfficiency>aMaxEfficiency:
                aMaxEfficiency=aEfficiency
                aSampleId=itSampleId
    return aSampleId

# game loop
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
        if i==0:
            if len(_players)==0:
                _players.append([target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e])
            else:
                _players[0]=[target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e]
    log(_players[0])
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
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
        
        _samples[str(sample_id)]=[carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    
    aIHaveSample = False
    aMySample = []
    aMySampleId = -1
    for itSampleId in _samples.keys():
        if _samples[itSampleId][0]==0:
            aMySample = list(_samples[itSampleId])
            aMySampleId = str(itSampleId)
            aIHaveSample=True
            log("I have sample id "+itSampleId+" : "+str(_samples[itSampleId]))
            
    aMissingIngredients = [0,0,0,0,0]
    if aIHaveSample:
        for itIngredientIndex in range(5):
            aMissingIngredients[itIngredientIndex]=aMySample[4+itIngredientIndex]-_players[0][3+itIngredientIndex]
        log("Missing ingredients: "+str(aMissingIngredients))
    # If I have a sample and all ingredients, go to LABORATORY and connect
    if aIHaveSample and aMissingIngredients==[0,0,0,0,0]:
        log("I miss no ingredient")
        if _players[0][0]=="LABORATORY":
            _output="CONNECT "+aMySampleId
            del _samples[aMySampleId]
        else:
            _output = "GOTO LABORATORY"
    # If I have a sample and missing ingedients, go to MOLECULES and connect
    elif aIHaveSample:
        if _players[0][0]=="MOLECULES":
            for itMissingMolIndex in range(len(aMissingIngredients)):
                if aMissingIngredients[itMissingMolIndex]!=0:
                    _output="CONNECT "+_molecules[itMissingMolIndex]
        else:
            _output="GOTO MOLECULES"
    # If I have no sample, go to DIAGNOSIS and collect one
    else:
        log("I have no sample")
        if _players[0][0]=="DIAGNOSIS":
            aSampleId = getSampleFromCloud()
            if aSampleId!=-1:
                _output="CONNECT "+str(aSampleId)
            else:
                log("No sample available")
                _output = "GOTO DIAGNOSIS"
        else:
            _output = "GOTO DIAGNOSIS"

    print(_output)