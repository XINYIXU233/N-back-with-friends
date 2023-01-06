# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 21:29:41 2022

@author: wyf
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 15:57:22 2022

@author: luoqi
"""

import random
import pandas as pd
from psychopy import visual, event, core
from psychopy.hardware import keyboard
import nsequence_generator

#1.Preparation
# record information
ID = input("Participant ID: ") #please enter the participant ID here. 
item_number = 25
correct_number = 5

# create the window
win = visual.Window(size = (800, 600), units = 'pix', color = "black")
# create objects
fixation = visual.TextStim(win, "+", color = "white")
letter_display = visual.TextStim(win, color = "white")
welcome = visual.TextStim(win, "Welcome to the N-back experiment!", color = "white")
thankyou = visual.TextStim(win, "Thank you for participating the experiment!", color = "white")

#draw welcome information
welcome.draw()
win.flip()

core.wait(3)
win.flip()


# function for creating instruction for each block
def instruction_display(n):
    if n == 1:
        text = visual.TextStim(win, f"This is a {n}-back trial. \n"
                                    f"When the letter of current trial is same as the last letter, press 'Y'. \n"
                                    "Press Space if you understand the instruction.", color="white")
    else:
        text = visual.TextStim(win, f"This is a {n}-back trial. \n"
                                    f"When the letter of current trial is same as {n} letters ago, press 'Y'. \n"
                                    "Press Space if you understand the instruction.", color="white")

    return text

#prepare keyboards
kb = keyboard.Keyboard()


# Experiment: participants choose which n-back they would like to do and when to stop the exp by themselves.
answer_list = []
n_sequence = []
trial_list = []

for n in range(1,4):
    
    # clear three temporary lists
    answer_list_temp = []
    n_sequence_temp = []
    trial_list_temp = []
    
    # create answer_list, n_sequence, and trial_list
    # since they are writen in loop, I create an empty list before the loop and append new lists to the previous ones
    answer_list_temp = nsequence_generator.answer_list(n, item_number, correct_number)
    n_sequence_temp = nsequence_generator.n_sequence(n, answer_list_temp)
    trial_list_temp = nsequence_generator.trial_list(ID, answer_list_temp, n_sequence_temp, n)
    
    # display the instruction
    instruction = instruction_display(n)
    instruction.draw()
    win.flip()
    event.waitKeys(keyList = 'space') #wait for space to continue
    
    
    # display the fixation
    fixation.draw()
    win.flip()
    core.wait(2.5)
    win.flip()
    core.wait(2)
    
    correct_n = 0         #count correct trials
    hit_n = 0             #count hit
    false_alarm_n = 0     #count false alarm
    reject_n = 0          #count correct reject
    miss_n = 0            #count miss

    # display the letter sequence
    # show letter sequence: each letter show for 0.5s and break for 2.5s
    for i in range(len(n_sequence_temp)):
        letter_display.text = trial_list_temp[i][2]
        letter_display.draw()
        win.flip()
        core.wait(0.5)
        win.flip()
        core.wait(2.5)
        keys = kb.getKeys(['y'], waitRelease=False)
        if keys == []:
            trial_list_temp[i].append("NULL") # record the key pressed
            trial_list_temp[i].append(0) # record the response as 0/1
            trial_list_temp[i].append("NULL") # record the reaction time
            if trial_list_temp[1] == trial_list_temp[5]:
                trial_list_temp[i].append(1)
                correct_n = correct_n + 1
                reject_n = reject_n + 1
            else:
                trial_list_temp[i].append(0)
                false_alarm_n = false_alarm_n + 1
        else:
            key = keys[0]
            trial_list_temp[i].append("Y") # record the key pressed
            trial_list_temp[i].append(1)  # record the response as 0/1
            trial_list_temp[i].append(key.rt) # record the reaction time
            if trial_list_temp[1] == trial_list_temp[5]:
                trial_list_temp[i].append(1)
                correct_n = correct_n+1
                hit_n = hit_n + 1
            else:
                trial_list_temp[i].append(0)
                miss_n = miss_n + 1
    
    answer_list.append(answer_list_temp)
    n_sequence.append(n_sequence_temp)
    trial_list.append(trial_list_temp)
    trial_list.append(['correct rate', 'hit rate', 'false alarm rate', 'reject rate', 'miss rate'])
    trial_list.append([correct_n, hit_n, false_alarm_n, reject_n, miss_n])
 
# 3. export data
data = [['ID', 'Anser_List','Letter_Display','Block', 'Key_Pressed', 'Response', 'Reaction_Time','Correct']]
for sublist in trial_list:
    data.append(sublist)
    
df = pd.DataFrame(data)
#print(df) #test the data structure 

filename = f'sub-{ID:02d}.xlsx' # data filename for each sub.
filepath = '/Users/luoqi/Desktop/' #path of folder where you save data
df.to_excel(f'{filename}', index=False) #change it to your own directory
