# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 12:23:35 2017

@author: saini
"""

import pandas
import random
import numpy
import pyexcel

colnames = ['name', 'number', 'followers']
data = pandas.read_csv('users_100.csv', header=0)

users = list(data.name)

followers_number = list(data.number)

df = pandas.DataFrame(data)

pyexcelData = []
i=0
np_users = numpy.array(users)
for no in followers_number:
    indices = random.sample(range(1, len(users)), no)
    temp = list(np_users[indices])
    temp.insert(0,no)
    temp.insert(0,users[i])
    i+=1
    pyexcelData.append(temp)

pyexcelData.insert(0, ['name', 'number'])
sheet = pyexcel.Sheet(pyexcelData)
sheet.save_as("maindata_100.csv")
pyexcel.free_resources()