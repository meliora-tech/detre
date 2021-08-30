# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:03:03 2021

@author: Detre
"""

from flask_detre.utils.utils import (excel_number_conversion,remove_entry,no_text_and_char,
                                     char_no_text,text_no_char,text_and_char)

import re

# Util function that handles when time `action` characters
# are present
def remove_hms_textd(value,action, data_type="date"):
    # Find all digits 
    digit_pattern = re.compile("[\d]+")
    digits_found  = digit_pattern.findall(value)
    
    
    # Find the present `date` direcives
    num_date_pattern  = re.compile('[yYmd]')
    #num_date_arr      = num_date_pattern.findall(action)
      
   
     # Find the `text[D]` action(s) index(indices)
    textd_pattern = re.compile('(text\\[D\\])')
    textd_idx     = [ m.start(0) for m  in textd_pattern.finditer(action)]
    
    
    # Find the number of `date` index(indices) 
    num_date_idx      = [ m.start(0) for m  in num_date_pattern.finditer(action)]    
    len_num_date      = len(num_date_idx)
    max_num_date_idx  = max(num_date_idx)
    
    
    # Find the last index for the `date` values to be used
    # in `digits_found` arr
    final_idx = 0
    for idx in textd_idx:
        if max_num_date_idx < idx:
            break
        
        final_idx+=1    
    
    
    # Get the date values
    if len_num_date > 1:
        date_values = digits_found[final_idx:final_idx + len_num_date]
    else:
         date_values = [digits_found[final_idx]]
    
    # Remove the hms in value
    for d in digits_found:
        if str(d) not in date_values:
            
            value = value.replace(str(d), '',1)
            
    # Remove `text[D]`
    action = action.replace('text[D]','')

    return date_update_value(value,action,data_type)    


def date_update_value(value,action,data_type):
        value = value.strip()
       
        holder = {}
        if action == 'Excel':  # Number of days since epoch
           new_value = excel_number_conversion(value)
           return new_value
       
        elif action == 'remove':  # entry must be removed
            new_value = remove_entry()
            return new_value
        
        
        #======================================================
        # Check if there is any text or special characters
        # Case 1: No special characters and text
        # Case 2: No Text but there is special characters
        # Case 3: No special characters but there is text
        # Case 4: Text and special characters are present
        #=====================================================
        
        # Check if there is any time related `action` characters
        # If there is, then replace them with text or text[D]
        time_char_pattern = re.compile('[HMSp]')
        time_char_found   = time_char_pattern.findall(action)
        
       
        if len(time_char_found) > 0:
            for char in time_char_found:
                if char == 'p':
                    action = action.replace(char,'text')
                else:
                    action = action.replace(char,'text[D]')
            
            return remove_hms_textd(value,action, data_type)   
        
        
        # simply use the given format if text or special characters are not present
        if action.find('*') == -1 and action.find('text') == -1:
            return no_text_and_char(value,action)
        
        elif action.find('*') != -1 and action.find('text') == -1:
            #===========================================================
            # Case 2: Special character(s) is(are) present but no text 
            #=============================================================
            
        
              
             return char_no_text(holder,value, action)

        
            #==================================================
            # Case 3: No special characters but there is text
            #===================================================
        elif action.find('*') == -1 and action.find('text') != -1:
           
            return text_no_char(value,action)
                
        #=======================================================        
        # Case 4: Text and special characters are present
        #=======================================================
        elif action.find('*') != -1 and action.find('text') != -1:            
           
            if action.find('b') == -1 and action.find('B') == -1: # Both are not present
                              
                new_value     = text_and_char(value, action)
                return new_value
            
                
            elif action.find('b') != -1 and action.find('B') == -1:  # Handle the case for 'Jan','Feb', etc
            
                new_value     = text_and_char(value, action)
                return new_value
                
            elif action.find('B') != -1 and action.find('b') == -1: # Handle the case for 'January','February', etc

                    new_value     = text_and_char(value, action)
                    return new_value
