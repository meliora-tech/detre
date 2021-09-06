# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 14:37:27 2021

@author: Text update
"""

from flask_detre.utils.text_constants import URL_DOMAIN_TLD_REGEX
import re

def text_email_update(value,action,data_type):
    
    
    if action.strip().lower() == "none" or action.strip().lower() == "remove"  or  None:
        return 'remove'
    
    return ""

    
def text_url_update(value, action, data_type):
    
    if action.strip().lower() == "none" or action.strip().lower() == "remove"  or  None:
        return 'remove'
    
    elif "domain[text]" in action:
         pass
     
    elif "domain" in action and "tld" in action:
        if "." not in action:
            return ""
        else:
           all_urls = [] 
           if  URL_DOMAIN_TLD_REGEX.search(value) != None:
                urls      = re.finditer(URL_DOMAIN_TLD_REGEX, value)    
    
                for url in urls:
                    all_urls.append(url.group(0)) 
                
                return all_urls
           else:
               return ""
    return ""