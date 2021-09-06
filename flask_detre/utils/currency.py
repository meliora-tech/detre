# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:04:02 2021

@author: Detre
"""

import pandas as pd
import re

def detre_currency(df):
    
    all_data = []
    correct_ = []
    incorrect = []
    
    
    for idx,v in enumerate(df):
        v                 = str(v)
        non_digit_pattern = re.compile("[\D]")
        
        non_digit_found   = non_digit_pattern.findall(v)
        
        value             = v
        for non_digit in non_digit_found:
            if non_digit not in [",","."]:    
                value = value.replace(non_digit,'')
            
        correct_.append({"row":idx,"value":v,"detre":value})

    
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})            
    print(all_data)    
    return all_data

def convert_currency(df):
    
    
    numbers = df.fillna('').astype('str').str.replace(r'[^\d\.]', '').astype('float')
    
    return numbers