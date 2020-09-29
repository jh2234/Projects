# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:19:41 2019

@author: morga
"""

#matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# use seaborn plotting defaults
import seaborn as sns; sns.set()

#import data 
X = np.load('ClassifierDataX.npy')
y = np.load('ClassifierDatay.npy')


#make a fcn f
def f(x,w,b):
    return sum([w[i]*x[i] for i in range(len(w))]) + b

#import the svc module 
from sklearn.svm import SVC # "Support vector classifier"
model = SVC(kernel='linear', C=100)
model.fit(X, y)
print(model)

#find b value 
b_learn = model.intercept_[0]
b_learn
print(b_learn)

#find w value 
w_learn = (model.coef_)[0]
w_learn
print(w_learn)

#print
print("y[0] = ", y[0])
print("learned function of X[0] = ", f(X[0], w_learn, b_learn) )


print("T/F y[i] f(X[i]))")
I = range(len(y))
for i in I:
    sign = f(X[i],w_learn,b_learn)*y[i] > 0
    print(sign," ", y[i]," ", f(X[i],w_learn,b_learn))
    print("Number true:", sum([f(X[i],w_learn,b_learn)*y[i] > 0 for i in I]))
    print("Number false:", sum([f(X[i],w_learn,b_learn)*y[i] < 0 for i in I]))

y_predict = model.predict(X)
print(y_predict)
print(y==y_predict) #checking if model is accurate 

import json
data=json.load(open("new-data.json"))
houses = []
for x in data.keys():
    if 'House' in x:
        houses.append(x)
X_new = [[data[h]['Average Purchase'], data[h]['# times used service'], data[h]['max distance to restaurant'], data[h]['min distance to restaurant']] for h in houses]

#print(X_new)
print(houses)
y_new = model.predict(X_new)
print(y_new)

#print(data.keys())
