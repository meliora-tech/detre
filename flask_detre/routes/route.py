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
import logging

import pyexcel as pe
from pyexcel_xlsx import get_data

#from flask_detre import db
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask import Blueprint,Flask, flash ,request, jsonify, render_template, url_for, redirect,send_file, session
from flask_detre.utils.utils import (detre_date, get_correct_values_as_series, get_data_profile, 
                                     get_incorrect_values_as_df)
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

from flask_detre.models.models import EarlyAccess
from flask_detre.models.models import CountryCodes
from flask_detre.utils.text_constants import (DATE_ARR)

from flask_detre.utils.db_session import session_scope

from werkzeug.utils import secure_filename
from openpyxl import Workbook
from io import BytesIO



from flask_detre.forms.forms import (EarlyAccessForm, SurveyMonkeyForm, DetreUploadForm)


#from defusedxml.ElementTree import parse, fromstring
# Directory of the current file
dirname = os.path.dirname(__file__)

BLOG_URL = "http://127.0.0.1:8000"
LOG_FILE = os.path.join(dirname.replace("\\routes",'\\logs'),'app.log')
logging.basicConfig(level=logging.DEBUG,filename=LOG_FILE, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
route_bp  = Blueprint("route_bp",__name__)

#db.create_all()


@route_bp.errorhandler(413)
def too_large(e):
    """
    Error handling when a large file has been uploaded
    
    """
    logger.error("Large file uploaded")
    return "File size is large", 413


@route_bp.errorhandler(405)
def method_not_allowed(e):
    """
    Handle for 405 error
    """
    logger.error("Method not allowed error." + str(e))
    return "Method not allowed.", 405

@route_bp.route("/dates/constants")

def date_constants():
    """
    Get all the date formats from which the user can select for `extract` date
    """
    return jsonify({"result":DATE_ARR})

@route_bp.route("/blog")
def blog():
    """
    Display the blog page
    """
    return redirect(BLOG_URL)

@route_bp.route("/privacy")
def privacy():
    """
    Display the privacy and terms & conditions page
    """
    return render_template("privacy.html")


@route_bp.route("/faq")
def faq():
    """
    Display the FAQ page
    """
    return render_template("faq.html")


@route_bp.route("/resources")
def documentation():
    """
    Display the resources page
    """
    return render_template("documentation.html")

@route_bp.route("/", methods=['GET', 'POST'])
def upload_file():
    
    """
    POST: Handle the upload of the data file.
    
    GET: Display the home screen
    """
    
    if request.method == 'POST' and session["detre_csrf"] == request.form['csrf_token']:
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

                
            return redirect(url_for("route_bp.data_columns")), 204         
        except Exception as e:
            logger.exception("Upload file error: " + str(e))
            return redirect(url_for("route_bp.upload_file")), 401
        
        

    return render_template('home.html')


@route_bp.route("/early-access", methods=["GET","POST"])
def early_access():
    """
    GET : Display the sign up page for early access
    
    POST: {}
    """
    
    form = EarlyAccessForm()
    if form.validate_on_submit():
        email       = form.data['email']
        launch_sub  = form.data['launch_sub']
        letter_sub  = form.data['letter_sub']
        
        
        with session_scope() as session:
            early_access = EarlyAccess(email=email,launch_sub=launch_sub,letter_sub=letter_sub)
            
            session.add(early_access)
            
        
    
    
    
    
    return render_template("early_access.html",form=form)

@route_bp.route("/demo", methods=['GET'])
def demo():
    
    """
     POST: Handle the uploaded file
     GET:
    """
    form = DetreUploadForm()
    
    if request.method == 'POST':
        file =  request.files['file']
        
        all_names = []
        f         = secure_filename(file.filename)
        
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
       
        """
        Below code is kept for multiple file uploads handling. 
        To be used 
        """
        
        
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
    
    session["detre_csrf"] = form.csrf_token.current_token
    return render_template("demo.html",form=form)



@route_bp.route("/survey", methods=["GET","POST"])
def survey():
    """
    POST : Handle the uploaded Survey Monkey file
    GET  : Upload page for `Survey Monkey` file.
    """
    
    form = SurveyMonkeyForm()
    if request.method == "POST" and session['user_csrf'] == request.form['csrf_token'] :
        file = request.files['file']
        
        f    = secure_filename(file.filename)
        
        # Check if its secure
        
        
        
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
        
    session['user_csrf'] = form.csrf_token.current_token
    return render_template("survey.html",form=form)

@route_bp.route("/survey/analysis", methods=["GET"])
def survey_analysis():
    """
    API that runs the data cleaning on the Survey Monkey entries
    """
   
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
             logger.exception("Survey monkey analysis error: "+ str(e))
             flash(url_for("route_bp.survey"),"Something went wrong while cleaning your survey.")
             return redirect(url_for("route_bp.survey"))           
       
    else:
       return redirect(url_for("route_bp.survey")) 


@route_bp.route("/survey/analysis", methods=["GET"])
def download_survey():
    """
    Download the cleaned `Survey Monkey` file
    """
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
    """
    Display the column selection type page
    """
    if session.get('updated_value'):
        session["updated_value"] = None
        
    if session.get("all_columns"):
        session["all_columns"] = None
        
    all_names = session['all_names']
    return render_template("results.html",results= all_names  )
        
        
@route_bp.route("/data", methods=["GET","POST"])
def data():
    """
    Main function to run the data profile, find issues and correct values base on the given column type provided by
    the user
    """
    if request.method == "POST":
        form = request.form
        
        all_data    = []
        all_profile = []
        data_types  = {}
        
        # Get the form keys
        form_keys = form.keys()
        
        file_name = session.get('name','3fc3f606-d51a-4b4c-95bf-bb6c1bc7247a- date.csv')
       
        f         = file_name.split("- ")[1]
        
        
        # Get only the keys that have 'filename'
        file_keys = []
        for key in form_keys:
            
            
            if f in key:
                file_keys.append(key)
        
        # All columns (new ones also included)
        all_columns = session.get("all_names",[])[0]['columns']
        
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
                df_incorrect            = get_incorrect_values_as_df(phone_data)
                
                all_data.append({clean_k:phone_data})
                
                get_data_profile(df_correct,df_incorrect,clean_k,all_profile,"phone")
                data_types[clean_k] = "phone"
                
                all_columns.append(clean_k)
                
            elif dtype == "date":
                
                
                format_      = "%Y-%m-%d"
                date_data    = detre_date(df[clean_k],format_)
                
                df_correct   = get_correct_values_as_series(date_data)
                df_incorrect = get_incorrect_values_as_df(date_data)
                
                all_data.append({clean_k:date_data})
                
                if len(df_correct) != 0:
                    date_profile = detre_profile(df_correct,df_incorrect,"date")
                    
                    
                    
                    all_profile.append({clean_k:date_profile})
                else:
                    all_profile.append({clean_k:[]}) # No profile for the column
                    
                data_types[clean_k] = "date"
                all_columns.append(clean_k)
                
                
            elif dtype == "time":
                
                time_data           = detre_time(df[clean_k])
                df_correct          = get_correct_values_as_series(time_data)
                df_incorrect        = get_incorrect_values_as_df(time_data)
                
                
                all_data.append({clean_k:time_data})
                
                get_data_profile(df_correct, df_incorrect, clean_k,all_profile,"time")
                data_types[clean_k] = "time"  
                
                all_columns.append(clean_k)
                
            elif dtype == "datetime":
                datetime_data           = detre_datetime(df[clean_k])
                
                df_correct              = get_correct_values_as_series(datetime_data)
                df_incorrect            = get_incorrect_values_as_df(datetime_data)
                
                all_data.append({clean_k:datetime_data})
                
                get_data_profile(df_correct,df_incorrect,clean_k,all_profile,"datetime")
                data_types[clean_k] = "datetime"     
                
                all_columns.append(clean_k)
                
            elif dtype == "currency":
                currency_data           = detre_currency(df[clean_k])
                df_correct              = get_correct_values_as_series(currency_data)
                df_incorrect            = get_incorrect_values_as_df(currency_data) 
               
                all_data.append({clean_k   : currency_data})
                get_data_profile(df_correct,df_incorrect,clean_k,all_profile,"currency")
                
               
                data_types[clean_k] = "currency"    
                all_columns.append(clean_k)
                
            elif dtype == "whole":
                whole_data    = detre_wnumber(df[clean_k])
                df_correct    = get_correct_values_as_series(whole_data)
                df_incorrect            = get_incorrect_values_as_df(whole_data)
                
                all_data.append({clean_k:whole_data})
                
                get_data_profile(df_correct,df_incorrect,clean_k,all_profile,"whole")
                
                data_types[clean_k] = "whole"
                
                all_columns.append(clean_k)
                
            elif dtype == "decimal":
                decimal_data    = detre_decimal(df[clean_k])
                df_correct      = df_correct   = get_correct_values_as_series(decimal_data)
                df_incorrect            = get_incorrect_values_as_df(decimal_data)
                
                all_data.append({clean_k: decimal_data})
                
                
                
                get_data_profile(df_correct,df_incorrect,clean_k,all_profile,"decimal")
                data_types[clean_k]  = "decimal"
                
                all_columns.append(clean_k)
                
            elif dtype == "country":
                country_data    = detre_country(df[clean_k])
                df_correct      = get_correct_values_as_series(country_data)
                df_incorrect    = get_incorrect_values_as_df(country_data)
                
                all_data.append({clean_k:country_data})
                
                get_data_profile(df_correct,df_incorrect,clean_k,all_profile,"country")
                data_types[clean_k] = "country" 
                
                all_columns.append(clean_k)
                
            elif dtype == "text":
                 
                 remove_actions, extract_actions, replace_actions = [], [], []
                 remove_items, extract_items, replace_items       = [], [], []
                 
                 
                 for key in form.keys():
                     if "text-action-item" in key and clean_k in key:
                         
                         action = form[key].split(":")[0].strip().lower()
                         item   = form[key].split(":")[1].strip().lower()
                         
                         if "date" in item:
                             item = re.sub(r'[\d\()]+','',item).strip()
                             date_fmt = form["text-date"].split(",")
                    
                         
                         if action == "remove":
                             remove_actions.append("remove")
                             remove_items.append(item)
                         
                         if action == "extract":
                             extract_actions.append("extract")
                             extract_items.append(item)
                             
                         if action == "replace":
                             replace_actions.append("replace")
                             replace_items.append(item)
                 
                 # No action was provided but data type was selected as `text`   
                 if  len(remove_actions) == 0 and len(extract_actions) == 0:
                     text_data  = detre_text(df[clean_k],[],[])
                     all_data.append({clean_k:text_data})
                     
                     df_correct              = get_correct_values_as_series(text_data)
                     df_incorrect            = get_incorrect_values_as_df(text_data)
                     data_types[clean_k] = "text"
                     
                     get_data_profile(df_correct, df_incorrect, clean_k, all_profile, "text")

                     all_columns.append(clean_k)                     
                 
                 if len(remove_actions) > 0:
                     for action, item in zip(remove_actions,remove_items):
                         if item != "date":
                             text_data_remove  = detre_text(df[clean_k], remove_actions, remove_items)
                         else:
                            text_data_remove  = detre_text(df[clean_k], remove_actions, remove_items,date_fmt=date_fmt)
                        
                     all_data.append({clean_k:text_data_remove})
                     data_types[clean_k] = "text"
                     
                     all_columns.append(clean_k)
                 
                 if len(extract_actions) > 0:
                     for action, item in zip(extract_actions,extract_items):
                         if item!= "date":
                             text_data_extract = detre_text(df[clean_k],extract_actions,extract_items)
                         else:
                             text_data_extract = detre_text(df[clean_k],extract_actions,extract_items,date_fmt=date_fmt)
                         
                         df_correct              = get_correct_values_as_series(text_data_extract)
                         df_incorrect            = get_incorrect_values_as_df(text_data_extract)
                         
                         extract_profile   = detre_profile(df_correct,df_incorrect ,"text")
                         all_data.append({"new_"+clean_k+"_"+item:text_data_extract})
                         all_profile.append({"new_"+clean_k+"_"+item :extract_profile })
                        
                         data_types["new_" + clean_k + "_" + item] = "text-"+item.strip().lower()                     
                         
                         # Save the column name
                         all_columns.append("new_" + clean_k + "_" + item)
                         
                         # Save the correct data associated with the column
                         
                         session["new_" + clean_k + "_" + item] = text_data_extract[0]['correct']
                         
                 if len(replace_actions) > 0:
                     
                     text_data_replace  = detre_text(df[clean_k], replace_actions, replace_items)

                 
        # session 
        session["all_columns"] = all_columns        
        return render_template('clean.html',
                               all_data=all_data, data_types = data_types,
                               all_profile = all_profile,no_footer=True)
    
    # 
    
    return redirect(url_for("route_bp.demo"))


@route_bp.route("/update/value", methods=["POST"])
def update_value():
    """
    Use the given `action` to run an update for the provided row value
    """
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
    """
    Run the `action` across all values within the column.  
    
    Only values that have not been `accepted` or `removed` will be run
    """
    form = request.form
    
    file_name = session.get('name',None)
    if file_name:
        data = pd.read_table(os.path.join(dirname.replace("\\routes",''),'temp',file_name), sep=",") 
        
        row       = form["rows"].split(",")
        row       = [int(i)  for i in row]
        action    = form["action"]
        column    = form['column']
        data_type =form['data_type']
        
        # Check column name if it is for a new column or not
       
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
    """
    A user accepts the Detre update for the provided `action`
    """
    if session.get('updated_value'):
        
        form = request.form
        
        update = {
                     'column_name': form['column_name'],
                     'new_value': form['new_value'],
                     'old_value': form['old_value']
                     
                }    
        
        new_update               =  session['updated_value']
        new_update[form['row']]  = update
        session['updated_value'] = new_update
       
        
    else:
        form = request.form
       
        update = {
                     'column_name': form['column_name'], 
                     'new_value': form['new_value'],
                     'old_value': form['old_value']
                     
                }
    
       
        
        session['updated_value'] = {form['row'] :update}
        
        
    return "True"

@route_bp.route('/download/excel')
def excel():
    
    """
    API to download the results as an `xlsx` file
    
    There are two major parts:
        1. No changes were made
        2. Changes were made via user provided `actions`
        
    Within each part, a new column could have been created via the `extract` action. 
    """
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
        
        #===================================================================
        # 1. Get all the columns from the uploaded file 
        # 2. Get all columns from (1) above and also new one(s) if created 
        #====================================================================
        df_columns = df.columns.tolist()
        data_columns = session.get("all_columns",None)

        
        if data_columns is not None:
            if len(data_columns) == len(df_columns):
                
                #=========================
                # No new columns created
                #==========================
                ws.append(df.columns.tolist())
                for idx, td in df.iterrows():
                    if str(idx) in updated_values_keys:
                        data = update_values[str(idx)]
                        
                        sub_df  = df.iloc[idx,:]
                        
                        sub_df[data["column_name"]] = data['new_value']
                        
                        
                        ws.append(sub_df.tolist())
                        
                    else:
                        
                        ws.append(td.tolist())
                        
            else:
                for col in data_columns:
                    # Check if a new column 
                    if col not in df_columns: 
                        
                        # New column derived from which column
                        if "new_" in col:
                            column = col.replace("new_","")
                            column = re.sub("_[a-z]+$","",column)                    
                        
                        
                        # Get all the 'correct' rows
                        rows = { r['row']:idx for idx,r in enumerate(session[col]) }
                        
                        
                        column_values = []
                        for idx, td in enumerate(df.loc[:,column]):
                            if idx in list(rows.keys()):
                                    
                                    index = rows[idx]
                                    column_values.append(session[col][index]['detre'] )
                            else:
                                     column_values.append("")
                        
                        # Make a series with new column name 
                        series = pd.Series(column_values,name=col)
                        #series.name(col)
                        
                        # Join with df
                        df = df.join(series)     
                        
                
                # Get the updated values for the respective columns
                ws.append(df.columns.tolist())
                for idx, td in df.iterrows():
                    if str(idx) in updated_values_keys:
                        data = update_values[str(idx)]
                        sub_df  = df.iloc[idx,:]
                        sub_df[data["column_name"]] = data['new_value']
                        
                        
                        ws.append(sub_df.tolist())
                        
                    else:
                        
                        ws.append(td.tolist())                
            
        else:
            return redirect(url_for("demo"))
        
        
    else:
        #============================
        # No values were updated but new column(s) could
        # have been created via `extract`
        #===============================
        
        
        # 1. Get all the columns from the uploaded file 
        # 2. Get all columns from (1) above and also new one(s) if created 
        df_columns = df.columns.tolist()
        data_columns = session.get("all_columns",None)
        
        if data_columns is not None:
            for col in data_columns:
                # Check if a new column was created
                if col not in df_columns: 
                    
                    # New column derived from which column
                    if "new_" in col:
                        column = col.replace("new_","")
                        column = re.sub("_[a-z]+$","",column)                    
                    
                    # Get all the 'correct' rows
                    rows = { r['row']:idx for idx,r in enumerate(session[col]) }
                    
                    column_values = []
                    for idx, td in enumerate(df.loc[:,column]):
                        if idx in list(rows.keys()):
                            
                                index = rows[idx]
                                column_values.append(session[col][index]['detre'] )
                        else:
                                 column_values.append("")
                    
                    # Make a series with new column name 
                    series = pd.Series(column_values,name=col)
                    
                    #series.name(col)
                   
                    # Join with df
                    df = df.merge(series, left_index=True, right_index=True)
        else:
            return redirect(url_for("demo"))
        
        ws.append(df.columns.tolist())
        for idx,td in df.iterrows():
            ws.append(td.tolist())
    
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)


    return send_file(file_stream, attachment_filename="Detre Output.xlsx", as_attachment=True), 200


@route_bp.route("/country_codes")
def country_codes():
    """
    API to get all the phone country codes
    """
    country_codes = CountryCodes.query.all()
    
    
    data = []
    for cc in country_codes:
        result = {}
        result["country_code"] = cc.phone_code
        result["value"]        = "( " + cc.phone_code + " ) " + cc.country_name
        
        data.append(result)
    
    return jsonify({"result":data})
        