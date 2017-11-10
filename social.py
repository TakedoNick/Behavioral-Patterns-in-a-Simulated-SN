# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 14:24:24 2017

@author: Nick
"""

import csv
import numpy
import pandas
import pyexcel
import math
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plot
from community import community_louvain

from collections import defaultdict


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

np_socioMatrix = numpy.array(socioMatrix)
G = nx.DiGraph(np_socioMatrix)

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




# Properties of Actor----------------------------------- 
# TODO: Degree Centrality
degreeCentrality = numpy.zeros(g).tolist()
for i in range(0, g):
    degreeCentrality[i] = outDegree[i]/float(g-1)      

userdata_df['Degree Centrality'] = degreeCentrality


# TODO: Closeness Centrality
# Highest Time Complexity
"""
closenessCentrality = numpy.zeros(g).tolist()
reachableActors = numpy.zeros(g).astype(int).tolist()       
fairness = numpy.zeros(g).astype(int).tolist()



for i in range(0, g):
    closenessCentrality[i] = (reachableActors[i]**2)*(g-1)/float(fairness[i])
   
"""
closenessCentrality = nx.closeness_centrality(G)
userdata_df['Closeness Centrality'] = closenessCentrality.values()

# TODO: Betweenness Centrality
betweennessCentrality = nx.betweenness_centrality(G)
userdata_df['Betweenness Centrality'] = betweennessCentrality.values()

# TODO: Eigen Vector Centrality
eigenVectorCentrality = nx.eigenvector_centrality(G)
userdata_df['EigenVector Centrality'] = eigenVectorCentrality.values()
        
    


# Properties of the Network----------------------------
# TODO: Group Degree Centrality

        
# TODO: Group Closeness Centrality
        
# TODO: Group Betweenness Centrality

# TODO: Graph Transitivity
graphTransitivity = nx.transitivity(G)


userdata_df.to_csv('processsedData.csv', encoding='utf-8', index=False)

# Visualization of the Network
part = community_louvain.best_partition(G)
values = [part.get(node) for node in G.nodes()]

nx.draw_spring(G, cmap = plot.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)