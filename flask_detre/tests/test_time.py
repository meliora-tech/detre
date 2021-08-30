# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:09:25 2021

@author: Detre
"""

from flask_detre.utils.time import (convert_to_time, detre_time, time_update_value)
import pandas as pd

def test_time():
    time_1 = convert_to_time('23h00','%Hh%M')
    time_2 = convert_to_time('23:00',None)
    
    assert time_2 == "23:00:00"
    assert time_1 == "23:00:00"
    

def test_time_return():

    series    = pd.Series(["23h00","23:00","23h55","23H00",'14;00 ',"asdasda sdasd"])
    result    = detre_time(series)
    correct   = len(result[0]["correct"])
    incorrect = len(result[1]["incorrect"])
    
    assert correct == 5
    assert incorrect == 1
    

def test_time_update_value():
    new_value_1   = time_update_value("1500 pm","HMp","time")
    new_value_2   = time_update_value("Dec 1015am","textHMp","time")
    new_value_3   = time_update_value("Dec 10:15am","textH*Mp","time")
    new_value_4   = time_update_value("10;24am","H*Mp","time")
    new_value_5   = time_update_value("Dec 12 10:24am","texttext[D]H*Mp","time")
    new_value_6   = time_update_value("Dec 12, 2021 10:24am","texttext[D]*text[D]H*Mp","time")
    new_value_7   = time_update_value("Dec 12, 10:24am 2021","texttext[D]*H*Mptext[D]","time")
    new_value_8   = time_update_value("Dec 1024am 2021","textHMptext[D]","time")
    new_value_9   = time_update_value("Dec 16, 2010","remove","time")
    new_value_10  = time_update_value("November 8/10..10: am","texttext[D]*text[D]**H*p","time")
    
    assert  new_value_1 == "15:00:00"
    assert  new_value_2 == "10:15:00"
    assert  new_value_3 == "10:15:00"
    assert  new_value_4 == "10:24:00"
    assert  new_value_5 == "10:24:00"
    assert  new_value_6 == "10:24:00"
    assert  new_value_7 == "10:24:00"
    assert  new_value_8 == "10:24:00"
    assert  new_value_9 == 'remove' 
    assert  new_value_10 == "10:00:00"
     
    