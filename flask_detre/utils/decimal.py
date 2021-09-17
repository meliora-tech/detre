# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 14:54:50 2021

@author: Detre
"""


import pandas as pd
import re
import html

def detre_decimal(df):
    
    all_data = []
    correct_ = []
    incorrect = []
    
    df  = df.astype('str')
    
    df_clean = df.apply(lambda x: re.sub("[^0-9,\.]",'',x))
    
    for idx, v in enumerate(df_clean):
        v = html.escape(str(v))
        try:
            value  = float(v) 
            correct_.append({"row":idx,"value":v,"detre":value})
        except:
            incorrect.append({"row":idx,"value":v,"detre":"Provide guidance"})
            
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data    


def decimal_update_value(value,action,data_type):
    
    if action == "remove":
        return "remove"
    
    return None