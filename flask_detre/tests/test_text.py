# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 18:29:25 2021

@author: Detre
"""


from flask_detre.utils.text import detre_text
from flask_detre.utils.detre_text_update import text_email_update, text_url_update
from flask_detre.utils.phone_number import phone_update_value
import pandas as pd



def test_text_remove():
   """
   Test when remove placed for given text 
   """     
   df     = pd.Series(["asd ad ntuthuko@asd.com da asdad www.loop.com www.lty.com - a1 $ 3.,,,"])
   values = detre_text(df,["remove","remove","remove"],["url","email","punct"])
   
   assert values[0]['correct'][0]['detre'] == 'asd ad  da asdad    a1 $ 3'
   
   
def test_text_extract_url():
    """
    Test when url is extracted from text 
    """     
    
    df      = pd.Series(["asd ad ntuthuko@asd.com da asdad www.loop.com www.lty.com - a1 $ 3.,,,",
                         "My name is claim...https://t.co/SZlazvFzYx", '<script src="//www.google.com/somejsfile.js">',
                         'ftp://window.google', 'http://window.google', 'window.google', 'Link:https://www.google.com',
                         'PAYMENT EUR 1,420.00.zip', 'Visit us @www.example.com', 'Visit our website:www.example.com',
                         'Visit our website-www.example.com', 'Visit our website*www.example.com', 'Visit our website+www.example.com',
                         'Visit our website...www.example.com', "Nonsense URL = '.example.com'"])
    values  = detre_text(df,["extract"],["url"])
    
    assert values[0]['correct'][0]['detre'] == 'www.loop.com,www.lty.com,www.loop.com,www.lty.com'
    
    
def test_text_extract_email():
    df      = pd.Series(["asd ad ntuthuko@asd.com da asdad www.loop.com www.lty.com - a1 $ 3.,,,"])
    values  = detre_text(df,["extract"],["email"])
    
    assert values[0]['correct'][0]['detre'] == 'ntuthuko@asd.com'    
    

def test_text_extract_phone_number():
    """
    Test when phone number is extracted from text 
    """     
    
    df = pd.Series(["My name is claim...0734215042","278965620 <script src='//www.google.com/somejsfile.js'>",
                    '<p><strong>Kuala Lumpur</strong><strong>:</strong> +60 (0)3 2723 7900</p><p><strong>Mutiara Damansara:</strong> +60 (0)3 2723 7900</p><p><strong>Penang:</strong> + 60 (0)4 255 9000</p>        <h2>Where we are </h2>        <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8686        </p></div><div class="sys_two">    <h3 class="parentSchool">General enquiries</h3><p style="FONT-SIZE: 11px">     <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8000+ 60 (7) 268-6200 <br />Fax:<br /> +60 (7) 228-6202<br /> Phone:</strong><strong style="color: #f00">+601-4228-8055</strong>',
                    'df.info +1 (415)-555-1212"',"PAYMENT EUR 1,420.00.zip"])
    
    values = detre_text(df,["extract"],["phone"])
    
    assert values[1]['incorrect'][0]['row'] == 4
    assert values[0]['correct'][0]['detre'] == '0734215042'
    assert values[0]['correct'][3]['detre'] == '+1 (415)-555-1212'


def test_text_date_extract():
    """
    Test when date is extracted from text 
    """    
    
    df      = pd.Series(["2021-12-13 asd asd ads","zero (eg: 03/12/2008","Single digit months can start with a leading zero (eg: 03/12/2008)",
                         "CANNOT include February 30 or February 31 (eg: 2/31/2008)"])
    values  = detre_text(df,["extract"],["date"],[0,1,2,3,4])
    
    assert  values[0]['correct'][0]['detre']   == '2021-12-13'
    assert  values[0]['correct'][1]['detre']   == '2008-03-12'
    assert  values[1]['incorrect'][0]['detre'] == 'No date found.'



def test_text_update_email():
    """
    Test when email is updated 
    """
    new_value_1 = text_email_update("asdsa +245555","None","text-email")

    assert new_value_1 == "remove"
    
    
def test_text_extract_url_update():
    """
    Test when url  is updated 
    """
    new_value  = text_url_update("jkbk ln asd adas.com asdasd","domain.tld","text-url")
    
    assert new_value[0] == "adas.com"
    
    
    

def test_text_extract_phone_update():
    """
    Test when phone number is updated 
    """
    new_value = phone_update_value('df.info +1 (415)-555-1212"','text*+d*ddd*ddd*dddd','text-phone')
    
    assert new_value == ". +1 (415)-555-1212"



    
    
    
    