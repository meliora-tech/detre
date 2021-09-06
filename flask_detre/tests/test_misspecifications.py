# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 10:46:32 2021

@author: Detre
"""



import pytest
import requests
import os
import time
from flask import Flask, session
from flask_detre import create_app

app = create_app()
# app = Flask(__name__)
# app.secret_key = 'M?y-seCret_KEy'

#dirname = os.path.dirname(__file__)

#dirname = "C:\\Users\\27608\\Documents\\Detre\\flask_detre\\tests"
url = "http://localhost:8100/data"



def test_date_misspecification():
    # file = os.path.join(dirname,'files','date.csv')
    # files = {'file': open(file,'rb')}

    
    # Upload the file    
    #r =  requests.post("http://localhost:8100/",files=files)
    all_names = []
    data = {
        "filename": "date.csv",
        "columns": ["date"]
    }
    
    all_names.append(data)
    with app.test_client() as c:
        
        # with c.session_transaction() as sess:
            
        #     sess['all_names'] = all_names
        #     sess["name"]      = "3fc3f606-d51a-4b4c-95bf-bb6c1bc7247a- date.csv"
        #r =  requests.post("http://localhost:8100/",files=files)
        
        #all_columns = sess.get("all_names",[]) #sess.get("all_names",[])[0]['columns']
        #assert len(all_columns) == 1
        # Select the data type
        
        rs = c.post("/",data={"date-date.csv-select":'date'})
       
        # print(rs.get_data())
        assert rs.status_code == 200

    