# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 14:24:24 2017

@author: Nick
"""

import csv
import numpy
import pandas
import pyexcel
from pprint import pprint


colnames = ['name', 'number']
data = pandas.read_csv('maindata_10.csv', header=0)

userdata = pandas.read_csv('users_10.csv', header=0)
userdata_df = pandas.DataFrame(userdata)

users = list(data.name)
g = len(users) #total number of users in the network
print "List of Unique Users : "
pprint(users)

followers_number = list(data.number)

users_tag = {} 
print "\n"
print "Generating Tags for the users -->"
# Generate Tags for each user to be referenced
for i in range(0, g):
    users_tag[users[i]] = i

pprint(users_tag)
print "\n"


#Followers list for each user
print "Gathering Follower Data...", "\n"
followers = []
flag = 0
x=0
records = pyexcel.iget_records(file_name = 'maindata_10.csv')
with open('maindata_10.csv') as myFile:  
    reader = csv.reader(myFile)
    for row in reader:
        if(flag==1):
            row = row[2:followers_number[x]+2]
            followers.append(row)
            x+=1
        else:
            flag=1
            continue


print "Generating the SocioMatrix for the Network -->"
# TODO: Generate the SocioMatrix
k=0
socioMatrix = numpy.zeros([g, g]).astype(int).tolist()
for user_followers in followers:
        for i in user_followers:
            socioMatrix[k][users_tag[i]] += 1
        k+=1

pprint(socioMatrix)


# Properties of the Network----------------------------

# TODO: Mean In Degree
inDegree = numpy.zeros(g).astype(int).tolist()
meanInDegree = 0
for i in range(0, g):
    for j in socioMatrix:
        if(j[i]!=0):
            inDegree[i]+=1
                        
for i in inDegree:
    meanInDegree += i

meanInDegree /=float(g)        
userdata_df['InDegree'] = inDegree


# TODO: Mean Out Degree
outDegree = followers_number
meanOutDegree = 0
for i in outDegree:
    meanOutDegree += i

meanOutDegree /= float(g)
userdata_df['OutDegree'] = outDegree


# TODO: Variance In Degree
varianceIndegree = 0
for i in range(0, g):
    temp = inDegree[i]-meanInDegree
    temp = temp**2
    varianceIndegree += temp

varianceIndegree /= float(g)

        
# TODO: Variance Out Degree
varianceOutdegree = 0
for i in range(0, g):
    temp = outDegree[i] - meanOutDegree
    temp = temp**2
    varianceOutdegree += temp

varianceOutdegree /= float(g)

       
# TODO: Density of the Network
totalPossibleLines = g*(g-1)
density = 0
for i in (inDegree+outDegree):
    density += i

density /= float(totalPossibleLines)


# TODO: Group Degree Centrality

        
# TODO: Group Closeness Centrality
        
# TODO: Group Betweenness Centrality

# TODO: Global Clustering Coefficient



# Properties of Actor----------------------------------- 
        
# TODO: Degree Centrality
        


# TODO: Closeness Centrality
        


# TODO: Betweenness Centrality
        
        

# TODO: Eigen Vector Centrality
        
        
        
# TODO: Local Clustering Coefficient
