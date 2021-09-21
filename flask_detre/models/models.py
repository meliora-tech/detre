# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 15:35:15 2021

@author: Detre
"""

from flask_detre import db

class CountryCodes(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(255))
    phone_code   = db.Column(db.String(255))
    country_code = db.Column(db.String(255))
    
    
class EarlyAccess(db.Model):
    
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(255))
    launch_sub = db.Column(db.Boolean)
    letter_sub = db.Column(db.Boolean)
    
    
    