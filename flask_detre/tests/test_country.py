# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:28:08 2021

@author: Detre
"""


from flask_detre.utils.country import detre_country

import pandas as pd


def test_country():
    
    df = pd.Series(["SA","South Africa","England","Fin","Match"])
    
    values = detre_country(df)
    
    assert values[0]["correct"][0]['detre'] == "Saudi Arabia"
    assert values[0]["correct"][1]['detre'] == "South Africa"
    assert values[0]["correct"][2]['detre'] == "United Kingdom"
    assert values[0]["correct"][3]['detre'] == "Finland"
    assert values[1]["incorrect"][0]['detre'] == "Please provide guidance"
