# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:23:24 2016

@author: cheeren
"""
a = [1,1,2,3,5,6,11]
b = [0,0,0,0,0,0,0]

for index in range(7):
    b[index] = 2 * a[(index + 1)%7]
    
print (b)

    