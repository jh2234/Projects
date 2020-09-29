# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 09:27:34 2019

@author: morga
"""


import pandas as pd
import json
import matplotlib.pyplot as plt   #importing modules 
from gurobipy import *
import time


df = pd.read_csv("Blacksburg-Restaurants-And-Houses.csv")   #reading in data 
data = json.load(open("data.json", "r"))
places = list(data.keys())
restaurants = places[0:14] #set of restaurants
houses = places[14:]  #set of houses 


#def plot_locations_and_edges(Edges):
    #for (i,j) in Edges:
    #    plt.plot([location[i,0], location[j,0]], [location[i,1], location[j,1]], color = "blue", linestyle = "dashed", linewidth= 0.5)
   # x,y = np.transpose(location);

   # plt.scatter(x,y, color = "red");
   # plt.xlabel("x-coordinate")
   # plt.ylabel("y-coordinate")
   # plt.title("Houses to Restaurants")
   # plt.show()


start = time.clock()

# Create a new model
m = Model("Drop n Dine")

# Create set
#sets are places and restaurants from above code 
#not sure how to get distances 

# Create variables
x = m.addVars(houses,restaurants, vtype=GRB.BINARY, name="x")


# Set objective
##min the sum of the distances*xij 
m.setObjective(sum(data[i]['Distance'][j]*x[i,j] for i in houses for j in restaurants), GRB.MINIMIZE)

# Add constraint:
## up to 5 houses assigned to each restaurant
m.addConstrs((sum(x[i, j] for i in houses) <= 5 for j in restaurants), "Maximum of 5 houses constraint")

# Add constraint: 
## can only assign one house to one restaurant
m.addConstrs((sum(x[i,j] for j in restaurants) == 1 for i in houses), "One house to one restaurant") 


# Optimize model
m.optimize()

#End the timer
end = time.clock()
print("Time to run code: ", end - start)
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)
################

x_sol = [ [ x[i,j].x for i in houses] for j in restaurants]
edges = [(i,j) for i in houses for j in restaurants if x[i,j].x ==1]

#for i in houses:
   # if sum(x[i,j].x == 0)

#plotting houses and restaurants 
x = [data[place]['Coordinates'][0] for place in houses]
y = [data[place]['Coordinates'][1] for place in houses]
plt.scatter(x,y, color='red', label="Houses")
x = [data[place]['Coordinates'][0] for place in restaurants]
y = [data[place]['Coordinates'][1] for place in restaurants]
plt.scatter(x,y, color='blue', label = "Restaurants")
plt.title("Location of Houses and Restaurants")
plt.legend()





for (i,j) in edges:
        plt.plot([data[i]['Coordinates'][0], data[j]['Coordinates'][0]], [data[i]['Coordinates'][1], data[j]['Coordinates'][1]], color = "black", linestyle = "dashed", linewidth= 0.5)
    
        plt.xlabel("longitude coordinates")
        plt.ylabel("latitude coordinates")
    #plt.title("Matchings of Rival Teams")
plt.show()