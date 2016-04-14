# -*- coding: utf-8 -*-
"""
    Imperative version of Content Aware Image Resizing
        - Avidan, Shamir (2007)
    cinda heeren, 4/2016, UBC
"""
from PIL import Image

    
# not functional - writes pixels out to a .jpg
def writeImage(rows,width):
    smIm = Image.new('RGB', (width, ph), 'white')
    for y in range(ph):
        for x in range(width):
            smIm.putpixel((x,y),rows[y][x])           
    smIm.save("ocean" + str(width), "png")
    
def buildRow(row,prevCosts,width):
    retRow = []
    for x in range(width):
        costsIncludingThis = map(
            lambda c : (c[0] + energy(row,x,width), c[1] + [x]), 
            [prevCosts[(x-1)%width]] + [prevCosts[x%width]] + [prevCosts[(x+1)%width]])
        retRow.append(min(costsIncludingThis,key=lambda x : x[0]))
    return retRow
       
def buildTable(rows,width):
    retTable = [] #make empty table will insert rows of (predecessor,cost) pairs
           
    firstRow = []
    for x in range(width):
        firstRow.append((energy(rows[0],x,width),[x]))
    retTable.append(firstRow)        
    
    for y in range(1,ph):
        retTable.append(buildRow(rows[y],retTable[y-1],width))
        
    return retTable

# returns a list of lists of pixel colors
def removeSeam(seam,rows,width):
    smRow = lambda row: [rows[row][x] for x in range(width) if not x == seam[row]]
    return list(map(smRow,range(ph)))
# returns a list of lists of pixel colors, including the red seam
def redSeam(seam,rows,width):
    smRow = lambda row: [rows[row][x] for x in range(seam[row])] + [(255,0,0)] + [rows[row][x] for x in range(width) if x > seam[row]]
    return list(map(smRow,range(ph))) 
    
#computes sum of squared differences between adjacent pixels
#def energy(row, col, width):
#    sqdiff = lambda pair: (pair[0]-pair[1])*(pair[0]-pair[1])
#    zipPixel = lambda k: zip(row[col],row[k]) # zip rgb tuples
#    return sum(map(sqdiff, zipPixel((col-1)%width))) + sum(map(sqdiff, zipPixel((col+1)%width)))
#computes absolute differences between adjacent pixels
def energy(row, col, width):
    absdiff = lambda pair: abs(pair[0]-pair[1])
    zipPixel = lambda k: zip(row[col],row[k]) # zip rgb tuples
    return sum(map(absdiff, zipPixel((col-1)%width))) + sum(map(absdiff, zipPixel((col+1)%width)))         
#returns a tuple: (total energy,[seam columns])    
def seamAtPixel(row, col, width):
    return costPath[row][col]

#returns a tuple: (total energy,[seam columns])    
def findSeam(rows,width):
    return min(map(seamAtPixel,[ph-1]*width,range(width),[rows]*width), key=lambda x : x[0])

img = Image.open('ocean.jpg')
img.thumbnail((300,300), Image.ANTIALIAS)
pw,ph = img.size
numToRemove = int(pw/3)

#load image into rows of rgb pixels
rows = list(map(lambda y : list(map(lambda x : img.load()[x,y], range(pw))), range(ph)))

for i in range(numToRemove):
    costPath = buildTable(rows,pw-i) # creates a table of (cost, path) pairs
    solution=findSeam(rows,pw-i) # work is done here!

    redRows = redSeam(solution[1],rows,pw-i) 
    removedRows = removeSeam(solution[1],rows,pw-i)
    
    rows = list(removedRows)

    if i%20 == 0:
        writeImage(redRows,pw-i)
        writeImage(removedRows,pw-1-i)

writeImage(redRows,pw-numToRemove)
writeImage(removedRows,pw-1-numToRemove)



        

    




    
    