# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 14:18:06 2021

@author: Detre
"""

from flask_detre.utils.datetime_ import (detre_datetime, datetime_update_value)

import pandas as pd



def test_datetime_():
    
    series    = pd.Series(["4:40 oct 13 atlantic","Oct 20/10 4:50PM","November 8/10...12 noon",
                           "Oct 21, 2010 3:00 pm","Jan 12, 2011","11:00 am","Nov. 16/10 11;50 a.m."])
    result    = detre_datetime(series)
    correct   = result[0]["correct"]
    incorrect = result[1]["incorrect"]
    
    assert len(correct) == 4
    assert len(incorrect) == 3
    

def test_datetime_upatde():
    
    new_value   = datetime_update_value("November 8/10...12 noon","Bd*y*Htext")
    new_value_2 = datetime_update_value("4:40 oct 13 atlantic","H*Mbdtext") 
    new_value_3 = datetime_update_value("Nov. 16/10 11;50 a.m.","b*d*yH*Mp")
    assert new_value == "2010-11-08 12:00:00"
    assert new_value_2 == "1900-10-13 04:40:00"
    assert new_value_3 == "2010-11-16 11:50:00"