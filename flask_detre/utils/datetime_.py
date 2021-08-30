# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 14:07:10 2021

@author: Detre
"""

import pandas as pd

from flask_detre.utils.time import time_update_value
from flask_detre.utils.date import date_update_value

# Main function call from the API
def detre_datetime(df):
    all_data = []
    correct_ = []
    incorrect = []
    
    for idx, dt_value in enumerate(df):
        dt_value = str(dt_value).strip()
        try:
            result = pd.to_datetime(dt_value).strftime("%Y-%m-%d %H:%M:%S")
            correct_.append({"row":idx,"value":dt_value,"detre":result})
        except:
            incorrect.append({"row":idx,"value":dt_value,"detre":"Please provide guidance"})
            
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data 

# Main function for upates
def datetime_update_value(value, action):
    
    if action == "remove":
        return "remove"
    
    date_ = date_update_value(value,action,"date")
    time_ = time_update_value(value,action,"time")
    
    if date_ and time_:
        return date_+" " + time_
    else:
        return None