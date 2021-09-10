# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 20:40:24 2021

@author: Detre
"""


from flask_detre.utils.text_utils import fingerprint

import pandas as pd
import numpy as np


def detre_profile(df,df_incorrect,type_):
    
    """
    Get the data profile for the given series and `type`. Also get the profile for the `incorrect` dataframe 
    """
    ans = {}
    
    if type_ == "currency" or type_ == "decimal" or type_ == "whole" :
        df                    = pd.to_numeric(df)
        #ans["correct_values"] = df.to_list()
        ans["total_correct"]  = len(df)
        mean            = df.mean()
        std             = df.std()
        ans["min"]      = str(df.min())
        ans["max"]      = str(df.max())
        ans["std"]      = std
        ans["mean"]     = mean
        
        
        ans["n_unique"] = len(df.unique())
        freq_series     = df.value_counts()[df.value_counts() >= 2]
        
        duplicates_total = df.duplicated().sum()
        
        ans["duplicates_total"] = duplicates_total
        
        if type_ == "whole" or type_ == "decimal":
            ans["freq"]     = [dict(freq_series)]
        else:
            ans["freq"]    = [ {str(k):v}  for k,v in dict(freq_series).items()]         
            
        
        upper_outliers           = df[list(np.where( df > mean+std )[0])].values
        lower_outliers           = df[list(np.where( df < mean-std )[0])].values
        ans["n_upper_outliers"]  = len(upper_outliers)
        ans["n_lower_outliers"]  = len(lower_outliers)
        
        ans["upper_outliers"]    = list(upper_outliers)
        ans["lower_outliers"]    = list(lower_outliers)
        
        
        if len(df_incorrect) != 0:
            detre_outcome  = df_incorrect["detre"].value_counts()
            ans["incorrect_pattern"] = detre_outcome.to_dict()
            ans["total_incorrect"] = df_incorrect.shape[0]
            
        return ans




    if type_ == "datetime" or type_ == "date" or type_ == "time":
        if type_ == "date":
           
            df = pd.to_datetime(df, format='%Y-%m-%d').dt.date
            

            diff_sorted_counts = (df.sort_values() - df.sort_values().shift(periods=1)).value_counts()
            diff_unsorted_counts = (df - df.shift(periods=1)).value_counts()
            
            ans["diff_sorted_freq"] = [ {str(k).replace(' 00:00:00',''):v}  for k,v in dict(diff_sorted_counts).items()]  
            ans["diff_unsorted_freq"] = [ {str(k).replace(' 00:00:00','').replace(' +00:00:00','') :v}  for k,v in dict(diff_unsorted_counts).items()]  
            

            ans["dow_freq"]       = [dict(pd.to_datetime(df).dt.day_name().value_counts())]
            ans["monthname_freq"] = [dict(pd.to_datetime(df).dt.month_name().value_counts())]
            ans["year_freq"]      = [dict(pd.to_datetime(df).dt.year.value_counts())]
            ans["day_freq"]       = [dict(pd.to_datetime(df).dt.day.value_counts())]
            ans["month_freq"]     = [dict(pd.to_datetime(df).dt.month.value_counts())]
            
        elif type_ == "time":
            df = pd.to_datetime(df)
            
            diff_sorted_counts = (df.sort_values() - df.sort_values().shift(periods=1)).dt.seconds.value_counts()
            diff_unsorted_counts = (df - df.shift(periods=1)).dt.seconds.value_counts()
            

            ans["diff_sorted_freq"]   = [dict(diff_sorted_counts)]
            ans["diff_unsorted_freq"] = [dict(diff_unsorted_counts)]
            ans["sec_freq"]    = [dict(pd.to_datetime(df, format='%H:%M:%S').dt.second.value_counts())]
            ans["minute_freq"] = [dict(pd.to_datetime(df, format='%H:%M:%S').dt.minute.value_counts())]
            ans["hour_freq"]   = [dict(pd.to_datetime(df, format='%H:%M:%S').dt.hour.value_counts())]


            
        else:
            df = pd.to_datetime(df)
            
            diff_sorted_counts = (df.sort_values() - df.sort_values().shift(periods=1)).value_counts()
            diff_unsorted_counts = (df - df.shift(periods=1)).value_counts()
            
            ans["diff_sorted_freq"]   = [ {str(k)   :v}  for k,v in dict(diff_sorted_counts).items()]  
            ans["diff_unsorted_freq"] = [ {str(k) :v}  for k,v in dict(diff_unsorted_counts).items()]  
                        
            ans["dow_freq"]       = [dict(pd.to_datetime(df).dt.day_name().value_counts())]
            ans["monthname_freq"] = [dict(pd.to_datetime(df).dt.month_name().value_counts())]
            ans["year_freq"]      = [dict(pd.to_datetime(df).dt.year.value_counts())]
            ans["day_freq"]       = [dict(pd.to_datetime(df).dt.day.value_counts())]
            ans["month_freq"]     = [dict(pd.to_datetime(df).dt.month.value_counts())]

            ans["sec_freq"]    = [dict(pd.to_datetime(df, format='%H:%M:%S').dt.second.value_counts())]
            ans["minute_freq"] = [dict(pd.to_datetime(df, format='%H:%M:%S').dt.minute.value_counts())]
            ans["hour_freq"]   = [dict(pd.to_datetime(df, format='%H:%M:%S').dt.hour.value_counts())]
            
            
        duplicates_total = df.duplicated().sum()
        
        ans["duplicates_total"] = duplicates_total   
        ans["total_correct"]  = len(df)
        ans["min"]            = str(df.min())
        ans["max"]            = str(df.max())
       
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
            
        ans["n_unique"] = len(dict_.keys())
        
        ans["text_cluster"] = dict_  
        
        
        
        
        
        
        return ans        
            
        
        
    if type_ == "date":
        df = pd.to_datetime(df,format="%Y-%m-%d" ).dt.date
    
    if type_ == "time":
        df  = pd.to_datetime(df,format="%H:%M:%S" ).dt.time
                
    if type_ == "decimal" or type_ == "whole" or type_ == "currency":
        df = pd.to_numeric(df)
        
        
    

    
    # Total number of NA or Null
    # na_total = df.isna().sum() + df.isnull().sum() 
    
    # ans["na_total"] = na_total
    
    # Total number of  ' '
    # empty_total = df[df == ''].shape[0] + df[df == ' '].shape[0]
    
    if type_ == "whole" or type_=="decimal" or type_=="datetime" or \
        type_ == "date" or type_ == "time" or type_ == "currency":
            
        ans["min"]      = str(df.min())
        ans["max"]      = str(df.max())
        
        #ans["range"]    = df.max() - df.min()
        ans["n_unique"] = len(df.unique())
        freq_series     = df.value_counts()[df.value_counts() >= 2]
        
            # Total number duplicates
        duplicates_total = df.duplicated().sum()
        
        ans["duplicates_total"] = duplicates_total
        
        if type_ == "whole" or type_ == "decimal":
            ans["freq"]     = [dict(freq_series)]
        else:
            ans["freq"]    = [ {str(k):v}  for k,v in dict(freq_series).items()]
    
    
    # ans["empty_total"] = empty_total
    
    if type_ == "text" or type_=="country" or type_ == "phone" or type_=="datetime" or type_=="date":
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



