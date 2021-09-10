# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:29:22 2021

@author: Detre
"""

import pandas as pd
import pycountry
import re


def detre_country(df):
    
    all_data = []
    correct_ = []
    incorrect = []    
    
    for idx, v in enumerate(df):
        
        v    = re.sub("[^A-Za-z ]","",str(v)).lower()
        
        if v == "" or v == " ":
            incorrect.append({"row":idx,"value":v,"detre":"Empty value"})
            continue
    
        try:
             ans    = pycountry.countries.search_fuzzy(v)
             value  = ans[0].name
             correct_.append({"row":idx,"value":v,"detre":value})
        except Exception as e:
            
            try:
                ans    = pycountry.countries.lookup(v)
                value  = ans.name
                correct_.append({"row":idx,"value":v,"detre":value})
            except Exception as e:
                incorrect.append({"row":idx,"value":v,"detre":"Please provide guidance"})
  
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data    