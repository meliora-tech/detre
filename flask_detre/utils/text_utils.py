# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 18:39:02 2021

@author: Detre
"""


import re
import unidecode


def get_fingerprints(df):
    
    """
        Function to get all fingerprints for a given pandas Series
        
        :param - pd.Series
        :return - dict
    """
    
    dict_ = {}
    for v in df:
        
        finger_print = fingerprint(v)
        
        if dict_.get(finger_print) == None:
            dict_[finger_print] = [v]
        else:
            
            old_arr = dict_[finger_print]
            old_arr.append(v)

    return dict_



def fingerprint(string):
    
    """
      Function used to produce a fingerprint for a string
      
      :params - string
      :return - string
    """
    # change all characters to their lowercase representation
    string = string.lower()
    # remove all punctuation and control characters
    string = re.sub("[^A-Za-z0-9 ]+", "", string)
    # normalize extended western characters to their ASCII representation
    string = unidecode.unidecode(string)
    # split the string into whitespace-separated tokens
    words = string.split()
    # sort the tokens and remove duplicates
    words = sorted(list(set(words)))
    # join the tokens back together
    return " ".join(words)