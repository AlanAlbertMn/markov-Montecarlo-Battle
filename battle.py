import random
import math
import numpy as np

a = 0
b = 1
N = 10
CLANS = 3
filename = 'battleResults.txt'

# function for montecarlo
def f(x):
    return x**2


def printMatrix(clanKeys, matrix, size):
    # print(clanKeys)
    for i in range(size):
        file.write("  {}\t" .format(clanKeys[i]))
    file.write("\n")
    row = 0
    for i in matrix:
        file.write("{} " .format(clanKeys[row]))
        for j in i:
            file.write(("{:.2f} " .format(j)))
            # file.write("{} " .format(str(float(j))))
        file.write("\n")
        row+=1

def montecarlo(probabilities):
    for i in range(N):
        ar = np.zeros(N)
        
        for i in range (len(ar)):
            ar[i] = np.random.uniform(a,b)
        integral = 0.0

        for i in ar:
            integral += f(i)

        ans = (b-a)/float(N)*integral
    
    # print("Ans ", ans)
    i = 0
    tmp = i
    for x in probabilities:
        # print("Interval [{}, {}]" .format(x[i], x[i+1]))
        if ans >= x[i] and ans < x[i+1]:
            # print("Ans {} in {} interval" .format(ans, tmp))
            # file.write("Ans {} in {} interval\n" .format(ans, tmp))
            return tmp
        else:
            # print("Ans {} not in {} interval" .format(ans, tmp))
            tmp+=1

def numSoldiers(dictClans):
    # print("=================================")
    # file.write("=================================\n")
    for clan, info in dictClans.items():
        # print("Clan {} has {} soldiers left." .format(clan, info[0]))
        file.write("Clan {} has {} soldiers left.\n" .format(clan, info[0]))
    # print("=================================")
    file.write("=================================\n")
    
def getIntervals(probListAttacker, attacker):
    inter = list()
    suma = float(0)
    for x in probListAttacker:
        suma1 = suma
        suma2 = suma + x
        inter.append([suma1, suma2])
        suma = suma2

# to see the final intervals uncomment the two lines below 
    # print("Intervalos final de clan: ", attacker)
    # print(inter)
    return inter

def countSoldiers(clans):
    for clan, info in clans.items():
        # print("Clan {} has {} soldiers left." .format(clan, info[0]))
        if info[0] == 0:
            # print("Clan {} was annihilated" .format(clan))
            file.write(("Clan {} was annihilated\n" .format(clan)))
            clans.pop(clan)
            return 0


def attackSoldier(dictClans, attacker):
    if len(dictClans) > 2:
        probs = dictClans.get(attacker)[2]
        # print("Probabilities of attacking for clan ", attacker)
        # print(probs)
        # file.write("Probabilities of attacking for clan {}\n" .format(attacker))
        attacked = montecarlo(probs)
        if attacked == attacker: # this condition is set so if montecarlo generates the same clan as objective for the attackiong clan, it generates a new objective
            while attacked == attacker:
                attacked = montecarlo(probs)
                # print("Attacked clan number: ", attacked)
                # file.write("Attacked clan number: {}\n" .format(attacked))
        file.write("Clan {} attacked clan {}!\n" .format(attacker, attacked))
        # print("Clan {} attacked clan {}!" .format(attacker, attacked))
        dictClans.get(attacked)[0]-=1
    else: 
        for clan, info in dictClans.items():
            if clan != attacker :
                dictClans.get(clan)[0]-=1

def fillMatrix(battleMatrix, nClans):
    if nClans != 2:
        for elem in range(nClans): # for the number of rows in the battle matrix
            sumOne = 0
            tmp= list()
            for elem2 in range(nClans-2):
                # float("{:.2f}".format(13.949999999999999))
                rd = float("{:.2f}" .format(random.random()))
                
                while sumOne+rd >= 1:
                    rd = float("{:.2f}" .format(random.random()))
                    # print("rd en ciclo ", rd)
                sumOne += rd
                tmp.append(rd)
                # print("Suma uno {} iteracion {}" .format(sumOne, elem))
                diff = 1 - sumOne
                tmp.append(diff)
            battleMatrix.append(tmp)
        # print(battleMatrix)
        for elem in range(nClans):
            battleMatrix[elem].insert(elem, 0)
        # print(battleMatrix)
        return battleMatrix
    else:
        battleMatrix = [[0, 1], [1, 0]]
        # print(battleMatrix)
        return battleMatrix

# In battleMatrix we save the probabilities of each clan to attack the others by order
battleMatrix = list(list())
battleMatrix = fillMatrix(battleMatrix, CLANS)

# in 'clans' is saved the required information of the clans in the following structure: {'number_of_clan': ['amount_of_soldiers', 'probabilities_to_attack', 'intervals_for_montecarlo']}
clans = dict({0: [10, battleMatrix[0], getIntervals(battleMatrix[0], 0)], 1: [20, battleMatrix[1], getIntervals(battleMatrix[1], 1)], 2: [30, battleMatrix[2], getIntervals(battleMatrix[2], 2)]})
# clans = {0: [10, battleMatrix[0], 0], 1: [20, battleMatrix[1]], 2: [30, battleMatrix[2]]}

##################################################################################################################
# Start
##################################################################################################################

# initial state of the clans

with open(filename,"w+",encoding="utf-8") as file:
    printMatrix(list(clans.keys()), battleMatrix, CLANS)
    numSoldiers(clans)
    while len(clans)>1:
        # generate random number of the clan that is going to attack
        rClanIndex = round(random.uniform(0, len(clans)))
        clanKeys = list(clans.keys())
        # print(clanKeys)
        while rClanIndex not in clanKeys:
            # print("rClanIndex ", rClanIndex)
            rClanIndex = round(random.uniform(0, len(clans)))
        # print("Attacking clan: " , rClan)

        file.write("Attacking clan: {}\n" .format(rClanIndex))
        # then we call the function giving permission to the selected clan to attack other clans
        attackSoldier(clans, rClanIndex)
        
        # We need to know if any clan ran out of soldiers
        if countSoldiers(clans) == 0 and len(clans)>1:
            # print("Somebody ran out of soldiers")
            numSoldiers(clans)
            CLANS-=1
            battleMatrix = fillMatrix(battleMatrix, CLANS)
            # print(clans)
            # print(battleMatrix)
            i = 0
            for clan, info in clans.items():
                clans.get(clan)[1] = battleMatrix[i]
                clans.get(clan)[2] = getIntervals(battleMatrix[i], clan)
                i+=1
            # print(clans)
            printMatrix(list(clans.keys()), battleMatrix, CLANS)
        # Now we print the current status of the battle
        
        numSoldiers(clans)
    winner = list(clans.keys())
    file.write("The winner is clan {}!" .format(winner[0]))