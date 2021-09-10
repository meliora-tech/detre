# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 16:48:20 2021

@author: Detre
"""

from selenium import webdriver

import os
import pytest
import requests



CHROMEDRIVER_DIR = "C:/Users/27608/Documents/Chrome Drivers/chromedriver"  


@pytest.fixture
def setup_and_teardown():
        
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR, options=options)
    #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR)
    yield driver
    
    driver.close()




def test_upload_different_file_formats_frontend():
    """
    Test for uploads: xlsx, csv, json, tsv, ord, txt
    """
    pass


def test_upload_different_file_sizes_frontend():
    """
    
    """
    
    pass



@pytest.mark.parametrize("fn,code",[("text.txt",401),("text.xlsx",204),("text.csv",204),("text.tsv",204),("text.ods",401)])
def test_upload_different_file_formats_backend(request,fn,code):
    """
    Test for uploads: xlsx, csv, tsv, ods, txt
    """
    file = os.path.join(request.fspath.dirname,"files",fn) 
    resp = requests.post("http://localhost:8100",files={'file': open(file,'rb')})
    
    assert resp.status_code == code
    




@pytest.mark.parametrize("fn,code",[("text.xlsx",204),("big_file.xlsx",413)])
def test_upload_different_file_sizes_backend(request,fn,code):
    """
    Test for different file sizes: < 0.5MB, 1.0MB, 1.5MB, 2.0MB, > 2MB
    """
    file = os.path.join(request.fspath.dirname,"files",fn) 
    resp = requests.post("http://localhost:8100",files={'file': open(file,'rb')})
    
    assert resp.status_code == code
    