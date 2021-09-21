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
    options.add_argument("--window-size=1920, 2100")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("allow-insecure-localhost")
    # See the following: https://stackoverflow.com/questions/45631715/downloading-with-chrome-headless-and-selenium/47366981#47366981
    # https://stackoverflow.com/questions/45631715/downloading-with-chrome-headless-and-selenium
    options.add_experimental_option("prefs", {
          "download.default_directory": DOWNLOADS_PATH,
          "download.prompt_for_download": False,
        })

    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR, options=options)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': DOWNLOADS_PATH}}
    command_result = driver.execute("send_command", params)
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

    
    # form.send_keys("C:/Users/27608/Documents/Detre/flask_detre/tests/files/text.csv")

    

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
    
    time.sleep(2)
    setup_and_teardown.find_element_by_id("download-file").click()
    
    time.sleep(5)
    DOWNLOADS_PATH   = str(Path.home() / "Downloads")
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
    
    time.sleep(5)
    setup_and_teardown.find_element_by_id("add-text-btn").click()    
    
    time.sleep(2)
    setup_and_teardown.find_element_by_css_selector("button[type='submit']").click()
    
    time.sleep(5)
    setup_and_teardown.find_element_by_id("download-file").click()
    
    time.sleep(5)
    
    DOWNLOADS_PATH   = str(Path.home() / "Downloads")
    download_folder_xlsx = glob.glob(os.path.join(DOWNLOADS_PATH,"*.xlsx"))
    
    assert os.path.join(DOWNLOADS_PATH,"Detre Output.xlsx") in download_folder_xlsx


# def test_download_file_changes_normal(setup_and_teardown, request):
#     """
#     Test when a user makes changes via the data type keyboard
#     """
#     setup_and_teardown.get("http://www.localhost:8100/")
    
#     btn = setup_and_teardown.find_element_by_id("get-started")
#     btn.click()
    
#     form = setup_and_teardown.find_element_by_id("fallback-file")
    
#     fn = os.path.join(request.fspath.dirname,"files",text_file)
    
#     form.send_keys(fn)
    
#     time.sleep(2)    
    
#     # click proceed
#     setup_and_teardown.find_element_by_id("proceed").click()
     
#     select_name =  text_file.replace(".csv","") + "-" + text_file + "-select"  
#     select = Select(setup_and_teardown.find_element_by_name(select_name))
    
#     select.select_by_value("date")    
    
#     setup_and_teardown.find_element_by_css_selector("button[type='submit']").click()
    
#     # Make changes to the date
    
#     setup_and_teardown.find_element_by_id("text-column-tab").click()
    
#     setup_and_teardown.find_element_by_id("text-issues-tab").click()
    
#     setup_and_teardown.find_element_by_id("text-row-0").send_keys("Ytext")
    
#     setup_and_teardown.find_element_by_css_selector("tr#row-0 button.submit").click()
    
    
#     setup_and_teardown.find_element_by_css_selector("tr#row-0 button.btn-success").click()
    
#     time.sleep(2)
#     setup_and_teardown.find_element_by_id("download-file").click()
    
#     time.sleep(5)
    
#     download_folder_xlsx = glob.glob(os.path.join(DOWNLOADS_PATH,"*.xlsx"))
    
    
#     assert os.path.join(DOWNLOADS_PATH,"Detre Output (2).xlsx") in download_folder_xlsx
    
    