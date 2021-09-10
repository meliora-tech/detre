# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 14:39:09 2021

@author: Detre
"""

import re
from flask_detre.utils.text_constants import (EMAIL_REGEX, URL_REGEX, 
                                              PUNCT_TRANSLATE_UNICODE, PHONE_REGEX)


#  Email  
def _email(text):
    all_emails  = []
    if  EMAIL_REGEX.search(text) != None :
        
        emails      = re.finditer(EMAIL_REGEX, text)    
    
        for email in emails:
            all_emails.append(email.group(0))    
        
    return all_emails


def _url(text):
    all_urls  = [] 
    if URL_REGEX.search(text) != None:    
       
        urls      = re.finditer(URL_REGEX, text)
        
        for url in urls:
            all_urls.append(url.group(0))  
    
    return all_urls


def _phone(text):
    all_phones  = [] 
    if PHONE_REGEX.search(text) != None:    
        
        phones      = re.finditer(PHONE_REGEX, text)
        
        for phone in phones:
            all_phones.append(phone.group(0))     

    return all_phones

def _punct(text):
    return text.translate(PUNCT_TRANSLATE_UNICODE) 


def remove(text,items):
    for item in items:
        text = text.replace(item,'')
        
    return text



def extract(text,items):
    pass



def replace(text,repl,items):
    pass


def detre_text_extract(text,type_):
        """
            Function used to extract a given 'type' of string
        """
        if type_ == "url":
            all_urls = _url(text)
            if len(all_urls) == 0:
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
                text       = all_phones[0] if len(all_phones) > 1 else ",".join(all_phones)    
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
      




def detre_text(df,actions,types_):

    all_data  = []
    correct_  = []
    incorrect = []    
    

    if len(actions) == 0 and len(types_) == 0:
        for idx, vtext in enumerate(df):
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
                
                ans, value = detre_text_extract(text,type_)
               
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
               
            
            
            
