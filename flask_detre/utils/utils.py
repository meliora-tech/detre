# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 15:53:15 2021

@author: Detre
"""

import pandas as pd
import re
from collections import Counter


def detre_find_months(holder,action,value):
        month_directives = r'[bBm]'
        pattern   = re.compile(month_directives)
        found_patterns =  pattern.findall(action)
        
        if found_patterns:
            count = Counter(found_patterns)
            
            for key in count.keys():
                if key == 'b':
                    b_month = r'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
                    month_pattern = re.compile(b_month)
                    
                    holder["month"] = {'b': month_pattern.findall(value.lower())}

                    
                elif key == 'B':
                    B_month = r'january|february|march|april|may|june|july|august|september|october|november|december'
                    month_pattern = re.compile(B_month)
                    
                    holder["month"] = {'B': month_pattern.findall(value.lower())}                    
                elif key == 'm':
                     pattern = re.compile(r'[^\D]+')
                     act     = action.replace('*','').replace('text','')
                     matches = pattern.findall(value)
                     idx   = act.find('m') 
                     
                     if len(matches) == 1:
                         
                         month = matches[0][idx:idx+2]
                         holder["month"] = {'m': month}
                        
                     else:  # Its an array
                         month  = matches[idx]
                         holder["month"] = {'m': month}


def detre_find_years(holder,action,value):
    year_directives = r'[yY]'
    
    pattern   = re.compile(year_directives)
    found_patterns =  pattern.findall(action)
    
    if found_patterns:
        count = Counter(found_patterns)
        
        for key in count.keys():
            if key == 'y':
                pattern = re.compile(r'[^\D]+')
                act     = action.replace('*','').replace('text','')
                matches = pattern.findall(value)
                idx   = act.find('y') 
                
                if len(matches) == 1:
                    
                    year = matches[0][idx:idx+2]
                    holder["year"] = {'y': year}
                   
                else:  # Its an array
                    year  = matches[idx]
                    holder["year"] = {'y': year}
            elif key == 'Y':
                pattern = re.compile(r'[^\D]+')
                act     = action.replace('*','').replace('text','')
                matches = pattern.findall(value)
                idx   = act.find('Y') 
                
                if len(matches) == 1:
                    
                    year = matches[0]
                    holder["year"] = {'Y': year}
                   
                else:  # Its an array
                    year  = matches[idx]
                    holder["year"] = {'Y': year}
            

def detre_find_days(holder,action,value):
    day_directives = r'[d]'
    pattern        = re.compile(day_directives)
    found_patterns =  pattern.findall(action)

    if found_patterns:
        count = Counter(found_patterns)
        
        for key in count.keys():
            if key == 'd':
                pattern = re.compile(r'[^\D]+')
                act     = action.replace('*','').replace('text','')
                matches = pattern.findall(value)
                idx   = act.find('y') 
                
                if len(matches) == 1:
                    
                    day = matches[0][idx:idx+2]
                    holder["day"] = {'d': day}
                   
                else:  # Its an array
                    day  = matches[idx]
                    holder["day"] = {'d': day}
    
  
    
def detre_formatter(char):
    
    clean_char  = char.strip() 
    if clean_char == 'm':
        
        pass    
    
    
def get_new_value(value, months_found,alpha_pattern,action,directive):
        if len(months_found) == 1:
           
            update_value = value.lower().replace(months_found[0],'')
            found_alpha    = alpha_pattern.findall(update_value)
            
            for w in found_alpha:
                update_value = update_value.replace(w,'')
                
            clean_action = action.replace('text','').strip()
            action_format = ''
            
            for char in clean_action:
                if char.strip() != directive:
                    action_format += '%' + char
                
                
            action_format += '%' + directive
            update_value  += months_found[0]                 
            new_value    = pd.to_datetime(update_value.strip(),format=action_format)
            
            return new_value.strftime('%Y-%m-%d')                            
            
        else:
            
            for month_found in months_found:
                update_value = value.lower().replace(month_found,'')
                found_alpha    = alpha_pattern.findall(update_value)
                
                for w in found_alpha:
                    update_value = update_value.replace(w,'')
                    
                clean_action = action.replace('text','').strip()
                action_format = ''
                
                for char in clean_action:
                    if char.strip() != directive:
                        action_format += '%' + char
                    
                action_format += '%' + directive
                update_value  += month_found                     
                new_value    = pd.to_datetime(update_value.strip(),format=action_format)
                
                return new_value.strftime('%Y-%m-%d')    
    
def excel_number_conversion(value:str):
    
    seconds     = (int(value) - 25569)*86400
    new_value   = pd.to_datetime(seconds, unit='s')
    
    return new_value.strftime('%Y-%m-%d')
    
def remove_entry():
    return 'remove'

def no_text_and_char(value:str, action:str):
    ans = ''
    for char in action:
        ans+='%'+char
    
    new_value = pd.to_datetime(value,format=ans)
    
    return new_value.strftime('%Y-%m-%d')



def char_no_text(holder:dict,value:str, action:str):
    pattern_dt_all = re.compile(r'[dbBmyY]')
    
    all_counts = Counter(pattern_dt_all.findall(action))
    count      = False
    for k,v in all_counts.items():
        if v > 1:
            count = True
    
    # There is  one character of each
    if not count:
        # Find all non-alpanumeric characters
        pattern = re.compile(r'[^\d\w]+')
        matches = pattern.findall(value)
        
        if len(matches) == 1:
            clean_value = value
            for char in matches[0]:
                
                clean_value = clean_value.replace(char,'')
                
                
            clean_action = action.replace('*','') 
            action_format = ''
            for char in clean_action:
                action_format+='%'+char
             
            new_value    = pd.to_datetime(clean_value,format=action_format)
            
            
            return new_value.strftime('%Y-%m-%d')
        
    else:
        
        # Find day, month and year
        try:
            detre_find_days(holder,action,value)
            
            detre_find_months(holder,action,value)
            
            detre_find_years(holder, action, value)
        except:
            return None
       
        
       # construct final date
        return construct_date(holder,'%Y-%m-%d')



def text_no_char(value:str,action:str):

        if action.find('b') == -1 and action.find('B') == -1:
            alpha_pattern  = re.compile(r'[A-Za-z]+')
            found_alpha    = alpha_pattern.findall(value)
            clean_value    = value
            for w in found_alpha:
                clean_value = clean_value.replace(w,'')
            
            clean_action = action.replace('text','').strip()
            action_format = ''
            
            for char in clean_action:
                action_format += '%' + char
            new_value    = pd.to_datetime(clean_value.strip(),format=action_format)
            return new_value.strftime('%Y-%m-%d')
            
        elif action.find('b') != -1 and  action.find('B') == -1:  # Handle the case for 'Jan','Feb', etc
                
                #digits        = '[^\D]+'
                b_month       = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
                alpha_pattern = re.compile(r'[A-Za-z]+')
                month_pattern = re.compile(b_month)  
                months_found  = month_pattern.findall(value.lower())
                
                
                new_value     = get_new_value(value, months_found, alpha_pattern, action,'b')
                return new_value
                
        elif action.find('B') != -1 and action.find('b') == -1:
            
                B_month       = 'january|february|march|april|may|june|july|august|september|october|november|december'
                alpha_pattern = re.compile(r'[A-Za-z]+')
                month_pattern = re.compile(B_month)  
                months_found  = month_pattern.findall(value.lower())                    
                new_value     = get_new_value(value, months_found, alpha_pattern, action,'B')
                return new_value    
    
    

def text_and_char(value:str, action:str):
    if action.find('b') == -1 and action.find('B') == -1: # Both are not present
        alpha_pattern = re.compile(r'[A-Za-z]+')                
        new_value     = get_value(value,action,[],alpha_pattern,'')
        return new_value
        
        
    elif action.find('b') != -1 and action.find('B') == -1:  # Handle the case for 'Jan','Feb', etc
    
        # The special month names should not be removed
        b_month = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
        alpha_pattern = re.compile(r'[A-Za-z]+')
        month_pattern = re.compile(b_month) 
        months_found  = month_pattern.findall(value.lower())
        new_value     = get_value(value,action,months_found,alpha_pattern,'b')
        return new_value
        
        
    elif action.find('B') != -1 and action.find('b') == -1: # Handle the case for 'January','February', etc
            B_month       = 'january|february|march|april|may|june|july|august|september|october|november|december'
            alpha_pattern = re.compile(r'[A-Za-z]+')
            month_pattern = re.compile(B_month)  
            months_found  = month_pattern.findall(value.lower())
            new_value     = get_value(value,action,months_found,alpha_pattern,'B')
            return new_value







def get_value(value:str,action:str,months_found:list,alpha_pattern:str,directive:str):
    
    update_value   = value if len(months_found) == 0 else value.lower().replace(months_found[0],'') 
    found_alpha    = alpha_pattern.findall(update_value)     
    clean_value    = update_value
    
    for w in found_alpha:
        clean_value = clean_value.replace(w,'')
        
    clean_value = clean_value.strip()    
    
    punc_pattern = re.compile(r'[^\d\w]+')
    matches = punc_pattern.findall(clean_value)
    
    for char in matches:
        clean_value = clean_value.replace(char,'') 
    
    clean_action = action.replace('text','').strip()
    clean_action = clean_action.replace("*",'').strip()
    
    
    action_format = ''
    
    for char in clean_action:
        if char.strip() != directive:
           action_format += '%' + char
    
    if directive != '' and len(months_found) != 0:    
        action_format+= '%' + directive    
        clean_value  += months_found[0]     
        
    new_value    = pd.to_datetime(clean_value,format=action_format)
    return new_value.strftime('%Y-%m-%d') 



def construct_date(holder:dict, format_:str):
        action_format   = ''
        clean_value     = ''
        for k in holder.keys():
            if k == 'month':
               key    = list(holder[k].keys())[0]  
               action_format   += '%' + key
               clean_value += holder[k][key][0] if isinstance(holder[k][key], list) else holder[k][key]
               
            elif k == 'year':
               key    = list(holder[k].keys())[0]  
               action_format   += '%' + key
               clean_value += holder[k][key][0] if isinstance(holder[k][key], list) else holder[k][key]      
               
               
        new_value    = pd.to_datetime(clean_value,format=action_format)
            
           
        return new_value.strftime(format_)    

    


                    


def detre_date(df,format_):
    
    all_data = []
    correct_ = []
    incorrect = []
    #format_  = "%Y-%m-%d, %H:%M:%S"
    #format_  = "%Y-%m-%d"
    pattern = re.compile(r'[\D]+')
    for idx,v in enumerate(df):
        try:
            #df.astype({"datetime":"datetime64[ns]"})
            #print(pd.to_datetime(v))
            if isinstance(v,str):
                val = v.strip().replace('\\t',' ').replace('\\n',' ')
                correct_.append({"row":idx,"value":v,"detre":pd.to_datetime(val).strftime(format_)})
            else:
                incorrect.append({"row":idx,"value":v,"new_value":"","detre":'Not a date'})                
        except Exception as e:
            num_ = pattern.findall(v)
            
            if len(num_) == 0:
                incorrect.append({"row":idx,"value":v,"new_value":"","detre":'Number(s) found. Potentially has a date pattern'})
                #print(f"No number found. {v}")
                
                
            elif len(num_) >=1 and len(num_) <=3:
                
                
                # Check if there is a year
                year_range = range(1655,2955)
                if len(num_) == 1:   # Assume its a year
                    
                    # Check how many letters it has
                    len_  = len(num_[0])
                    if len_ == 2:       
                        
                        incorrect.append({"row":idx,"value":v,"new_value":"","detre":'year2'})
                        #print(f"Is this a year? 20{num_[0]} or 19{num_[0]}")
                    elif len_ == 4 :
                        # Check if it falls within the range
                        if num_[0] in year_range:
                            incorrect.append({"row":idx,"value":v,"new_value":"","detre":'year4' })
                            #print(pd.to_datetime(num_[0]))
                            #print(f"{num_[0]}")
                        else:
                            incorrect.append({"row":idx,"value":v,"new_value":"","detre":'Guidance'})
                            #print(f"Is this number of days from Epoch? Is the format mm/yy or yy/mm? Is it dd/mm or mm/dd? {num_[0]}")
                    else:
                        incorrect.append({"row":idx,"value":v,"new_value":"","detre":'Guidance'})
                        #print(f"No idea what to do: {num_[0]}")
                        
                elif len(num_) == 2: # Assume its a year and month
                    
                    try:
                        year_month = pd.to_datetime("-".join(num_)).strftime(format_)
                        correct_.append({"row":idx,"value":v,"detre":year_month})
                    except Exception as e:
                        sum_len = sum([len(n)  for n in num_])    
                        # Case 1:  4 & 2
                        if sum_len == 6:
                            incorrect.append({"row":idx,"value":v,"new_value":"","detre":'guidance-yyyymm'})
                            # print("Is this yyyymm or mmyyyy? ")
                        # Case 2:  4 & 4
                        elif sum_len == 8:
                            incorrect.append({"row":idx,"value":v,"new_value":"","detre":'guidance-yyyymmdd'})
                            # print("Is this yyyymmdd or mmddyyy or ddmmyyyy?")
                        # Case 3:  1 & 2 
                        elif sum_len == 3: 
                           incorrect.append({"row":idx,"value":v,"new_value":"","detre":'guidance-yym'}) 
                           # print("Is this myy or yym?")
                        # Case 4:  1 & 4
                        elif sum_len == 5:
                            incorrect.append({"row":idx,"value":v,"new_value":"","detre":'guidance-yyyym'})
                            # print("Is this myyyy or yyyym?")
                        
                        
            
                        
                else:
                    a = "-".join(num_)
                    incorrect.append({"row":idx,"value":v,"new_value":"","detre":'There is a date pattern with some text.'})
                    #print(f"Has year/month/day. {a}")
            elif len(num_) > 3:
                pd.to_datetime("-".join(num_))
                incorrect.append({"row":idx,"value":v,"new_value":"","detre":'datetime'})
                #print("Has year/month/day hh/min/ss. Select the closest option to your data.")

    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})
    return all_data



def get_correct_values_as_series(detre_data):
    """
    Function gets the `correct` values from the detre_XXX output function. The series output is used 
    as an input in the profile function
    """
    
    correct_arr = detre_data[0]["correct"]
    
    df_correct      = pd.DataFrame(correct_arr)
    
    return df_correct["value"]