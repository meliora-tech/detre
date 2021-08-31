# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 14:27:48 2021

@author: Detre Team
"""



import pytest
from flask_detre.utils.utils import (excel_number_conversion, remove_entry, 
                         no_text_and_char, char_no_text, text_no_char,
                         text_and_char)

from flask_detre.utils.detre_update_values import detre_update_multiple_values


def test_remove_entry():
    """
    Test the remove entry `action`
    """
    new_value = remove_entry()
    assert new_value == 'remove'

def test_excel_number_conversion():
    """
    Test the convert to excel `action`
    """
    new_value  = excel_number_conversion('42795')
    
    assert new_value == '2017-03-01'
    
    
def test_no_text_and_char():
    """
    Test the no text and character `action`
    """
    new_value = no_text_and_char('0909','my')
    
    assert new_value == '2009-09-01'
    
def test_char_no_text():
    """
    Test the no text `action`
    """
    new_value = char_no_text({},'Nov.`02','b**y')

    assert new_value == '2002-11-01'    

def test_text_no_char():
    """
    Test the no character `action`
    """
    new_value  = text_no_char('Deposited in Bratislava in 2001','textY')
    
    assert new_value == '2001-01-01'
    
def test_text_and_char():
    
    """
    Test the text and character `action`
    """
    new_value = text_and_char('8/12/04 (scholarship)','d*m*y*text*')
    
    assert new_value == '2004-12-08'
    
    
def test_update_multiple_values():
    """
    Test the update for mulitple values
    """
    
    values = detre_update_multiple_values(['8/12/04 (scholarship)','Deposited in Bratislava in 2001'],"d*m*y*text*",
                                          "date")
    
    assert values[0] == '2004-12-08'
    assert values[1] == 'None'
    
    
    
    