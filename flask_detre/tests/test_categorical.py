# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 17:14:25 2021

@author: Detre
"""



import pytest
import pandas as pd

from flask_detre.utils.categorical import detre_categorical


def test_categorical():
    df  =  pd.Series(["m","Male","f"])
    categories  = ["Male","Female"]
    ans         = detre_categorical(df,categories)
    
    assert ans == None
    
    
    