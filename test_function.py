#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:00:05 2022

@author: luoqi
"""
import nsequence_generator

for i in range(1000):
    a = nsequence_generator.answer_list(3, 14, 2)
    b = nsequence_generator.n_sequence(3,a)
    print(a)
    print(b)