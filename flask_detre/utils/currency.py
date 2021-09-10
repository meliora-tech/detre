# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:04:02 2021

@author: Detre
"""

from collections import Counter

import pandas as pd
import re

def detre_currency(df):
    
    all_data = []
    correct_ = []
    incorrect = []
    
    
    for idx,v in enumerate(df):
        try:
            v                 = str(v)
            
            # Check if the value is empty
            if v =="" or v ==" ":
                 incorrect.append({"row":idx,"value":v,"detre":"Empty value"})
                 
            # Check if text was matched
            matched_text = match_text(v, idx, incorrect)
            
            if matched_text:
                continue
            
            # Check if date, time or datetime matched
            matched_dt = match_date_or_time(v, idx, incorrect)
                
            if matched_dt:
                continue
            
            non_digit_pattern = re.compile("[\D]")
            
            non_digit_found   = non_digit_pattern.findall(v)
            
            value             = v
            for non_digit in non_digit_found:
                if non_digit not in [",","."]:    
                    value = value.replace(non_digit,'')
            
            comma_period = [ nd for nd in non_digit_found if nd == "." or nd == "," ]
            
            
            if "." in comma_period and "," in comma_period:
                value              = match_currency_char(value,comma_period,',')
                new_comma_period   = non_digit_pattern.findall(value)
                value              = match_currency_char(value,new_comma_period,'.')
                
                correct_.append({"row":idx,"value":v,"detre":value})
            elif "." not in comma_period and "," in comma_period:
                 value = match_currency_char(value,comma_period,",")
                         
                 correct_.append({"row":idx,"value":v,"detre":value})
            elif "." in comma_period and "," not in comma_period:
                
                value = match_currency_char(value,comma_period,'.')
                
                correct_.append({"row":idx,"value":v,"detre":value})
            elif "." not in comma_period and "," not in comma_period:
                correct_.append({"row":idx,"value":v,"detre":value})
        
        except:
            incorrect.append({"row":idx,"value":v,"detre":"Edge Case"})
    
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})            
      
    return all_data



def match_text(value, idx, incorrect):
    """
    Find if there is text in the provided value. If there is then it must be captured as incorrect.
    """
    text_found    = re.findall("[A-Za-z]+",value)
    numbers_found = re.findall(r"[0-9]+", value)
    
    if len(text_found) > 0 and len(numbers_found) > 0:
        number_currency = re.findall(r"[A-Za-z][A-Za-z]?[\\. ]?\d{1,}[` ,\\.]?\d{1,}\d{1,}[` ,\\.]?\d{1,}",value)
        
        if len(number_currency) > 0:
            return False
        
        incorrect.append({"row":idx,"value":value,"detre":"Text and numbers found"})
        return True
    elif len(text_found) > 0 and len(numbers_found) == 0:
        incorrect.append({"row":idx,"value":value,"detre":"Only text found"})
        return True
    elif len(text_found) == 0 and len(numbers_found) > 0:
        return False


def match_date_or_time(value, idx, incorrect):
    """
    Find if the provided value is similar to a date, time or datetime structure
    """
    
    dt_chars_found = re.findall(r"[:/-]", value) 
    
    if len(dt_chars_found) > 0:
        incorrect.append({"row":idx,"value":value,"detre":"Date/Time related characters found"})
        return True


def match_currency_char(value,comma_period,char):
    """
    Match the provided char and replace it with either '' or "." based on its position
    in the number string
    """
    if char == ".":
        rchar = r"\\."
    else:
        rchar = r","
        
    n_chars = Counter(comma_period)[char]
    if n_chars == 1 and char == ",":
        if len(value.split(",")[1]) >= 3:
            return float(value.replace(",",""))
        
    for idx, match in enumerate(re.finditer(rchar,value)):
        if (n_chars-1) == idx:
            value = value.replace(char,".")
        else:
            value = value.replace(char,'',match.start())

    return float(value)

def convert_currency(df):
    
    
    numbers = df.fillna('').astype('str').str.replace(r'[^\d\.]', '').astype('float')
    
    return numbers


if __name__ == "__main__":
    value = "$152,000.522.25"
    print(match_currency_char(value,[",",".","."],","))
    value = match_currency_char(value,[",",",","."],",")
    print(match_currency_char(value,"."))