import random
import numpy as np

a = 0
b = 1
N = 1
filename = 'battleResults.txt'

# function for montecarlo
def f(x):
    return x**2


def printMatrix(matrix, size):
    for i in range(size):
        file.write("  {}\t" .format(i))
    file.write("\n")
    row = 0
    for i in matrix:
        file.write("{} " .format(row))
        for j in i:
            file.write("{} " .format(str(float(j))))
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
        print(info[0])
        if info[0] == 0:
            print("Clan {} was annihilated" .format(clan))
            clans.pop(clan)
            return 0


def attackSoldier(dictClans, attacker):
    probs = dictClans.get(attacker)[2]
    # print("Probabilities of attacking for clan ", attacker)
    # print(probs)
    # file.write("Probabilities of attacking for clan {}\n" .format(attacker))
    attacked = montecarlo(probs)
    if attacked == attacker: # this condition is set so if montecarlo generates the same clan as objective for the attackiong clan, it generates a new objective
        while attacked == attacker:
            attacked = montecarlo(probs)
            # print("Attacked clan number: ", attacked)
            file.write("Attacked clan number: {}\n" .format(attacked))
    file.write("Clan {} attacked clan {}!\n" .format(attacker, attacked))
    # print("Clan {} attacked clan {}!" .format(attacker, attacked))
    dictClans.get(attacked)[0]-=1


# In battleMatrix we save the probabilities of each clan to attack the others by order
battleMatrix = [[ 0 , 0.4, 0.6],
                [0.2,  0 , 0.8],
                [0.7, 0.3,  0 ]]

# in 'clans' is saved the required information of the clans in the following structure: {'number_of_clan': ['amount_of_soldiers', 'probabilities_to_attack', 'intervals_for_montecarlo']}
clans = dict({0: [10, battleMatrix[0], getIntervals(battleMatrix[0], 0)], 1: [20, battleMatrix[1], getIntervals(battleMatrix[1], 1)], 2: [30, battleMatrix[2], getIntervals(battleMatrix[2], 2)]})


##################################################################################################################
# Start
##################################################################################################################

# initial state of the clans

with open(filename,"w+",encoding="utf-8") as file:
    printMatrix(battleMatrix, 3)
    numSoldiers(clans)
    for i in range(25):
        # generate random number of the clan that is going to attack
        rClan = random.randint(0, len(clans)-1)
        # print("Attacking clan: " , rClan)

        file.write("Attacking clan: {}\n" .format(rClan))
        # then we call the function giving permission to the selected clan to attack other clans
        attackSoldier(clans, rClan)
        
        # We need to know if any clan ran out of soldiers
        if countSoldiers(clans) == 0:
            print("Somebody ran out of soldiers")
            numSoldiers(clans)
            break
        # Now we print the current status of the battle
        numSoldiers(clans)