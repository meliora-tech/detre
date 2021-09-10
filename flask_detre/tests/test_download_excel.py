# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 13:36:26 2021

@author: Detre Team
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select

import glob
import os
import pytest
import requests
import time

from pathlib import Path


url = "http://localhost:8100"

DOWNLOADS_PATH   = str(Path.home() / "Downloads")
CHROMEDRIVER_DIR = "C:/Users/27608/Documents/Chrome Drivers/chromedriver"  

date_file  = "date.csv"
text_file  = "text.csv"





@pytest.fixture
def setup_and_teardown():
        
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR, options=options)
    #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR)
    yield driver
    
    driver.close()
    
    
    # driver.get("http://www.localhost:8100/")
    
    # btn = driver.find_element_by_id("get-started")
    # btn.click()
    
    # form = driver.find_element_by_id("fallback-file")
    
    # form.send_keys("C:/Users/27608/Documents/Detre/flask_detre/tests/files/date.csv")
    
    # time.sleep(2)    
    # # click proceed
    # driver.find_element_by_id("proceed").click()
     
    # select = Select(driver.find_element_by_name("date-date.csv-select"))
    
    # select.select_by_value("date")    
    
    # driver.find_element_by_css_selector("button[type='submit']").click()
    
    # driver.find_element_by_id("download-file").click()
    
    # download_folder_xlsx = glob.glob(os.path.join(DOWNLOADS_PATH,"*.xlsx"))
    
    # assert os.path.join(DOWNLOADS_PATH,"Detre Output.xlsx") in download_folder_xlsx

    
    # form.send_keys("C:/Users/27608/Documents/Detre/flask_detre/tests/files/date.csv")

    

def test_download_excel_file_fail():
    
    """
    Test downloading a file directly with no prior upload
    """    
    resp = requests.get(url+'/download/excel')   
    assert 500 == resp.status_code
    

    




def test_download_file_no_changes(setup_and_teardown,request):
    """
    Test when a user uploaded a file but made no changes and downloaded it again
    """
    
    setup_and_teardown.get("http://www.localhost:8100/")
    
    btn = setup_and_teardown.find_element_by_id("get-started")
    btn.click()
    
    form = setup_and_teardown.find_element_by_id("fallback-file")
    
    fn = os.path.join(request.fspath.dirname,"files",date_file)
    
    form.send_keys(fn)
    
    time.sleep(2)    
    
    # click proceed
    setup_and_teardown.find_element_by_id("proceed").click()
     
    select = Select(setup_and_teardown.find_element_by_name("date-date.csv-select"))
    
    select.select_by_value("date")    
    
    setup_and_teardown.find_element_by_css_selector("button[type='submit']").click()
    
    
    setup_and_teardown.find_element_by_id("download-file").click()
    
    time.sleep(5)
    download_folder_xlsx = glob.glob(os.path.join(DOWNLOADS_PATH,"*.xlsx"))
    
    
    assert os.path.join(DOWNLOADS_PATH,"Detre Output.xlsx") in download_folder_xlsx


def test_download_file_changes_new_column(setup_and_teardown,request):
    """
    Test when user has selected `text` data type with an `extract` action
    """
    
    setup_and_teardown.get("http://www.localhost:8100/")
    
    btn = setup_and_teardown.find_element_by_id("get-started")
    btn.click()
    
    form = setup_and_teardown.find_element_by_id("fallback-file")
    
    fn = os.path.join(request.fspath.dirname,"files",text_file)
    
    form.send_keys(fn)
    
    time.sleep(2)    
    
    # click proceed
    setup_and_teardown.find_element_by_id("proceed").click()
     
    select = Select(setup_and_teardown.find_element_by_name("text-text.csv-select"))
    
    select.select_by_value("text")

    # click `add`
    setup_and_teardown.find_element_by_id("add-text-action").click()
    
    time.sleep(3)
    setup_and_teardown.find_element_by_id("add-text-btn").click()    
    
    setup_and_teardown.find_element_by_css_selector("button[type='submit']").click()
    
    setup_and_teardown.find_element_by_id("download-file").click()
    
    time.sleep(5)
    download_folder_xlsx = glob.glob(os.path.join(DOWNLOADS_PATH,"*.xlsx"))
    
    assert os.path.join(DOWNLOADS_PATH,"Detre Output (1).xlsx") in download_folder_xlsx


def test_download_file_changes_normal(setup_and_teardown, request):
    """
    Test when a user makes changes via the data type keyboard
    """
    setup_and_teardown.get("http://www.localhost:8100/")
    
    btn = setup_and_teardown.find_element_by_id("get-started")
    btn.click()
    
    form = setup_and_teardown.find_element_by_id("fallback-file")
    
    fn = os.path.join(request.fspath.dirname,"files",text_file)
    
    form.send_keys(fn)
    
    time.sleep(2)    
    
    # click proceed
    setup_and_teardown.find_element_by_id("proceed").click()
     
    select_name =  text_file.replace(".csv","") + "-" + text_file + "-select"  
    select = Select(setup_and_teardown.find_element_by_name(select_name))
    
    select.select_by_value("date")    
    
    setup_and_teardown.find_element_by_css_selector("button[type='submit']").click()
    
    # Make changes to the date
    
    setup_and_teardown.find_element_by_id("text-column-tab").click()
    
    setup_and_teardown.find_element_by_id("text-issues-tab").click()
    
    setup_and_teardown.find_element_by_id("text-row-0").send_keys("Ytext")
    
    setup_and_teardown.find_element_by_css_selector("tr#row-0 button.submit").click()
    
    
    setup_and_teardown.find_element_by_css_selector("tr#row-0 button.btn-success").click()
    
    setup_and_teardown.find_element_by_id("download-file").click()
    
    time.sleep(5)
    download_folder_xlsx = glob.glob(os.path.join(DOWNLOADS_PATH,"*.xlsx"))
    
    
    assert os.path.join(DOWNLOADS_PATH,"Detre Output (2).xlsx") in download_folder_xlsx
    
    