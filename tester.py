# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 16:04:31 2017

@author: saini
"""

import csv

with open('maindata_10.csv') as myFile:  
    reader = csv.reader(myFile)
    for row in reader:
        print(row)