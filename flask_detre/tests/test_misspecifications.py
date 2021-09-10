# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 10:46:32 2021

@author: Detre

# See the followin to solve "SessionNotCreatedException: session not created: This version of ChromeDriver only supports Chrome version 90
# Current browser version is 93.0.4577.63 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe"
# See: https://stackoverflow.com/questions/62155465/sessionnotcreatedexception-this-version-of-chromedriver-only-supports-chrome-ve
# See: https://stackoverflow.com/a/58727916/9928905

"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import itertools
import pytest
import os
import time
import glob
# from flask import Flask, session
# from flask_detre import create_app


#app = create_app()


CHROMEDRIVER_DIR = "C:/Users/27608/Documents/Chrome Drivers/chromedriver"    
   

                
filenames      = ["date.csv","country.csv","text.csv","phone.csv","time.csv","whole.csv","decimal.csv",
                  "currency.csv","datetime.csv"]
data_types     = [ "date","country","text","phone","time","whole","decimal","currency","datetime"]
files          = [f for f in filenames]
  

params = []
# Create the params for the misspecification
for f,fn in zip(files,filenames):
    comb_dt = list(itertools.product([f],[fn.replace(".csv","")],data_types))
    for comb in comb_dt:
        params.append(comb)

   




 

@pytest.fixture
def setup_and_teardown():
    """
    Setup and Teardown the Headless Chrome Browswer
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")


    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR, options=options)
    #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR)
    yield driver
    
    driver.close()
    
    
@pytest.mark.parametrize("file,type1,type2",params)   
def test_data_type_misspecification(setup_and_teardown,request,file ,type1, type2):    
    """
    Test misspecification for each data type.  Does the `Results` page appear despite the
    incorrect data type provided by the user
    """  
    setup_and_teardown.get("http://www.localhost:8100/")
    
    btn = setup_and_teardown.find_element_by_id("get-started")
    btn.click()
    
    form = setup_and_teardown.find_element_by_id("fallback-file")
    #"C:/Users/27608/Documents/Detre/flask_detre/tests/files/date.csv"
    fn = os.path.join(request.fspath.dirname,"files",file)
    
    form.send_keys(fn)
    
    time.sleep(2)    
    # click proceed
    setup_and_teardown.find_element_by_id("proceed").click()
    
    
    # select the type
    select_name = type1 + "-" + file + "-" + "select" 
    select = Select(setup_and_teardown.find_element_by_name(select_name)) # "date-date.csv-select"
    
    select.select_by_value(type2)
    
    if type2 == "phone":
        time.sleep(2) 
        select_phone = Select(setup_and_teardown.find_element_by_name(type1+"-country-code-select"))
        select_phone.select_by_value("27")
       
    # click submit
    setup_and_teardown.find_element_by_css_selector("button[type='submit']").click()
    
    assert setup_and_teardown.find_element_by_id(type1+'-column-tab').text == type1
    
    
    

    # driver.get("http://www.localhost:8100/")
    
    # btn = driver.find_element_by_id("get-started")
    # btn.click()
    
    # form = driver.find_element_by_id("fallback-file")
    
    # form.send_keys("C:/Users/27608/Documents/Detre/flask_detre/tests/files/date.csv")
    
    # time.sleep(2)    
    # # click proceed
    # driver.find_element_by_id("proceed").click()
    
    
    # # select the type
    # select = Select(driver.find_element_by_name("date-date.csv-select"))
    
    # select.select_by_value("phone")
    
    
    # select_phone = Select(driver.find_element_by_name("date-country-code-select"))
    # select_phone.select_by_value("27")
    # # click submit
    # driver.find_element_by_css_selector("button[type='submit']").click()
    
    # assert driver.find_element_by_id('date-column-tab').text == type1    
