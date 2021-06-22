# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 15:51:06 2021

@author: Kathi
"""



import xlsxwriter
import xlrd
import random
#randomize the seed
random.seed(1234)

path = r"C:\Users\Kathi\Documents\Studium Kognitionswissenschaft\4. Semester\Teamprojekt visuelle Wahrnehmung\Programmieren\ExperimentProgrammierung"


randomPairs = True 

listDark = []
listLight = [] 

#create lists of shapenames
def picName(number, color):
    return color + str(number) + ".bmp"
for i in range(1, 25):
    listDark.append(picName(i, "dark"))
    listLight.append(picName(i, "light"))

#shuffle pairs if necessary
if(randomPairs):
    # Shuffle two lists with same order
    # Using zip() + * operator + shuffle()
    temp = list(zip(listDark, listLight))
    random.shuffle(temp)
    listDark, listLight = zip(*temp)

row = 0
col = 0

#number of trials
num_trials = 120

#array with numbers (starting/second shape)
order = [x % 24 for x in range(num_trials)]
#randomizing the order of the initial shapes
random.shuffle(order)
#print(order)

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

#array with numbers of repetition (this and next position; 1 = second element)
repetition = [(x % 9) for x in range(num_trials)]
random.shuffle(repetition)
print(repetition)
    

#create workbook object for shapes file
workbookStart = xlsxwriter.Workbook(path + r"\shapes.xlsx")
worksheetShapes = workbookStart.add_worksheet()

#create input of shapes file 
#for i in range(len(listDark)):
#    worksheetShapes.write(0, i, listDark[i])
#    worksheetShapes.write(1, i, listLight[i])

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

#create a workbook object for stimuli file
workbook = xlsxwriter.Workbook(path + r"\stimuli.xlsx")
worksheet = workbook.add_worksheet()

workbook_shapes = xlrd.open_workbook(path + r"\shapes.xlsx")
shapesheet = workbook_shapes.sheet_by_index(0)


rowList = []



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

listShapes = listDark[:12] + listLight[:12] + listDark[12:] + listLight[12:] 
print(order)

row = 0
repidx = 0

for i in order:
    element = listShapes[i]
    #print(element)
    constTrial = const[i]
    #print(constTrial)
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
            #print(element, nxt)
            rowList.append(nxt)
        #else add next element in different color
        else:
            nxt = getNeighbor(element, i, constTrial, j)
            #print(element, nxt)
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
    
 

    
workbookStart.close()
workbook.close()
