# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 14:52:46 2021

@author: Detre
"""



import pandas as pd
from flask_detre.utils.decimal import (detre_decimal,decimal_update_value)



def test_decimal():
    
    df = pd.Series(["1`000.12","500.12",50,'asdass'])
    ans = detre_decimal(df)

    assert ans[0]["correct"][0]["detre"] == 1000.12
    assert ans[0]["correct"][1]["detre"] == 500.12
    assert ans[1]["incorrect"][0]["value"] == ''

def test_decimal_update():
    
    ans =  decimal_update_value("","remove","decimal")
    
    assert ans == "remove"
    
    