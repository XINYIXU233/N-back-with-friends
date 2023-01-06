#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:47:10 2022

@author: luoqi
"""

import random

# function to generate an answer list, consisting with 0 & 1

def answer_list(n, item_number, correct_number):
    answer_list = n * [0] # first n items in answer list have to be 0, 1 can occur start from the n+1 item
    rest = correct_number * [1] + (item_number - correct_number - n) * [0] # rest of the items in the answer list
    random.shuffle(rest)
    answer_list.extend(rest)
    return answer_list

# function to generate the n-sequence, according to the answer list
# the basic idea of this function is that we create temp to save the last n letters, and the n+1 letter should be the rest letters
# other than the ones in temp.
def n_sequence(n,answer_list):

    letters = ["A", "B", "C", "D", "E", "F", "G", "H"] #letters record candidate letters you are choosing from
    sequence = [] # sequence record the n_sequence, which are the letters you are presenting
    temp = [] # temp save the last n letters, and for the n+1 letter, you are going to choose from letters orther than temp.
    
    
    # this loop first create first n letters, in which there should be only 0 answers and no repetitive letters
    for i in range(n):
        letter = random.choice(letters) # firstly randomly choose from one from the 8 letters
        sequence.append(letter) #append this letter to sequence
        temp.append(letter) # also record this letter to temp
        letters.remove(temp[-1]) # delete this letter from letters to make sure this letter will not be selected in next trial.
        
    
    # after generating first n letters, we will finalize the sequence here
    for i in range(n,len(answer_list)):
        
        # at the beginning of each trial, redefine letters as 8 candidate letters,
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"] 
        
        # remove temp from letters, to make sure the letters in temp will not be selected
        for j in range(len(temp)):
            letters.remove(temp[j]) 
        
        #randomly choose one from letters and append to sequence
        if answer_list[i] == 0:      
            letter = random.choice(letters) 
            sequence.append(letter)
        
        # this is a n-back trail, so we append the same letter as the n-back one. 
        if answer_list[i] == 1:        
            sequence.append(sequence[i-n])
        
        # since, we add new letter to the sequence, so we have to update the temp. remove the first letter from temp and add the last
        # letter in sequence to temp.
        temp.remove(temp[0])
        temp.append(sequence[i])
    
    return sequence


def trial_list(id, answer_list, n_sequence, n):
    trial_list = [] #create a temporary list to store the elements in pair
    for i in range(len(answer_list)):
        temp = [id, answer_list[i], n_sequence[i],n]
        trial_list.append(temp)

    return trial_list





