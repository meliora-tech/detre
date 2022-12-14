# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 18:43:36 2021

@author: Detre
"""

import re
import unicodedata
import sys
import itertools 


date_arr = []
YEARS_CONSTANT  = ["YY","YYYY"]
MONTHS_CONSTANT = ["M","MM","MMM"]
DAYS_CONSTANT   = ["D","DD"]
DATE_CHAR       = ["-"," ","/","."]



# Year, month, day
for i in itertools.product(YEARS_CONSTANT,MONTHS_CONSTANT,DAYS_CONSTANT):
    for char in DATE_CHAR:
        date_arr.append(char.join(i))
        
# Year, day, month    
for i in itertools.product(YEARS_CONSTANT,DAYS_CONSTANT,MONTHS_CONSTANT):
    for char in DATE_CHAR:
        date_arr.append(char.join(i))

#  month, day, year
for i in itertools.product(MONTHS_CONSTANT,DAYS_CONSTANT,YEARS_CONSTANT):
    for char in DATE_CHAR:
        date_arr.append(char.join(i))

# day, month, year    
for i in itertools.product(DAYS_CONSTANT,MONTHS_CONSTANT,YEARS_CONSTANT):
    for char in DATE_CHAR:
        date_arr.append(char.join(i))    
    

DATE_ARR = date_arr


EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-](@|[(<{\[]at[)>}\]])(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))?",
    flags=re.IGNORECASE | re.UNICODE,
)


URL_DOMAIN_TLD_REGEX = re.compile(
    
    r"(?:"
    r"(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)"
    r"(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*"
    r"(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))" r"|" r"(?:(localhost))" r")",
    flags=re.UNICODE | re.IGNORECASE
    )


# Url 
URL_REGEX = re.compile(
   
    r"(?:^|(?<![\w\/\.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?:\/\/|ftp:\/\/|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?" r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))" r"|" r"(?:(localhost))" r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:\/[^\)\]\}\s]*)?",
    # r"(?:$|(?![\w?!+&\/\)]))",
    # @jfilter: I removed the line above from the regex because I don't understand what it is used for, maybe it was useful?
    # But I made sure that it does not include ), ] and } in the URL.
    flags=re.UNICODE | re.IGNORECASE,
)


# Numbers
NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+???-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))"
)

# Replace punct with ""
PUNCT_TRANSLATE_UNICODE = dict.fromkeys(
    (i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P")),
    "",
)


PHONE_REGEX = re.compile(
    r"((?:^|(?<=[^\w)]))(((\+?[01])|(\+\d{2}))[ .-]?)?(\(?\d{3,4}\)?/?[ .-]?)?(\d{3}[ .-]?\d{4})(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W)))|\+?\d{4,5}[ .-/]\d{6,9}"
)


PHONE_REGEX_ = re.compile(
  
   r'(\+?[-()\s\d]+?)+'
    )

PHONE_REGEX_UNIVERSAL = re.compile(
  
   r"(\+\d{1,3}( )?|\+\s\d{1,3}\s|\+\s?\d{1,3}\s?\(\d{1,2}\)|\(?\d{1,2}-?\)?\s?)?((\(\d{1,3}\))|\d{1,3})[- .]?\d{3,4}[- .]?\d{4,}"
    )


 # r'\+?[-()\s\d]+?(?=\s*[+<])'