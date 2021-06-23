# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 15:51:06 2021

@author: Kathi
"""


import xlsxwriter
import random

#########################
##### GENERAL CODE ######
#########################

#randomize the seed!
random.seed(1234)
#random.seed()
#not important for psychopy, has to be adapted later
path = r"C:\Users\Kathi\Documents\Studium Kognitionswissenschaft\4. Semester\Teamprojekt visuelle Wahrnehmung\Programmieren\ExperimentProgrammierung"

#we always want to change the pairs for every participant
#could be left out
randomPairs = True 

#definitions that will be important later
#variables that are used in the code

listDark = []
listLight = [] 
listRed = []
listGreen = []

#number of trials
num_trials = 120

#create lists of shapenames
def picName(number, color):
    return color + str(number) + ".bmp"

for i in range(1, 25):
    listDark.append(picName(i, "dark"))
    listLight.append(picName(i, "light"))
    
for i in range(1, 25):
    listRed.append(picName(i, "red"))
    listGreen.append(picName(i, "green"))

#shuffle pairs if necessary
if(randomPairs):
    # Shuffle two lists with same order
    # Using zip() + * operator + shuffle()
    temp = list(zip(listDark, listLight))
    random.shuffle(temp)
    listDark, listLight = zip(*temp)
    temp = list(zip(listGreen, listRed))
    random.shuffle(temp)
    listGreen, listRed = zip(*temp)
    

#array with colors
color = ["g", "g", "g", "g", "g", "g", "r", "r", "r", "r", "r", "r"] * 4
print(color)


#array with numbers for constellation of pairs
const1 = [x % 3 for x in range(6)]
const2 = [(x % 3) + 3 for x in range(6)]
# randomizing the order of constellations
random.shuffle(const1)
random.shuffle(const2)
const = (const1 + const2) * 4
print(const)


#create workbook object for shapes file
workbookStart = xlsxwriter.Workbook(path + r"\shapes.xlsx")
worksheetShapes = workbookStart.add_worksheet()


#create input of shapes file 
for i in range(12):
    worksheetShapes.write(i, 0, listDark[i])
    worksheetShapes.write(i + 12, 0, listLight[i])
    worksheetShapes.write(i + 24, 0, listDark[i + 12])
    worksheetShapes.write(i + 36, 0, listLight[i + 12])
    worksheetShapes.write(i, 1, color[i])
    worksheetShapes.write(i + 12, 1, color[i + 12])
    worksheetShapes.write(i + 24, 1, color[i + 24])
    worksheetShapes.write(i + 36, 1, color[i + 36])
    worksheetShapes.write(i, 2, const[i])
    worksheetShapes.write(i + 12, 2, const[i + 12])
    worksheetShapes.write(i + 24, 2, const[i + 24])
    worksheetShapes.write(i + 36, 2, const[i + 36])

#same list internal in python (access to shapes.xlsx file theoretically unnecessary)    
listShapes = listDark[:12] + listLight[:12] + listDark[12:] + listLight[12:] 

listColors = listGreen[:12] + listRed[:12] + listGreen[12:] + listRed[12:] 

#######################################################
####### code for SECOND PART of the experiment ########
#######################################################

#create a workbook object for stimuli file
workbook = xlsxwriter.Workbook(path + r"\stimuli.xlsx")
worksheet = workbook.add_worksheet()

#array with numbers (starting/second shape)
order = [x % 24 for x in range(num_trials)]
#randomizing the order of the initial shapes
random.shuffle(order)
#print(order)


#array with numbers of repetition (this and next position; 1 = second element)
repetition = [(x % 9) for x in range(num_trials)]
random.shuffle(repetition)
print(repetition)

rowList = []
row = 0
repidx = 0

#function which gives back the first of the eleven figures of a row
#different shape and color than randomly chosen "start/second element"
def getFirst(element, i, constTrial):
    first3 = []
    idx1 = const.index(constTrial)
    idx2 = idx1 + 1 + const[idx1 + 1:].index(constTrial)
    if(idx1 == i):
        first3.append(listShapes[idx1 + 36])
        first3.append(listShapes[idx2 + 36])
        first3.append(listShapes[idx2 + 12])
    elif(idx1 + 12 == i):
        first3.append(listShapes[idx1 + 24])
        first3.append(listShapes[idx2 + 24])
        first3.append(listShapes[idx2])
    elif(idx2 == i):
        first3.append(listShapes[idx1 + 12])
        first3.append(listShapes[idx1 + 36])
        first3.append(listShapes[idx2 + 36])
    elif(idx2 + 12 == i):
        first3.append(listShapes[idx1])
        first3.append(listShapes[idx1 + 24])
        first3.append(listShapes[idx2 + 24])        
    else:
        print("Error")
    #print(first3)
    return random.choice(first3)

#find next figure:
#either partnerelement in the opposite lightness (j uneven)
#or first Element of other pair in oppostie lightness (j even)
def getNeighbor(element, i, constTrial, j):
    nxt = "null"
    #print(element)
    if(j % 2 == 0):
        idx1 = const.index(constTrial) #first element pair 1
        idx2 = idx1 + 1 + const[idx1 + 1:].index(constTrial) #first element pair 2
        if(listShapes[idx1] == element): #dark
            nxt = listShapes[idx1 + 36]
        elif(listShapes[idx1 + 12] == element): #light
            nxt = listShapes[idx1 + 24] 
        elif(listShapes[idx2] == element): #dark
            nxt = listShapes[idx2 + 36]
        elif(listShapes[idx2 + 12] == element): #light
            nxt = listShapes[idx2 + 24]      
        else:
            print("Error")
    else:
        idx1 = const.index(constTrial) #first element pair 1
        idx2 = idx1 + 1 + const[idx1 + 1:].index(constTrial) #first element pair 2
        if(listShapes[idx1 + 24] == element): #dark
            nxt = listShapes[idx2 + 12] #light
        elif(listShapes[idx1 + 36] == element): #light
            nxt = listShapes[idx2] #dark
        elif(listShapes[idx2 + 24] == element):
            nxt = listShapes[idx1 + 12]
        elif(listShapes[idx2 + 36] == element):
            nxt = listShapes[idx1]      
        else:
            print("Error")
    return nxt

#find partnerelement in the same color
def getRepetition(element, i, constTrial, j):
    if(j % 2 == 0):
        idx1 = const.index(constTrial) #first element pair 1
        idx2 = idx1 + 1 + const[idx1 + 1:].index(constTrial) #first element pair 2
        if(listShapes[idx1] == element): #dark
            nxt = listShapes[idx1 + 24]
        elif(listShapes[idx1 + 12] == element): #light
            nxt = listShapes[idx1 + 36] 
        elif(listShapes[idx2] == element): #dark
            nxt = listShapes[idx2 + 24]
        elif(listShapes[idx2 + 12] == element): #light
            nxt = listShapes[idx2 + 36]      
        else:
            print("Error")
    else:
        idx1 = const.index(constTrial) #first element pair 1
        idx2 = idx1 + 1 + const[idx1 + 1:].index(constTrial) #first element pair 2
        if(listShapes[idx1 + 24] == element):
            nxt = listShapes[idx2]
        elif(listShapes[idx1 + 36] == element):
            nxt = listShapes[idx2 + 12]
        elif(listShapes[idx2 + 24] == element):
            nxt = listShapes[idx1]
        elif(listShapes[idx2 + 36] == element):
            nxt = listShapes[idx1 + 12]      
        else:
            print("Error")
    return nxt

#create the file stimuli.xlsx with 120 rows and 11 columns
for i in order:
    element = listShapes[i]
    constTrial = const[i]
    first = getFirst(element, i, constTrial)
    rowList.append(first)
    rowList.append(element)
    rep = repetition[repidx]
    repidx = repidx + 1
    print("rep:" + str(rep))
    for j in range(9):
        #if repetition is reached, add next element in same color
        if(rep == j):
            nxt = getRepetition(element, i, constTrial, j)
            rowList.append(nxt)
        #else add next element in different color
        else:
            nxt = getNeighbor(element, i, constTrial, j)
            rowList.append(nxt)
        #this new element is the basis for the following element
        element = nxt
    #print(rowList)
    #write row in the excel table
    for k in range(len(rowList)):
        worksheet.write(row, k, rowList[k])
    #count and delete old list for next iteration
    row = row + 1
    rowList = []   
    
 
#######################################################
####### code for FIRST PART of the experiment ########
#######################################################   
 
#create a workbook object for stimuli file
workbookStream = xlsxwriter.Workbook(path + r"\stream.xlsx")
streamsheet = workbookStream.add_worksheet()

# For each observer, 12 shapes were assigned to the red group, 
# and the remaining 12 shapes were assigned to the green group. 
# Within each color, the 12 shapes were further divided into six groups of 
# two shapes. Separate temporal streams were first generated for each color, 
# consisting of 24 repetitions of each tupel randomly intermixed. 
# To manipulate attention (as described below), we also included in each stream 
# 24 instances in which the second shape of a tupel was immediately repeated 
# (e.g., ABBCD). Each stream thus included a total of 312 shapes


# every pair occurs 24 times (24*24) and 24 repetitions occurs futhermore in each (!)stream
# -> 624 = 24*24 + 24 + 24 = 312 + 312 shapes in total

#array with green shapes (first part of the pairs) in order of access
#144 first shapes of pair (144 + 144 = 288)
green = [x % 12 for x in range(6*24)]
rndmGreen = []
x = -1
y = -1
z = -1
for i in range(6*24):
    if(len(green) > 4):
        r = random.sample(green, 1)[0]
        while(z == r or (x == z and y == r)):
            r = random.sample(green, 1)[0]
        rndmGreen.append(r)
        green.remove(r)
        x = y
        y = z
        z = r
    else: 
        r = random.sample(green, 1)[0]
        if (z == r or (x == z and y == r)):
            r = random.sample(green, 1)[0]
        rndmGreen.append(r)
        green.remove(r)
        x = y
        y = z
        z = r
    
#randomizing the order of the shapes
#random.shuffle(rndmGreen)
print(rndmGreen)

#array with red shapes (first part of the pairs) in order of access
red = [(x % 12) + 12 for x in range(6*24)]
#randomizing the order of the shapes
#random.shuffle(rndmRed)
rndmRed = []
x = -1
y = -1
z = -1
for i in range(6*24):
    if(len(red) > 4):
        r = random.sample(red, 1)[0]
        while(z == r or (x == z and y == r)):
            r = random.sample(red, 1)[0]
        rndmRed.append(r)
        red.remove(r)
        x = y
        y = z
        z = r
    else: 
        r = random.sample(red, 1)[0]
        if (z == r or (x == z and y == r)):
            r = random.sample(red, 1)[0]
        rndmRed.append(r)
        red.remove(r)
        x = y
        y = z
        z = r
print(rndmRed)

#array with random numbers of repetition (24 repetitions in each stream)
#(the second shape of this pair will be repeated)
repSecond = [x for x in range(6*24)]
random.shuffle(repSecond)
repSecondG = repSecond[:24]
repSecondR = repSecond[24:48]
repSecondG.sort()
repSecondR.sort()
#print(repSecondG)
#print(len(repSecondG))
#print(repSecondR)
#print(len(repSecondR))

redStream = []
greenStream = []

def getRepPair(i, green):
    if(green):
        greenStream.append(listColors[rndmGreen[i]])
        greenStream.append(listColors[rndmGreen[i] + 24])
        greenStream.append(listColors[rndmGreen[i] + 24])
    else:
        redStream.append(listColors[rndmRed[i]])
        redStream.append(listColors[rndmRed[i] + 24])
        redStream.append(listColors[rndmRed[i] + 24])
    
def getPair(i, green):
    if(green):
        greenStream.append(listColors[rndmGreen[i]])
        greenStream.append(listColors[rndmGreen[i] + 24])
    else:
        redStream.append(listColors[rndmRed[i]])
        redStream.append(listColors[rndmRed[i] + 24])

j = 0

#create the green stream
for i in range(6*24):
    if(j < 24 and i == repSecondG[j]):
        getRepPair(i, True)
        j = j + 1
    else:
        getPair(i, True)
   
k = 0

#create the red stream
for i in range(6*24):
    #print("red: " + str(k) + " " + str(i) + " " + str(repSecondR[k]))
    if(k < 24 and i == repSecondR[k]):
        getRepPair(i, False)
        k = k + 1
    else:
        getPair(i, False)

#print(redStream)
#print(greenStream)
#print(len(redStream))
#print(len(greenStream))

interleaved = []

ctr = [(x % 2) for x in range(624)]
random.shuffle(ctr)
g = 0
r = 0
for i in ctr:
    if(i == 0):
        interleaved.append(greenStream[g])
        g = g + 1
    else:
        interleaved.append(redStream[r])
        r = r + 1
        
#print(interleaved)
#print(len(interleaved))

for k in range(len(interleaved)):
    streamsheet.write(k, 0, interleaved[k])

workbookStart.close()
workbook.close()
workbookStream.close()
