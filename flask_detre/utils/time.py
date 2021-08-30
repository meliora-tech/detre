# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:12:42 2021

@author: Detre
"""

import pandas as pd
import re

# Convert the given string in time to H:M:S
def convert_to_time(time_str,format_):
    
    if format_ is not None:
        time = pd.to_datetime(time_str,format=format_).time().strftime("%H:%M:%S")
    else:
        time_int = time_str
        time = pd.to_datetime(time_int).time().strftime("%H:%M:%S")
    return time
    

# Convert (if possible) when AM/PM have been detected
def am_pm_detection(time_found,idx, time_value ,correct_, incorrect):
    value_arr = time_found[0][0].split(':')
    
    if len(value_arr) == 2:
        
        result = pd.to_datetime(time_value,format="%H:%M").time().strftime("%H:%M:%S")
        correct_.append({"row":idx,"value":time_value,"detre":result})
    elif len(value_arr) == 3 and time_found[0][0].find('.') == -1:
        result = pd.to_datetime(time_value,format="%H:%M:%S").time().strftime("%H:%M:%S")
        correct_.append({"row":idx,"value":time_value,"detre":result})                        
    elif len(value_arr) == 3 and time_found[0][0].find('.') != -1:
        result = pd.to_datetime(time_value,format="%H:%M:%S.%f").time().strftime("%H:%M:%S.%f")
        correct_.append({"row":idx,"value":time_value,"detre":result})
    else:
        incorrect.append({"row":idx,"value":time_value,"new_value":"","detre":'Found too many numbers to convert. Provide guidance'})
                        


# Main function used in the api
def detre_time(df):
    
    
    all_data = []
    correct_ = []
    incorrect = []
    
    for idx, time_value in enumerate(df):
        time_value = time_value.strip()
        try:
            result = convert_to_time(time_value, format_=None)
            correct_.append({"row":idx,"value":time_value,"detre":result})
        except Exception as e:
            
            # Check if time_value is int or float
            if isinstance(time_value, int) or  isinstance(time_value, float):
                result = convert_to_time(time_value, format_=None)
                correct_.append({"row":idx,"value":time_value,"detre":result})                
                
            
            # Check if time_value has h:m(:s:ms) format
            number_pattern = re.compile("(\d+:\d+(:\d+)?(\.\d+)?)")
            time_found = number_pattern.findall(time_value)
            
            if len(time_found) != 0:
                
                # Find if it has AM/PM 
                if time_value.lower().find("pm") != -1 or time_value.lower().find("p.m.") != -1 :
                    
                    value_arr = time_found[0][0].split(':')
                    
                    if len(value_arr) == 2:
                        
                        result = pd.to_datetime(time_value,format="%H:%M").time().strftime("%H:%M:%S")
                        correct_.append({"row":idx,"value":time_value,"detre":result})
                    elif len(value_arr) == 3 and time_found[0][0].find('.') == -1:
                        result = pd.to_datetime(time_value,format="%H:%M:%S").time().strftime("%H:%M:%S")
                        correct_.append({"row":idx,"value":time_value,"detre":result})                        
                    elif len(value_arr) == 3 and time_found[0][0].find('.') != -1:
                        result = pd.to_datetime(time_value,format="%H:%M:%S.%f").time().strftime("%H:%M:%S.%f")
                        correct_.append({"row":idx,"value":time_value,"detre":result})
                    else:
                        incorrect.append({"row":idx,"value":time_value,"new_value":"","detre":'Found too many numbers to convert. Provide guidance'})
                    
                elif time_value.lower().find("am") != -1 or time_value.lower().find("a.m.") != -1:
                         am_pm_detection(time_found,idx, time_value ,correct_, incorrect)
                         
            
            else:
                # Check if it has a single non-digit value (e.g h)
                nondigit_pattern = re.compile("[\D]+")
                non_digit_arr    = nondigit_pattern.findall(time_value)
                
                                # Check if there is a digit
                no_digit_pattern = re.compile("[\d]+")
                no_digit_arr     = no_digit_pattern.findall(time_value)
                
                if len(non_digit_arr) == 1:
                    if len(non_digit_arr[0].strip()) == 1:
                        format_ = "%H"+non_digit_arr[0]+"%M"
                        result = pd.to_datetime(time_value,format=format_).time().strftime("%H:%M:%S")
                        correct_.append({"row":idx,"value":time_value,"detre":result})                    
                    else:
                        incorrect.append({"row":idx,"value":time_value,"new_value":"","detre":'Please provide guidance'})    

                
                elif len(no_digit_arr) == 0:
                    incorrect.append({"row":idx,"value":time_value,"new_value":"","detre":'No digit was found. Suggest to remove'})
                
                else:
                    incorrect.append({"row":idx,"value":time_value,"new_value":"","detre":'Please provide guidance'})    
            
            
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data        




# Util function used in time_update_value
def create_time(value,action):
    punct_pattern = re.compile("[\W]+")
    found_punct   = punct_pattern.findall(value)
    
    # Replace each punct with ''
    if len(found_punct) > 0: 
        for punct in found_punct:
            value  = value.replace(punct,'')
        
    # Add the % to each provided directive
    format_ = ''
    for char in action:
        format_+="%"+char
    
    try:    
        new_value = convert_to_time(value,format_)
        
        return new_value
    except Exception as e:
        
        return None        
 

# Util function used in time_update_value
# Remove the `text` action 

def remove_text(value,action):
    letter_pattern = re.compile("[A-Za-z]+")
    letters_found  = letter_pattern.findall(value)
    
    for letters in letters_found:
        letters = letters.strip()
        if letters.lower() == "am" or letters.lower() == "pm" or letters.lower() == "p.m" or letters.lower() == "a.m":
            continue
        else:
            value = value.replace(letters,'')
            
    value = value.strip()
    action = action.replace("text",'').strip()    
    
    return value, action


# Util used to get the time when
# `text[D]` is present
def textd_to_time(value : str,action: str,char=None):
    # Find all digits 
    digit_pattern = re.compile("[\d]+")
    digits_found  = digit_pattern.findall(value)
    
    
    # Find the H(hour), M(minute) and S(seconds) direcives
    time_pattern  = re.compile('[HMS]')
    time_arr      = time_pattern.findall(action)
    
   
    # Find the `text[D]` action(s) index(indices)
    textd_pattern = re.compile('(text\\[D\\])')
    textd_idx     = [ m.start(0) for m  in textd_pattern.finditer(action)]
    
    # Find the H(hour) index 
    hour_pattern  = re.compile('[H]+')
    hour_idx      = [ m.start(0) for m  in hour_pattern.finditer(action)][0]
    
    
    # Find the start index for the time values to be used
    # in `digits_found` arr
    final_idx = 0
    for idx in textd_idx:
        if hour_idx < idx:
            break
        
        final_idx+=1
    
    
    # Check if there is a locale (i.e. am or pm)
    local_pattern = re.compile("[p]")
    local_found   = local_pattern.findall(action)
    
    # Get the time values from the digits found
    if char is not None:
        time_values        = digits_found[final_idx:final_idx + len(time_arr)]
    else:
        if len(time_arr) == 1:
            time_values        = digits_found[final_idx]
        else:
            if len(time_arr) == len(digits_found):  # There is no character separating the `time` values 
                time_values        = digits_found[final_idx]
            else: 
                time_values        = digits_found[final_idx:final_idx + len(time_arr)]
            
      
    # Construct the time string and format according to locale presence if found 
    if len(local_found) > 0:
        
        hms_format         = "%" + "%".join(time_arr) + "%p"
        value              = value.lower()
        if value.find('am') != -1 or value.find('a.m') != -1 or value.find('a.m.') != -1 or value.find('am.') != -1:
            final_time_values = "".join(time_values) + "am"
        else:
            final_time_values = "".join(time_values) + "pm"
            
        return convert_to_time(final_time_values, hms_format)
    else:
       hms_format = "%" + "%".join(time_arr)
       final_time_values = "".join(time_values) 
    
       return convert_to_time(final_time_values, hms_format)    
    
# Update value based on user `action`
def time_update_value(value,action,data_type):
    
    if action == "remove":
        new_value = 'remove'
        return new_value
    
    if 'text' in action and 'text[D]' in action and '*' in action:
        
        # Find all digits 
        digit_pattern = re.compile("[\d]+")
        digits_found  = digit_pattern.findall(value)
        
        # Find the H(hour), M(minute) and S(seconds) direcives
        time_pattern  = re.compile('[HMS]')
        time_arr      = time_pattern.findall(action)
        
        # Find the `text[D]` action(s) index(indices)
        textd_pattern = re.compile('(text\\[D\\])')
        textd_idx     = [ m.start(0) for m  in textd_pattern.finditer(action)]
        
        # Find the H(hour) index 
        hour_pattern  = re.compile('[H]+')
        hour_idx      = [ m.start(0) for m  in hour_pattern.finditer(action)][0]
        
        
        # Find the start index for the time values to be used
        # in `digits_found` arr
        final_idx = 0
        for idx in textd_idx:
            if hour_idx < idx:
                break
            
            final_idx+=1
        
        # Check if there is a locale (i.e. am or pm)
        local_pattern = re.compile("[p]")
        local_found   = local_pattern.findall(action)
        
        # Get the time values from the digits found
        time_values        = digits_found[final_idx:final_idx + len(time_arr)]
        
        # Construct the time string and format according to locale presence if found 
        if len(local_found) > 0:
            
            hms_format         = "%" + "%".join(time_arr) + "%p"
            
            if value.find('am') != -1 or value.find('a.m') != -1 or value.find('AM') or value.find('A.M')!= -1:
                final_time_values = "".join(time_values) + "am"
            else:
                final_time_values = "".join(time_values) + "pm"
                
            return convert_to_time(final_time_values, hms_format)
        else:
           hms_format = "%" + "%".join(time_arr)
           final_time_values = "".join(time_values) 
        
           return convert_to_time(final_time_values, hms_format)
       
    elif 'text' in action and 'text[D]' in action and '*' not in action:
     
        return textd_to_time(value,action)
     
    elif 'text' in action and 'text[D]' not in action and '*' not in action:
        
        letter_pattern = re.compile("[A-Za-z]+")
        letters_found  = letter_pattern.findall(value)
        
        for letters in letters_found:
            letters = letters.strip()
            if letters.lower() == "am" or letters.lower() == "pm" or letters.lower() == "p.m" or letters.lower() == "a.m":
                continue
            else:
                value = value.replace(letters,'')
                
        value = value.strip()
        action = action.replace("text",'').strip()
        
        return create_time(value, action)       
        
    elif 'text' not in action and 'text[D]'  in action and '*'  in action:
         return textd_to_time(value,action,char='')
     
    elif 'text' not in action and 'text[D]'  in action and '*' not in action:
     
        return textd_to_time(value,action)
    elif 'text' not in action and 'text[D]' not in action and '*'  in action:
        
        action = action.replace('*','').strip()
        return create_time(value, action)        
        
    elif 'text'  in action and 'text[D]' not in action and '*'  in action:
        
        value, action = remove_text(value, action)
        
        action = action.replace('*','').strip()
        
        # Check if there are date `action` characters
        date_char_pattern = re.compile('[bByYd]')
        date_char_found   = date_char_pattern.findall(action)
        
        # Replace each according
        if len(date_char_found) > 0:
            for char in date_char_found:
                if char == "B" or char == "b":
                    action = action.replace(char,"text")
                elif char =="d" or char == "y" or char == "Y":
                    action = action.replace(char,"text[D]")
            
            # Call the update function again (recursion)        
            return time_update_value(value,action, data_type)
        
        
        return create_time(value, action)
        
    
    elif 'text' not in action and 'text[D]' not in action and '*'  not in action:
         punct_pattern = re.compile("[\W]+")
         found_punct   = punct_pattern.findall(value)
         
         # Replace each punct with ''
         if len(found_punct) > 0: 
            for punct in found_punct:
                value  = value.replace(punct,'')
             
         # Add the % to each provided directive
         format_ = ''
         for char in action:
             format_+="%"+char
         
         try:    
             new_value = convert_to_time(value,format_)
             
             return new_value
         except Exception as e:
             
             return None
         
        
    elif 'text' not in action and 'text[D]'  in action and '*'  in action:
        pass