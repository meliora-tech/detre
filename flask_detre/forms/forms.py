# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 13:07:49 2021

@author: Detre Team
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class EarlyAccessForm(FlaskForm):
    """
    Form for early access
    """
    email       = EmailField('email', validators=[DataRequired()])
    launch_sub  = BooleanField("Receive launch email",default="checked")
    letter_sub  = BooleanField("Subscribe to newsletter")
    join        = SubmitField("Join")
    
    
class SurveyMonkeyForm(FlaskForm):
    """
    Form for Survey Monkey file upload
    """
    
    survey_m =  FileField(validators=[FileRequired()])
    
    
class DetreUploadForm(FlaskForm):
    """
    Form for user file upload
    """
    
    detre_upload = FileField(validators=[FileRequired()])