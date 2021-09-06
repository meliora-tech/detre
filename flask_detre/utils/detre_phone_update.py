# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 10:14:17 2021

@author: Detre
"""

def text_phone_update(value,action,data_type):
    
    
    if action.strip().lower() == "none" or None:
        return 'None'
    elif action.strip().lower() == "reomve":
        return "remove"
    
    return "asdsa" 