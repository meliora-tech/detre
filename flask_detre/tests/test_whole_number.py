# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 16:32:18 2021

@author: Detre
"""

import pandas as pd
from flask_detre.utils.whole_number import (detre_wnumber,wnumber_update_value)


def test_whole():
    """
    Test when given a series of values classify them as correct or incorrect    
    """
    df = pd.Series(["1`000.12","500.12",50,'asdass'])
    ans = detre_wnumber(df)
    
    assert ans[0]["correct"][0]['detre'] == 50
    assert ans[1]["incorrect"][0]['value'] == '1000.12'
    assert ans[1]["incorrect"][2]['value'] == ''
    
    
def test_wnumber_update():
    """
    Test the update of a value given an `action`    
    """
    ans  =  wnumber_update_value("","remove","whole")
    
    assert ans == "remove"
    
def test_wnumber_multiple_updates():
    pass
