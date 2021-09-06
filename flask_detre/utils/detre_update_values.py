# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 14:40:32 2021

@author: Detre
"""

from flask_detre.utils.utils import (excel_number_conversion,remove_entry,no_text_and_char,
                                     char_no_text,text_no_char,text_and_char)

from flask_detre.utils.phone_number import phone_update_value
from flask_detre.utils.time import time_update_value
from flask_detre.utils.datetime_ import datetime_update_value
from flask_detre.utils.detre_text_update import (text_email_update, text_url_update)
from flask_detre.utils.whole_number import wnumber_update_value
from flask_detre.utils.decimal import decimal_update_value


def date_update_value(value,action,data_type):
        """
        Function to update the `date` value given by action
        """
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


#=======================================================        
# Update the relevant value based on the user `action` and datatype
#=======================================================

def detre_update_value(value,action,data_type):
    
    """
    Update the given value based on the action
    """
    print(action)
    print(data_type)
    if data_type == "date":
        return date_update_value(value,action,data_type)
        
    elif data_type == "phone" or data_type == "text-phone" :
        return phone_update_value(value,action,data_type)
    elif data_type == "time":
        return time_update_value(value,action,data_type)
    elif data_type == "text-email" or data_type == "email" :
        
        return text_email_update(value,action,data_type)
    
    elif data_type == "text-url":
        return text_url_update(value, action, data_type)
    elif data_type == "whole":
         return wnumber_update_value(value,action,data_type)
    elif data_type == "decimal":
         return decimal_update_value(value,action,data_type)
    elif data_type == "datetime":
         return datetime_update_value(value,action)

     
def detre_update_multiple_values(values:list,action:str,data_type:str):
    
    """
    Update all values based on the given `action`
    """
    print(action)
    print(data_type)
    results = []
    if data_type == "datetime":
        for value in values:
            try:
                result = datetime_update_value(value,action)
                results.append(result)
            except:
                results.append("None")
    
    elif data_type == "phone" or data_type == "text-phone" :
        
        for value in values:
            
            try:
                result = phone_update_value(value,action,"phone")
                
                results.append(result)
            except Exception as e:
                
                results.append("None")        

    elif data_type == "date":
        for value in values:
            
            try:
                result = date_update_value(value,action,"date")
                
                results.append(result)
            except Exception as e:
                
                results.append("None")        

    elif data_type == "time":
        for value in values:
            
            try:
                result = time_update_value(value,action,"time")
                
                results.append(result)
            except Exception as e:
                
                results.append("None")          

    elif data_type == "whole":
        for value in values:
            
            try:
                result = wnumber_update_value(value,action,"whole")
                
                results.append(result)
            except Exception as e:
                
                results.append("None")            
    
    elif data_type == "decimal":
        for value in values:
            
            try:
                result = decimal_update_value(value,action,"decimal")
                
                results.append(result)
            except Exception as e:
                
                results.append("None")       
                
    elif data_type == "text-phone":
        pass

    no_none = [ 'none' for n in results if n == 'None' or n == None]
    if len(no_none) != len(results): 
        return results
    else:
        return None