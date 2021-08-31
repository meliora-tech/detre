# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 10:56:46 2021

@author: Detre 
"""

import re
from flask import session


#=======================================================        
# Main function called by the API.  It returns the original and detre values 
# for phone numbers
#=======================================================  
def detre_phone(df,country_code):
    """
    Main function called from API for phone numbers
    """
    all_data = []
    correct_ = []
    incorrect = []
    
    
    for idx,v in enumerate(df):
        
        ans,value = phone_number(str(v), country_code)
        
        if ans == "incorrect":
            incorrect.append({"row":idx,"value":str(v),"new_value":"","detre":value}) 
        else:
            correct_.append({"row":idx,"value":str(v),"detre":value})

    
    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data


#=======================================================        
# Function used to see if a phone number has either text, characters or both
#======================================================= 
def phone_number(number,country_codes):
    
    """
    Utility function used to check  if phone number as text or characters or both
    """
    char_pattern = re.compile("[\W]+")
    text_pattern = re.compile("[A-Za-z]+")
    
    text_in_number = text_pattern.findall(number)
    char_in_number = char_pattern.findall(number)
    
    # Check if number has text and special characters
    if len(text_in_number) != 0 and len(char_in_number) != 0:
        return "incorrect","Has text and special characters"
        
    # Check if it has only text and no characters
    elif  len(text_in_number) != 0 and len(char_in_number) == 0:
        digits_pattern = re.compile("[^\D]+") 
        
        phone_numbers = digits_pattern.findall(number)
        
        if len(phone_numbers) > 0:
            return phone_check(phone_numbers[0],country_codes,"Has text but no special characters. Provide guidanace")
        
        return "incorrect","Has text but no special characters. Provide guidanace"
    # Check if it has only characters and no text
    elif len(text_in_number) == 0 and len(char_in_number) != 0:
        
        # Replace the special character(s)
        new_value = number
        for char in char_in_number:
            new_value = new_value.replace(char,'')
            
        return phone_check(new_value,country_codes,"Has special characters but no text. Provide guidanace")
    
    # Check if its only numbers
    elif len(text_in_number) == 0 and len(char_in_number) == 0:
        len_cc = len(country_codes)
        
        if country_codes == number.strip()[:len_cc]: # already has a country code
           
            return "correct",number
        else:
            if len(number) == 10:   # Has the correct number of digits, add country code
                
                return "correct",str(country_codes) + str(number[1:])
            elif len(number) == 9:
                return "correct",str(country_codes) + str(number)
            else:  # Need guidance from the user. There are multiple numbers
                return "incorrect","guidance"
                
 
#=======================================================        
# Util function used by other functions.  
#=======================================================        
def phone_check(number,country_codes, msg):
    char_pattern = re.compile("[\W]+")
    char_in_country_codes = char_pattern.findall(country_codes)

    if len(char_in_country_codes) > 0:
        for char in char_in_country_codes:
            country_codes = country_codes.replace(char,'')    
   
    len_cc = len(country_codes)
    
    number = number.strip()
    if country_codes == number[:len_cc]: # already has a country code
        
        if number[len_cc] == '0':
            
            return "correct", str(session.get("country_code",'')) + str(number[len_cc+1:])
    
        return "correct",number
    else:
        if len(number) == 10:   # Has the correct number of digits, add country code
            
            return "correct",str(session.get("country_code",'')) + str(number[1:])
        elif len(number) == 9:
            return "correct",str(session.get("country_code",'')) + str(number)
        else:  # Need guidance from the user. There are multiple numbers or something 
            return "incorrect",msg       
        
        
        
def _text_digit_and_tel(value,action):
    """
     Function used to convert given value to phone number using the `action` characters where `action` has tel 
    """
    digits_pattern    = re.compile("[^\D]+") 
    text_digits_idx   = [m.start() for m in re.finditer('text\[D\]', action)]
    tel_idx           = [m.start() for m in re.finditer('tel', action)]
    count_text_digits = len(text_digits_idx)
    all_numbers       = digits_pattern.findall(value)
    count_numbers     = len(all_numbers)
    
    tel_count         = count_numbers - count_text_digits
    
    i= 0
    remove_numbers = []
    # Assumes all the text[D] are at the beginning
    # Get all the idx where to remove the text numbers
    for idx in text_digits_idx:
        if idx < tel_idx[0]:
            remove_numbers.append(i)
            i+=1
        else:
            i+=tel_count
            remove_numbers.append(i)
            
    # Remove the text numbers
    value_arr = list(value)
    for idx in remove_numbers:
        value_arr[idx] = ''
    
    
    return session.get("country_code",'') + "".join(value_arr)

       
def _text_digit_and_digits(value,action):
    
    """ 
     Function used to convert string to phone number based on given `action` where `action` as 'd'(s) 
    """
    digits_pattern    = re.compile("[^\D]+") 
    text_digits_idx   = [m.start() for m in re.finditer('text\[D\]', action)]
    tel_idx           = [m.start() for m in re.finditer('d', action)]
    count_text_digits = len(text_digits_idx)
    all_numbers       = digits_pattern.findall(value)
    
    count_numbers     = len(all_numbers[0])
    min_tel_idx       = min(tel_idx)
    max_tel_idx       = max(tel_idx)
    
    tel_count        = count_numbers - count_text_digits 
        

    remove_numbers = []
    max_tel_count  = 0
    mid_tel_count  = 0 
    min_tel_count  = 0
    mid_tel_total  = 0
    for idx in text_digits_idx:
            if idx < min_tel_idx:
                remove_numbers.append(idx)
                min_tel_count  +=1
            elif idx > max_tel_idx:

                if mid_tel_total == 0:
                    remove_numbers.append(tel_count + max_tel_count)
                else:
                    remove_numbers.append(tel_count + max_tel_count + mid_tel_total)
                max_tel_count+=1
            else: # text[D] is in the middle
                if mid_tel_count == 0 and min_tel_count ==0 :
                    remove_numbers.append(idx)
                    mid_tel_count+=1
                    mid_tel_total+=1
                elif mid_tel_count == 0 and min_tel_count == 1 :
                    
                    remove_numbers.append(idx - 6)  # text[D] has 7 characters
                    mid_tel_count+=1
                    mid_tel_total+=1
                else: 
                    
                    # The next text[D] is adjacent (i.e. next) to the first one
                    
                    if idx - text_digits_idx[mid_tel_count-1] == 7:
                        remove_numbers.append(idx - text_digits_idx[mid_tel_count-1])
                    else: # The next text[D] is not adjacent (i.e. next) to the first one
                       
                         
                         if text_digits_idx[mid_tel_count-1] == 0:
                             step = (idx - text_digits_idx[mid_tel_count-1])%7 + 2
                         else:
                             step = (idx - text_digits_idx[mid_tel_count-1])%7 + 1
                             
                         remove_numbers.append(text_digits_idx[mid_tel_count-1] + step)
                      
                    mid_tel_total+=1
    
    value_arr = list(value)
    
    for idx in remove_numbers:
        value_arr[idx] = ''
        
    
    return value_arr

#=======================================================        
# Function used to update the number based on the `action`
# given by the user.   
#=======================================================          
def phone_update_value(value,action,data_type):
    
    """
    Main function used to update phone number based on the user given `action`
    """
    
    
    if "tel" in action and "d" in action:  # Not supported yet.  User has to choose "tel" or "d"
        return None
    
    
    if "text[D]" in action and "tel" in action and "*" not in action:
        
        digits_pattern    = re.compile("[^\D]+") 
        text_digits_idx   = [m.start() for m in re.finditer('text\[D\]', action)]
        tel_idx           = [m.start() for m in re.finditer('tel', action)]
        count_text_digits = len(text_digits_idx)
        all_numbers       = digits_pattern.findall(value)
        count_numbers     = len(all_numbers)
        
        tel_count         = count_numbers - count_text_digits
        
        i= 0
        remove_numbers = []
        # Assumes all the text[D] are at the beginning
        # Get all the idx where to remove the text numbers
        for idx in text_digits_idx:
            if idx < tel_idx[0]:
                remove_numbers.append(i)
                i+=1
            else:
                i+=tel_count
                remove_numbers.append(i)
                
        # Remove the text numbers
        value_arr = list(value)
        for idx in remove_numbers:
            value_arr[idx] = ''
        
        
        return session.get("country_code",'') + "".join(value_arr)
    
    
    elif "text[D]" in action and "tel" in action and "*"  in action:
        
        # remove special characters
        non_digit_pattern = re.compile("[\D]+")
        value             = re.sub(non_digit_pattern,'',value)
        action            = action.replace('*','')
        
        return _text_digit_and_tel(value,action)
    
    
    elif "text[D]" in action and "d" in action and "*"  in action:
        
        # remove special characters
        non_digit_pattern = re.compile("[\D]+")
        value             = re.sub(non_digit_pattern,'',value)
        action            = action.replace('*','')
       
        digits_pattern    = re.compile("[^\D]+") 
        text_digits_idx   = [m.start() for m in re.finditer('text\[D\]', action)]
        tel_idx           = [m.start() for m in re.finditer('d', action)]
        count_text_digits = len(text_digits_idx)
        all_numbers       = digits_pattern.findall(value)
        
        count_numbers     = len(all_numbers[0])
        min_tel_idx       = min(tel_idx)
        max_tel_idx       = max(tel_idx)
        
        tel_count        = count_numbers - count_text_digits 
            
    
        remove_numbers = []
        max_tel_count  = 0
        mid_tel_count  = 0 
        min_tel_count  = 0
        mid_tel_total  = 0
        for idx in text_digits_idx:
                if idx < min_tel_idx:
                    remove_numbers.append(idx)
                    min_tel_count  +=1
                elif idx > max_tel_idx:

                    if mid_tel_total == 0:
                        remove_numbers.append(tel_count + max_tel_count)
                    else:
                        remove_numbers.append(tel_count + max_tel_count + mid_tel_total)
                    max_tel_count+=1
                else: # text[D] is in the middle
                    if mid_tel_count == 0 and min_tel_count ==0 :
                        remove_numbers.append(idx)
                        mid_tel_count+=1
                        mid_tel_total+=1
                    elif mid_tel_count == 0 and min_tel_count == 1 :
                        
                        remove_numbers.append(idx - 6)  # text[D] has 7 characters
                        mid_tel_count+=1
                        mid_tel_total+=1
                    else: 
                        
                        # The next text[D] is adjacent (i.e. next) to the first one
                        
                        if idx - text_digits_idx[mid_tel_count-1] == 7:
                            remove_numbers.append(idx - text_digits_idx[mid_tel_count-1])
                        else: # The next text[D] is not adjacent (i.e. next) to the first one
                           
                             
                             if text_digits_idx[mid_tel_count-1] == 0:
                                 step = (idx - text_digits_idx[mid_tel_count-1])%7 + 2
                             else:
                                 step = (idx - text_digits_idx[mid_tel_count-1])%7 + 1
                                 
                             remove_numbers.append(text_digits_idx[mid_tel_count-1] + step)
                          
                        mid_tel_total+=1
        
        value_arr = list(value)
        
        for idx in remove_numbers:
            value_arr[idx] = ''
        
           
        return session.get("country_code",'') + "".join(value_arr)
    
    
    
    elif "text[D]" in action and "d" in action and "*" not in action:
        value_arr = _text_digit_and_digits(value,action)
        return session.get("country_code",'') + "".join(value_arr)
    
    elif "tel" in action:
        if "text" in action and "*" not in action:
            text_pattern = re.compile("[^A-Za-z]+")
            tel          = text_pattern.findall(value)
            
            if len(tel) == 0:
                return None
            else:
                ans, phone = phone_number(tel[0],session.get("country_code",''))
                if ans == "correct":
                    return phone
                else:
                    return None
                
            
    else:
        pass
        
if __name__ == "__main__":

    phone_number("27608314773", "27")        