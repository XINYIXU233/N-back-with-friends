#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 10:26:42 2023

@author: luoqi
"""

## This script aims to read the data files and draw plots
## We drawed a barplot for accuracy, both barplot and violin plot for reaction time

import pandas as pd
import matplotlib.pyplot as plt
import glob as gb
import numpy as np

# 1.read data files
files = gb.glob('example_data/data*.xlsx') 
files.reverse()
# read data for all subjects
data = []
for file in files:
    data.append(pd.read_excel(file))

# concatenate reponse time and acc of each subject into separate lists, rts and accs
newdata = pd.DataFrame(columns=['ID','Block','Reaction_Time','Correct'])
for i in range(len(data)):
    
    subdata = data[i]
    subdata.columns=subdata.iloc[0] #set the first row as column names
    subdata = subdata[1:] #then delete the first row
    subdata['Reaction_Time']=subdata['Reaction_Time'].fillna(0) #set all nan values as 0
    newdata = newdata.append(subdata[['ID','Block','Reaction_Time','Correct']])

# reaction time, accuracy rate and correct for each block are saved separately in rts accs and corrects
rts = [] # save the reaction times for each block
meanrts = [] # save the average reaction time for each block
corrects = [] # save the correct for each block
accs=[] #save the acc rate for each block
for block in range(1,max(newdata['Block'])+1):
    
    rt = newdata.loc[newdata['Block'] == block,'Reaction_Time']
    rt = rt.tolist()
    rts.append(rt)
    meanrts.append(sum(rt)/len(rt))
    correct = newdata.loc[newdata['Block'] == block,'Correct']
    corrects.append(correct)
    accs.append(sum(correct)/len(correct))


# 2.create plots
fig, ax = plt.subplots(3,1,figsize = (6,16),sharex = 'row')
blocks = ['1-back','2-back','3-back']
ind = range(len(blocks))
plt.setp(ax,xticks = ind ,xticklabels=blocks)

ax[0].bar(ind,meanrts,width = 0.2, align='center', alpha=0.5)
ax[0].title.set_text('mean reaction time')

ax[1].bar(ind,accs,width = 0.2, align='center', alpha=0.5)
ax[1].title.set_text('accuracy rate')
ax[1].set(ylim = (min(accs)-0.1,1))

ax[2].violinplot(rts, ind, points=20, widths=0.3,
                     showmeans=True, showextrema=True, showmedians=True)
ax[2].title.set_text('reaction times')

plt.savefig('plots.png')
plt.show()



















    
