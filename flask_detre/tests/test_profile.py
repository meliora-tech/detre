# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 19:15:09 2021

@author: Detre
"""

from flask_detre.utils.profile import detre_profile
from flask_detre.utils.time import detre_time
from flask_detre.utils.datetime_ import detre_datetime

import pandas as pd

def test_profile_phone():
   df   = pd.Series(["2706086412","270556422",""]) 
   data = detre_profile(df,"phone")
   
   assert data["duplicates_total"] == 0 

   
   
def test_profile_email():
   df   = pd.Series(["ntuthuko@ta.com","asd@as.com","ntuthuko@ta.com"]) 
   data = detre_profile(df,"text")
    
   assert len(data["text_cluster"]["ntuthukotacom"]) == 2  
   
   
def test_profile_time():
    series    = pd.Series(["23h00","23:00","23h55","23H00",'14;00 ',"asdasda sdasd"])
    result    = detre_time(series)
    correct   = result[0]["correct"]
    df        = pd.DataFrame(correct)
    profile   = detre_profile(df["detre"],"time")
    
    assert profile['duplicates_total'] == 2
    assert profile['n_unique']         == 3
    assert len(profile['freq'])        == 1
    

def test_profile_datetime():
    series    = pd.Series(["4:40 oct 13 atlantic","Oct 20/10 4:50PM","November 8/10...12 noon",
                           "Oct 21, 2010 3:00 pm","Jan 12, 2011","11:00 am","Nov. 16/10 11;50 a.m."])
    result    = detre_datetime(series)
    correct   = result[0]["correct"]
    df        = pd.DataFrame(correct)
    profile   = detre_profile(df['detre'],'datetime')
    
    assert profile['duplicates_total'] == 0
    assert profile['n_unique']         == 4
    assert len(profile['freq'])        == 0

         