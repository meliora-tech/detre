# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 10:57:25 2021

@author: Detre
"""

from flask_detre.utils.phone_number import (phone_number, phone_update_value)
from flask_detre.utils.detre_update_values import detre_update_multiple_values
import requests
from flask import Flask

app = Flask(__name__)
app.secret_key = 'my-seCret_KEy'

url = "http://localhost:8100"


def test_decimal_phone_number():
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '27'
            
        rv  = c.get(url)      
        new_value = phone_number("0.608314773","27")
        assert "incorrect" == new_value[0]
    
def test_phone_number():
    
    """ Make sure that phone number is true given a country code"""
    new_value = phone_number("0608314773","27")
    
    assert new_value[1] == "27608314773"
    
    
def test_country_code():
    
    """ Test request for country codes """
    value   = requests.get(url+"/country_codes")
    
    assert value.status_code == 200
    
def test_phone_update():
    """ Test  phone number update based on text digits and `tel` of number string """
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '93'
           
        rv  = c.get(url)    
        value = phone_update_value("27731234567","text[D]text[D]tel","phone")
    
        assert  value == "93731234567" 
        
def test_phone_update_more_numbers_end():
    """ Test  phone number update based on text digits at the  `end` of number string """
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code']  = '93'
        
        
        rv = c.get(url)
        value = phone_update_value("073;421;8472222","ddd*ddd*ddddtext[D]text[D]text[D]","phone")
        
        assert value == "930734218472"
    
    
def test_phone_update_more_numbers_start():
    """ Test  phone number update based on text digits at the `start` of number string """
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '93'
            
        rv = c.get(url)
        value = phone_update_value("073;421;8472","text[D]dd*ddd*dddd","phone")
        
        assert value == "93734218472"
        
        
def test_phone_update_more_numbers_start_and_end():
    """ Test  phone number update based on text digits at the `start` and `end` of number string """
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '93'
        
        rv = c.get(url)
        
        value = phone_update_value("073;421;8472222","text[D]dd*ddd*ddddtext[D]text[D]text[D]","phone")
        
        assert value == "93734218472"
        
def test_phone_update_more_numbers_mid_adjacent():
    """ Test  phone number update based on text digits at the  `'middle` and adjacent each other in the number string """ 
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '93'
            
        rv     = c.get(url)
        value  = phone_update_value("073;42155;8472","ddd*dddtext[D]text[D]*dddd","phone")
        
        assert value == "930734218472"
        
def test_phone_update_more_numbers_mid_not_adjacent():
     """ Test  phone number update based on text digits at the  `'middle` and not adjacent each other in the number string """    
     with app.test_client() as c:
         with c.session_transaction() as sess:
             sess['country_code'] = '93'
        
         rv    = c.get(url)
         value = phone_update_value("073;4215;85472","ddd*ddtext[D]d*dtext[D]dd","phone") 
         
         assert value == "930734258472"
         
         
def test_phone_update_more_numbers_start_mid():
    """ Test  phone number update based on text digits at the `start` and `middle`  of number string """
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess["country_code"] = '93'
        
        rv    = c.get(url)
        value = phone_update_value("073;4215;85472","text[D]dd*ddtext[D]d*dtext[D]ddd","phone") 
        
        assert value == "93734258472"
        
def test_phone_update_more_numbers_mid_end():
     """ Test  phone number update based on text digits at the `middle` and `end` of number string """
     with app.test_client() as c:
         with c.session_transaction() as sess:
             sess['country_code'] = '93'
             
         rv     = c.get(url)
         value  = phone_update_value("073;4215;8547222","ddd*ddtext[D]d*dtext[D]dddtext[D]text[D]","phone")
        
         assert value == "930734258472"
         
         
def test_phone_update_more_numbers_start_mid_end():
    """ Test  phone number update based on text digits at the `start`, `'middle` and `end` of number string """
    
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '93'
        
        rv    = c.get(url)
        value = phone_update_value("073;4215;84722","text[D]dd*ddtext[D]d*ddddtext[D]","phone") 
        
        assert value == "93734258472"
        
        
def test_phone_number_multiple_updates():
    
    """
    Test for multiple value updates
    """
    
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['country_code'] = '27'
        
        rv    = c.get(url)
        value = detre_update_multiple_values(["11731234567","00734581234"],"text[D]text[D]tel","phone") 
        
        assert value[0] == "27731234567"
        assert value[1] == "27734581234"