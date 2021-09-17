# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 14:39:09 2021

@author: Detre
"""

import html
import arrow
import re
from flask_detre.utils.text_constants import (EMAIL_REGEX, URL_REGEX, 
                                              PUNCT_TRANSLATE_UNICODE, PHONE_REGEX, 
                                              NUMBERS_REGEX, PHONE_REGEX_, DATE_ARR,
                                              PHONE_REGEX_UNIVERSAL)


from typing import List


def _date(text:str,fmt : List, all_dates: List ):
    """
    Function used to extract dates
    """
    
    
    
    for idx in fmt:
        try:
          ans = arrow.get(text,DATE_ARR[int(idx)]).datetime.date()
          #print(ans)
          all_dates.append(str(ans))
          fmt.pop(0)
        except Exception as e:
            # print(e)
            fmt.pop(0)
            if len(fmt) > 0:
                _date(text,fmt,all_dates)
            else:
                return all_dates
            
    return all_dates

def _email(text):
    """
    Function used to extract email(s)
    """
    all_emails  = []
    if  EMAIL_REGEX.search(text) != None :
        
        emails      = re.finditer(EMAIL_REGEX, text)    
    
        for email in emails:
            all_emails.append(email.group(0))    
        
    return all_emails


def _url(text):
    """
    Function used to extract url(s)
    """
    all_urls  = [] 
    
    if len(re.split("href=",text)) > 0: # For html tags
        arr = re.split("href=",text)
        
        for txt in arr:
            if URL_REGEX.search(txt) != None: 
                urls      = re.finditer(URL_REGEX, txt)
                
                for url in urls:
                    final_url = re.sub(r"<img |</a>|>|<|(?!src=)",'',url.group(0))
                    all_urls.append(final_url)        
            
    
    if len(re.findall(r"(\.\.\.)",text)) > 0: 
        text = re.sub(r"(\.\.\.)"," ",text)
        
    if URL_REGEX.search(text) != None:    
        # Escape the html tags
        
        urls      = re.finditer(URL_REGEX, text)
        
        for url in urls:
            all_urls.append(url.group(0))  
        
        
    return all_urls





def _phone(text):
    """
    Function to extract phone number(s)
    """
    all_phones  = [] 
    text        = str(text)
    if PHONE_REGEX_UNIVERSAL.search(text) != None:    
        
        phones      = re.finditer(PHONE_REGEX_UNIVERSAL, text)
        
        for phone in phones:
            if len(phone.group(0)) >= 9:
                
                all_phones.append(phone.group(0).strip()) 
         
            
        # if PHONE_REGEX.search(text) != None:
        #     phones      = re.finditer(PHONE_REGEX, text)
        
        #     for phone in phones:
               
        #         if len(phone.group(0)) != 1:
        #             all_phones.append(phone.group(0).strip())         
        
    return all_phones

def _punct(text):
    """
    Function used to get all PUNCTUATION
    """
    return text.translate(PUNCT_TRANSLATE_UNICODE) 

def _numbers(text):
    """
    Function used to get all numbers from text
    """
    all_numbers = []
    if NUMBERS_REGEX.search(text) != None:
        numbers = re.finditer(NUMBERS_REGEX, text)
        
        for num in numbers:
            all_numbers.append(num.group(0))
            
    return all_numbers

def remove(text,items):
    for item in items:
        text = text.replace(item,'')
        
    return text



def extract(text,items):
    pass



def replace(text,repl,items):
    pass


def detre_text_extract(text,type_,date_fmt=None):
        """
            Function used to extract a given 'type' of string
        """
        

        
        if type_ == "date":
            cdate_fmt = date_fmt.copy()
            all_dates = _date(text,cdate_fmt,[])
            
            if len(all_dates) > 0:
                return "correct", ";".join(all_dates)
            
            return "incorrect", "No date found."
        
        if type_ == "numbers":
            all_numbers = _numbers(text)
            
            if len(all_numbers) == 0:
                return "incorrect", "No numbers found"
            else:
                return "correct", " ;".join(all_numbers)
        
        if type_ == "url":
            
            all_urls = _url(text)
            if len(all_urls) == 0:
                # Check if there is "//"
                if len(re.findall(r'\/\/.*[^"><]',text)) > 0:
                    ans = re.findall(r'\/\/.*[^"><]',text)
                    for url in ans:
                        all_urls.append(url)
                    
                    return "correct", ",".join(all_urls)
                
                
                
                
                return "incorrect", "No url found. Provide Guidance"
            else:
                
                text     = ",".join(all_urls)
                return "correct", text
        
        
        if type_ == "email":
            all_emails = _email(text)
            if len(all_emails) == 0:
                return "incorrect", "No email found. Provide Guidance"
            else:
                text       = all_emails[0] if len(all_emails) > 1 else ",".join(all_emails)
                return "correct", text
            
            
        if type_ == "phone":
            all_phones = _phone(text)
            if len(all_phones) == 0:
                return "incorrect", "No phone number found. Provide Guidance"
            else:
                text       = ",".join(all_phones) if len(all_phones) > 1 else   all_phones[0]  
                return "correct", text



def detre_text_remove(text, type_):
        """
            Function used to remove a given 'type' of string
        """

    
        if type_ == "url":
            all_urls = _url(text)
            if len(all_urls) == 0:
                
                return "incorrect", "No url found to remove. Provide guidance"
            else:
                text     = remove(text,all_urls)
                return "correct", text
                
        if type_ == "email":
             all_emails = _email(text)
             if len(all_emails) == 0:
                  return "incorrect", "No email found to remove. Provide guidance"
             else:
                 text       = remove(text, all_emails)
                 return "correct", text
             
                
        if type_ == "punct":
            text    = _punct(text)
            return "correct", text
            
        if type_ == "phone":
             all_phones = _phone(text)
             if len(all_phones) == 0:
                 return "incorrect", "No phone number found to remove. Provide guidance"
             else:
                 text       = remove(text, all_phones)                 
                 return "correct", text
      




def detre_text(df,actions,types_, date_fmt=None):

    """
    Main function used for `text` type `actions`
    """
    all_data  = []
    correct_  = []
    incorrect = []    
    

    if len(actions) == 0 and len(types_) == 0: # text only selection with no `action` provided
        for idx, vtext in enumerate(df):
            #vtext = html.escape(vtext)
            correct_.append({"row":idx, "value":vtext, "detre": vtext})
            
        all_data.append({"correct":correct_})
        all_data.append({"incorrect":incorrect})            
         
        return all_data        
    
    
    for idx, vtext in enumerate(df):
        
        # Remove
        value  = vtext
        if "remove" in actions:
            for action, type_ in zip(actions,types_):
                ans, value = detre_text_remove(value, type_)
                
            if ans == "incorrect":
                incorrect.append({"row":idx, "value":vtext, "detre": value})
            else:
                correct_.append({"row":idx, "value":vtext, "detre": value})        
        
            all_data.append({"correct":correct_})
            all_data.append({"incorrect":incorrect})           
            return all_data          
        
        text = vtext
        for action, type_ in zip(actions,types_):
        
            if action == "remove":
                
                ans, value = detre_text_remove(text, type_)
                
                if ans == "incorrect":
                    incorrect.append({"row":idx, "value":vtext, "detre": value})
                else:
                    correct_.append({"row":idx, "value":vtext, "detre": value})
                
            
            elif action == "extract":
                text  = html.escape(str(vtext))
                vtext = html.escape(str(vtext))
                if type_ != "date":
                    ans, value = detre_text_extract(text,type_, date_fmt=None)
                else:
                    ans, value = detre_text_extract(text,type_, date_fmt=date_fmt)
               
                if ans == "incorrect":
                    incorrect.append({"row":idx, "value":vtext, "detre": value})
                else:
                    correct_.append({"row":idx, "value":vtext, "detre": value})
                
                
                
            elif action == "replace":
                if type_ == "url":
                    all_urls = _url(text)
                    text     = replace(text,'', all_urls)
        
                incorrect.append({"row":idx, "value":vtext, "detre": text})

    all_data.append({"correct":correct_})
    all_data.append({"incorrect":incorrect})            
     
    return all_data
               
            
            
            
