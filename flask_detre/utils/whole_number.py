# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 14:31:21 2021

@author: Detre
"""

import pandas as pd
import re


def detre_wnumber(df):
    
    all_data = []
    correct_ = []
    incorrect = []
    
    df  = df.astype('str')
    
    df_clean = df.apply(lambda x: re.sub("[^0-9,\.]",'',x))
    
    for idx, v in enumerate(df_clean):
        
        try:
            value  = int(v) 
            correct_.append({"row":idx,"value":v,"detre":value})
        except:
            incorrect.append({"row":idx,"value":v,"detre":"Provide guidance"})
            
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data    


def wnumber_update_value(value,action,data_type):
    
    if action == "remove":
        return "remove"
    
    return None
    