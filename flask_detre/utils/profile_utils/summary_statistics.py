# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 10:09:21 2021

@author: Detre
"""



def summary(df_correct, df_issues, type_:str):
      """
      Produce the summary statistics for the `correct` and `issues` values for the given 
      series.  The summary statistics will be produced based on the provided data type.
      """    
      
      
      min_  = str(df_correct.min())
      max_  = str(df_correct.max())
      
      
      n_unique        = len(df_correct.unique())
      freq_series     = df_correct.value_counts()[df_correct.value_counts() >= 2]
      
      
    
    

