# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 13:36:26 2021

@author: Detre Team
"""

import pytest
import requests

url = 'http://localhost:8100'

def test_download_excel_file():
    
    
    
    resp = requests.get(url+'/excel/download')
    
    # Assert status code
    assert 200 == resp.status_code
    
    # Assert the header
    assert 'attachment; filename=detre.xlsx' == resp.headers['Content-Disposition']