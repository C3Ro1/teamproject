# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 15:51:06 2021

@author: Kathi
"""
print("Hello World")

print("Hello World!")

#Hello World


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
repetition = [(x % 9) + 1 for x in range(num_trials)]
random.shuffle(repetition)
    

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
    idx = const.index(constTrial)
    return idx

for i in order:
    element = shapesheet.cell_value(i, 0)
    print(element)
    constTrial = shapesheet.cell_value(i, 1)
    print("constTrial: " + str(constTrial))
    #rowList.append(getFirst(element, i, constTrial))
    rowList.append(element)
    rep = repetition[i]
    #getNeighbor(element)
    print(getFirst(element, i, constTrial))
 

workbookStart.close()
