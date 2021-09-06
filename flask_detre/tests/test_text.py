# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 18:29:25 2021

@author: Detre
"""


from flask_detre.utils.text import detre_text
from flask_detre.utils.detre_text_update import text_email_update, text_url_update
import pandas as pd



def test_text_remove():
    
   df     = pd.Series(["asd ad ntuthuko@asd.com da asdad www.loop.com www.lty.com - a1 $ 3.,,,"])
   values = detre_text(df,["remove","remove","remove"],["url","email","punct"])
   
   assert values[0]['correct'][0]['detre'] == 'asd ad  da asdad    a1 $ 3'
   
   
def test_text_extract_url():
    
    df      = pd.Series(["asd ad ntuthuko@asd.com da asdad www.loop.com www.lty.com - a1 $ 3.,,,"])
    values  = detre_text(df,["extract"],["url"])
    
    assert values[0]['correct'][0]['detre'] == 'www.loop.com,www.lty.com'
    
    
def test_text_extract_email():
    df      = pd.Series(["asd ad ntuthuko@asd.com da asdad www.loop.com www.lty.com - a1 $ 3.,,,"])
    values  = detre_text(df,["extract"],["email"])
    
    assert values[0]['correct'][0]['detre'] == 'ntuthuko@asd.com'    
    
    
def test_text_update_email():
    new_value_1 = text_email_update("asdsa +245555","None","text-email")

    assert new_value_1 == "remove"
    
    
def test_text_extract_url_update():
    
    new_value  = text_url_update("jkbk ln asd adas.com asdasd","domain.tld","text-url")
    
    assert new_value[0] == "adas.com"