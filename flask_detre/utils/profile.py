# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 20:40:24 2021

@author: Detre
"""


from flask_detre.utils.text_utils import fingerprint

import pandas as pd

def detre_profile(df,type_):
    
    """
    Get the data profile for the given series and `type`
    """
    ans = {}

    if type_ == "datetime" or type_ == "date" or type_ == "time":
        df = pd.to_datetime(df)
        
    if type_ == "date":
        df = pd.to_datetime(df,format="%Y-%m-%d" ).dt.date
    
    if type_ == "time":
        df  = pd.to_datetime(df,format="%H:%M:%S" ).dt.time
                
    if type_ == "decimal" or type_ == "whole" or type_ == "currency":
        df = pd.to_numeric(df)
        
        
    
    # Total number duplicates
    duplicates_total = df.duplicated().sum()
    
    ans["duplicates_total"] = duplicates_total
    
    # Total number of NA or Null
    # na_total = df.isna().sum() + df.isnull().sum() 
    
    # ans["na_total"] = na_total
    
    # Total number of  ' '
    # empty_total = df[df == ''].shape[0] + df[df == ' '].shape[0]
    
    if type_ == "whole" or type_=="decimal" or type_=="datetime" or \
        type_ == "date" or type_ == "time" :
            
        ans["min"]      = str(df.min())
        ans["max"]      = str(df.max())
        
        #ans["range"]    = df.max() - df.min()
        ans["n_unique"] = len(df.unique())
        freq_series     = df.value_counts()[df.value_counts() >= 2]
        
        if type_ == "whole" or type_ == "decimal":
            ans["freq"]     = [dict(freq_series)]
        else:
            ans["freq"]    = [ {str(k):v}  for k,v in dict(freq_series).items()]
    
    
    # ans["empty_total"] = empty_total
    
    if type_ == "text" or type_=="country" or type_ == "phone" or type_=="datetime":
        dict_ = {}
        
        for v in df:
            
            finger_print = fingerprint(str(v))
            
            if dict_.get(finger_print) == None:
                dict_[finger_print] = [str(v)]
            else:
                
                old_arr = dict_[finger_print]
                old_arr.append(str(v))
                
        # Join each fingerprint values by ','
        for key, item in dict_.items():
            dict_[key]  = ",".join(item)
            
        # Other statistics
        ans["min"] = "-"
        ans["max"] = "-"
        ans["n_unique"] = len(dict_.keys())
        
        ans["text_cluster"] = dict_ 
        
    return ans    



