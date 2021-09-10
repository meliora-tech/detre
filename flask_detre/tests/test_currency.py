# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 15:09:21 2021

@author: Detre
"""

import pandas as pd


from flask_detre.utils.currency import detre_currency


def test_currency():
    
    new_value = detre_currency(pd.Series(["$120.22","R24,00"]))
    
    assert new_value[0]["correct"][0]['detre'] == float("120.22")
    assert new_value[1]["incorrect"][0]['value'] == "R24,00"