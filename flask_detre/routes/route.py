# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 10:03:18 2021

@author: Detre
"""




import pandas as pd
import sidetable
import os
import re
import json
import uuid

import pyexcel as pe
from pyexcel_xlsx import get_data


from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask import Blueprint,Flask, flash ,request, jsonify, render_template, url_for, redirect,send_file, session
from flask_detre.utils.utils import (detre_date, get_correct_values_as_series)
from flask_detre.utils.detre_update_values import (detre_update_value, detre_update_multiple_values)
from flask_detre.utils.phone_number import detre_phone
from flask_detre.utils.time import detre_time
from flask_detre.utils.datetime_ import detre_datetime
from flask_detre.utils.currency import detre_currency
from flask_detre.utils.country import detre_country
from flask_detre.utils.text import detre_text
from flask_detre.utils.profile import detre_profile
from flask_detre.utils.whole_number import detre_wnumber
from flask_detre.utils.decimal import detre_decimal
from flask_detre.utils.survey_monkey import survey_monkey_analysis


from flask_detre.models.models import CountryCodes

from werkzeug.utils import secure_filename
from openpyxl import Workbook
from io import BytesIO


route_bp  = Blueprint("route_bp",__name__)

#db.create_all()
# Directory of the current file
dirname = os.path.dirname(__file__)

@route_bp.errorhandler(413)
def too_large(e):
    return "File size is large", 413


@route_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@route_bp.route("/faq")
def faq():
    return render_template("faq.html")


@route_bp.route("/resources")
def documentation():
    return render_template("documentation.html")

@route_bp.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file =  request.files['file']
        
        all_names = []
        f = secure_filename(file.filename)
        
        
       
        f  = str(uuid.uuid4()) + "- " + f
        # save to temp folder
        file.save(os.path.join(dirname.replace("\\routes",''),'temp',f))
        
        
        
        try:
            filename_    = os.path.join(dirname.replace("\\routes",''),'temp',f) 
            dict_        = pe.get_dict(file_name=filename_)
            data_xls     = pd.DataFrame(dict_)
           
            
            
            data = {
                    "filename": f.split("- ")[1],
                    "columns": [c.strip() for c in list(data_xls.columns)]
                }
            all_names.append(data)
           
            session['all_names'] = all_names
            session["name"]      = f

                
            return '', 204         
        except Exception as e:
            
            return redirect(url_for("route_bp.upload_file"))
        
        

    return render_template('home.html')


@route_bp.route("/early-access", methods=["GET","POST"])
def early_access():
    
    return render_template("early_access.html")

@route_bp.route("/demo", methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        file =  request.files['file']
        
        all_names = []
        f = secure_filename(file.filename)
        
        dict_        = pe.get_dict(file_contents=file)
        data_xls     = pd.DataFrame(dict_)        
        
        
        #data_xls = pd.read_table(file, sep=",")
        data = {
                "filename": f,
                "columns": [c.strip() for c in list(data_xls.columns)]
            }
        all_names.append(data)
       
        session['all_names'] = all_names
        session["name"] = f
        # Write the file to temp folder
        data_xls.to_csv( os.path.join(dirname.replace("\\routes",''),'temp',f), index=None, sep=',')        
       
        # for idx,file in enumerate(file_list):
        #    f = secure_filename(file.filename)
           
        #    data_xls = pd.read_table(file, sep=",")
        #    data = {
        #            "filename": f,
        #            "columns": list(data_xls.columns)
        #        }
        #    all_names.append(data)
           
        #    session["name"] = f
        #    # Write the file to temp folder
        #    data_xls.to_csv('temp/'+f, index=None, sep=',')
            
        return '', 204 #data_xls.to_html()    
    
    return render_template("demo.html")



@route_bp.route("/survey", methods=["GET","POST"])
def survey():
    
    if request.method == "POST":
        file = request.files['file']
        
        f    = secure_filename(file.filename)
        
        f  = str(uuid.uuid4()) + "- " + f
        # save to temp folder
        file.save(os.path.join(dirname.replace("\\routes",''),'temp',f))
        
        filename_    = os.path.join(dirname.replace("\\routes",''),'temp',f) 
        survey_df    = pd.read_excel(filename_, header=[0,1])
        
        # Check if indeed a survey monkey file
        # Any column `respondent id`
        survey_columns = survey_df.columns.to_frame(index=0, name=["question",'options'])
        
        if sum(survey_columns["question"].str.strip().str.lower() == "respondent id") == 1:
            
            session["name"] = f
            return redirect(url_for("route_bp.survey_analysis"))
        else:
             flash(url_for("survey"),"Not a Survey Monkey survey")
             return redirect(url_for("route_bp.survey"))
        
    
    return render_template("survey.html")

@route_bp.route("/survey/analysis", methods=["GET"])
def survey_analysis():
    
   
    if session.get('name'):
       
       # Get the clean survey
       try:
           clean_survey = survey_monkey_analysis(dirname,session["name"]) 
           
           # save the clean survey
           f     = "clean-" + session["name"]
           file_ = os.path.join(dirname.replace("\\routes",''),'temp',f)
           clean_survey.to_excel(file_, engine='openpyxl')
           
           session["survey_name"] = f
           return send_file(file_, attachment_filename="Clean Survey Monkey Output.xlsx", as_attachment=True), 200
       
       except Exception as e:
             
             flash(url_for("survey"),"Something went wrong while cleaning your survey.")
             return redirect(url_for("route_bp.survey"))           
       
    else:
       return redirect(url_for("route_bp.survey")) 


@route_bp.route("/survey/analysis", methods=["GET"])
def download_survey():
    
    if session.get("survey_name"):
        try:
            file_ = os.path.join(dirname.replace("\\routes",''),'temp',session["survey_name"])
            return send_file(file_, attachment_filename="Clean Survey Monkey Output.xlsx", as_attachment=True), 200
        except:
            flash("Error occurred while downloading the survey.")
            return redirect(url_for("route_bp.survey")) 
    else:
        return redirect(url_for("route_bp.survey")) 
    

@route_bp.route('/columns')
def data_columns():
    all_names = session['all_names']
    return render_template("results.html",results= all_names  )
        
        
@route_bp.route("/data", methods=["GET","POST"])
def data():
    
    if request.method == "POST":
        form = request.form
        
        all_data    = []
        all_profile = []
        data_types  = {}
        
        # Get the form keys
        form_keys = form.keys()
        file_name = session.get('name','')
        f         = file_name.split("- ")[1]
        
        
        # Get only the keys that have 'filename'
        file_keys = []
        for key in form_keys:
            
            
            if f in key:
                file_keys.append(key)
        
        # Grab column name and type for a given 'filename'
        
        kv = {}
        
        for col in file_keys:
            kv[col] = form[col] 
        
        # Read in the 'filename'
        
        #df = pd.read_table(os.path.join(dirname.replace("\\routes",''),'temp',file_name), sep=",")
        filename_    = os.path.join(dirname.replace("\\routes",''),'temp',file_name) 
        dict_        = pe.get_dict(file_name=filename_)
        df           = pd.DataFrame(dict_)        

        
        # Match the excel data types with pandas data types
        type_dict = {}
        for k,dtype in kv.items():
            clean_k = k.replace("-"+f +"-select","")
            
            if dtype == "phone":
                # Make int
                
                type_dict[clean_k] = int
                country_code = form[clean_k + "-country-code-select"]
                session["country_code"] = country_code

                phone_data    = detre_phone(df[clean_k], country_code)
                
                df_correct    = get_correct_values_as_series(phone_data)
                
                phone_profile = detre_profile(df_correct, "phone")
                
                all_data.append({clean_k:phone_data})
                all_profile.append({clean_k: phone_profile })
                data_types[clean_k] = "phone"
                
            elif dtype == "date":
                
                
                format_      = "%Y-%m-%d"
                date_data    = detre_date(df[clean_k],format_)
                
                df_correct   = get_correct_values_as_series(date_data)
                date_profile = detre_profile(df_correct,"date")
                
                
                all_data.append({clean_k:date_data})
                all_profile.append(date_profile)
                data_types[clean_k] = "date"
               
                
            elif dtype == "time":
                
                time_data           = detre_time(df[clean_k])
                df_correct          = get_correct_values_as_series(time_data)
                time_profile        = detre_profile(df_correct, "time")
                
                all_data.append({clean_k:time_data})
                all_profile.append({clean_k:time_profile})
                data_types[clean_k] = "time"  
                
            elif dtype == "datetime":
                datetime_data           = detre_datetime(df[clean_k])
                
                df_correct              = get_correct_values_as_series(datetime_data)
                datetime_profile        = detre_profile(df_correct,"datetime")
                
                all_data.append({clean_k:datetime_data})
                all_profile.append({clean_k:datetime_profile})
                data_types[clean_k] = "datetime"     
                
            elif dtype == "currency":
                currency_data           = detre_currency(df[clean_k])
                df_correct              = get_correct_values_as_series(currency_data)
                
                currency_profile        = detre_profile(df_correct,"currency")
                
                all_data.append({clean_k   : date_data})
                all_profile.append({clean_k: currency_profile })
                data_types[clean_k] = "currency"    

            elif dtype == "whole":
                whole_data    = detre_wnumber(df[clean_k])
                df_correct    = get_correct_values_as_series(whole_data)
                
                whole_profile = detre_profile(df_correct,"whole")
                
                all_data.append({clean_k:whole_data})
                all_profile.append({clean_k:whole_profile})
                
                data_types[clean_k] = "whole"
                
            elif dtype == "decimal":
                decimal_data    = detre_decimal(df[clean_k])
                df_correct      = df_correct   = get_correct_values_as_series(decimal_data)

                decimal_profile = detre_profile(df_correct,"decimal")
                all_data.append({clean_k: decimal_data})
                
                all_profile.append({clean_k:decimal_profile})
                
                data_types[clean_k]  = "decimal"
                
                
            elif dtype == "country":
                country_data    = detre_country(df[clean_k])
                df_correct      = get_correct_values_as_series(country_data)
                
                country_profile = detre_profile(df_correct, "country") 
                all_data.append({clean_k:country_data})
                all_profile.append({clean_k :country_profile })
                data_types[clean_k] = "country" 

            elif dtype == "text":
                 remove_actions, extract_actions, replace_actions = [], [], []
                 remove_items, extract_items, replace_items       = [], [], []
                 
                 
                 for key in form.keys():
                     if "text-action-item" in key and clean_k in key:
                         
                         action = form[key].split(":")[0].strip().lower()
                         item   = form[key].split(":")[1].strip().lower()
                 
                         if action == "remove":
                             remove_actions.append("remove")
                             remove_items.append(item)
                         
                         if action == "extract":
                             extract_actions.append("extract")
                             extract_items.append(item)
                             
                         if action == "replace":
                             replace_actions.append("replace")
                             replace_items.append(item)
                 
                 
                 if len(remove_actions) > 0:
                     text_data_remove  = detre_text(df[clean_k], remove_actions, remove_items)
                     all_data.append({clean_k:text_data_remove})
                     data_types[clean_k] = "text"
                 
                 if len(extract_actions) > 0:
                     for action, item in zip(extract_actions,extract_items):
                         text_data_extract = detre_text(df[clean_k],extract_actions,extract_items)
                         all_data.append({  "new_"+clean_k+"_"+item:text_data_extract})
                         data_types["new_" + clean_k + "_" + item] = "text-"+item.strip().lower()                     
                
                 if len(replace_actions) > 0:
                     
                     text_data_replace  = detre_text(df[clean_k], replace_actions, replace_items)

                 
                
        return render_template('clean.html',
                               all_data=all_data, data_types = data_types,
                               all_profile = all_profile)


@route_bp.route("/update/value", methods=["POST"])
def update_value():
    
    form = request.form
    
    file_name = session.get('name',None)
    if file_name:
        data = pd.read_table(os.path.join(dirname.replace("\\routes",''),'temp',file_name), sep=",") 
        
        row = int(form["row"])
        action = form["action"]
        column = form['column']
        data_type =form['data_type']
        
        # Check column name if it is for a new column or not
       
        if "new_" in column:
            column = column.replace("new_","")
            column = re.sub("_[a-z]+$","",column)
        
        value = data.loc[row,column]

        try:
            new_value = detre_update_value(value,action,data_type)
        except:
            new_value = None
            
        if new_value:
            return jsonify({'error':0,'row': row ,'result':new_value})
        else:
            return jsonify({'error':1,'row': row ,'result':new_value})
    else:
        return jsonify({'error':2,'result':'Upload file again. Session expired and file was deleted.'})


@route_bp.route("/update/multiple/values", methods=["POST"])
def update_multiple_values():
    
    form = request.form
    
    file_name = session.get('name',None)
    if file_name:
        data = pd.read_table(os.path.join(dirname.replace("\\routes",''),'temp',file_name), sep=",") 
        
        row       = form["rows"].split(",")
        row       = [int(i)  for i in row]
        action    = form["action"]
        column    = form['column']
        data_type =form['data_type']
        
        # # Check column name if it is for a new column or not
       
        if "new_" in column:
            column = column.replace("new_","")
            column = re.sub("_[a-z]+$","",column)
        
        values = data[column].loc[row]
        
        
        new_values = detre_update_multiple_values(values,action,data_type)
  
            
            
        if new_values:
            return jsonify({'error':0,'row': row ,'result':new_values})
        else:
            return jsonify({'error':1,'row': row ,'result':new_values})
    else:
        return jsonify({'error':2,'result':'Upload file again. Session expired and file was deleted.'})
        
    
    
@route_bp.route("/accept/update", methods=["POST"])
def accept_change():
    if session.get('updated_value'):
        
        form = request.form
       
        update = {
                   
                     'new_value': form['new_value'],
                     'old_value': form['old_value']
                     
                }    
        
        new_update               =  session['updated_value']
        new_update[form['row']]  = update
        session['updated_value'] = new_update
       
        
    else:
        form = request.form
        update = {
                  
                     'new_value': form['new_value'],
                     'old_value': form['old_value']
                     
                }
    
       
        
        session['updated_value'] = {form['row'] :update}
        
        
    return "True"

@route_bp.route('/excel/download', methods=["GET"])
def excel_download():
    wb = Workbook()
    ws = wb.active
    
    # File name
    file_name = session.get('name','')
   
    
    # Read in the data        
    df = pd.read_table( os.path.join(dirname.replace("\\routes",''),'temp',file_name), sep=",")
    
    # Check if data has been updated
    if session.get('updated_value'):
        
        updated_values_keys = session.get('updated_value').keys()
        update_values       = session.get('updated_value')
        for idx,td in enumerate(df.iloc[:,0]):
            if str(idx) in updated_values_keys:
                data = update_values[str(idx)]
                ws.append(data['new_value'])
                
            else:
                
                ws.append([td])
        
        
        
    else:
        # No values were updated
        for idx,td in enumerate(df.iloc[:,0]):
            ws.append([td])
    
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(file_stream, attachment_filename="detre.xlsx", as_attachment=True), 200

@route_bp.route("/country_codes")
def country_codes():
    country_codes = CountryCodes.query.all()
    
    
    data = []
    for cc in country_codes:
        result = {}
        result["country_code"] = cc.phone_code
        result["value"]        = "( " + cc.phone_code + " ) " + cc.country_name
        
        data.append(result)
    
    return jsonify({"result":data})
        