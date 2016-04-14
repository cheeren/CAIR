# -*- coding: utf-8 -*-
"""
Funtional version of Content Aware Image Resizing
    - Avidan, Shamir (2007)
"""
from PIL import Image
img = Image.open('mtRanier.jpg')
img.thumbnail((10,10), Image.ANTIALIAS)
pw,ph = img.size

#load image into rows of rgb pixels
rows = list(map(lambda y : list(map(lambda x : img.load()[x,y], range(pw))), range(ph)))
    
# not functional - writes pixels out to a .jpg
def writeImage(rows):
    smIm = Image.new('RGB', (pw-1, ph), 'white')
    for y in range(ph):
        for x in range(pw-1):
            smIm.putpixel((x,y),rows[y][x])           
    smIm.save("mtRanierONE", "JPEG")

# returns a list of lists of pixel colors
def removeSeam(seam,rows):
    smRow = lambda row: [rows[row][x] for x in range(pw) if not x == seam[row]]
    return list(map(smRow,range(ph)))
      
#computes sum of squared differences between adjacent pixels
def energy(row, col):
    sqdiff = lambda pair: (pair[0]-pair[1])*(pair[0]-pair[1])
    zipPixel = lambda k: zip(row[col],row[k]) # zip rgb tuples
    return sum(map(sqdiff, zipPixel((col-1)%pw))) + sum(map(sqdiff, zipPixel((col+1)%pw)))
         
#returns a tuple: (total energy,[seam columns])    
def seamAtPixel(row, col, rows):
    if row==0:
        return (energy(rows[row],col),[col])
    else:
        costsPrev = map(lambda x : seamAtPixel(row-1, x, rows), [(col-1)%pw,col%pw,(col+1)%pw])
        costsIncludingThis = map(lambda c : (c[0] + energy(rows[row],col), c[1] + [col]), costsPrev)
        return min(costsIncludingThis, key=lambda x : x[0])

#returns a tuple: (total energy,[seam columns])    
def findSeam(pic):
    return min(map(seamAtPixel,[ph-1]*pw,range(pw),[pic]*pw), key=lambda x : x[0])
               
solution=findSeam(rows)
removedRows=removeSeam(solution[1],rows) 
writeImage(removedRows)


        

    




    
    