# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:22:09 2021

@author: Detre
"""

import pandas as pf
import numpy as np



def detre_categorical(df,categories):
    all_data  = []
    correct_  = []
    incorrect = []

    for category in categories:
        cat = category.lower()
        
        
    
    
    pass

def convert_cagetorical(df):

    new_value = np.where(df['index'].str.contains('nasa',case=False),'NASA',"")


def convert_cat2num(df):
    # Convert categorical variable to numerical variable
    num_encode = {'col_1' : {'YES':1, 'NO':0},
                  'col_2'  : {'WON':1, 'LOSE':0, 'DRAW':0}}  
    df.replace(num_encode, inplace=True) 