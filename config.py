# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 14:01:29 2021

@author: Detre
"""


from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class DevConfig:
    
    SECRET_KEY              = environ.get("SECRET_KEY")
    SESSION_TYPE            = 'sqlalchemy'
    SESSION_PERMANENT       = False
    MAX_CONTENT_LENGTH      = int(environ.get("MAX_UPLOAD_SIZE")) 
    UPLOAD_FOLDER           = environ.get('UPLOAD_FOLDER') 
    STATIC_FOLDER           = environ.get('STATIC_FOLDER') 
    
    DB_USER        = environ.get("DB_USER") 
    DB_PASSWORD    = environ.get("DB_PASSWORD")
    DB_HOST        = environ.get("DB_HOST")
    
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER +":" + DB_PASSWORD + "@" + DB_HOST  + "/detre"

    SQLALCHEMY_ECHO                = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS =  {
                                            
                                            'pool_pre_ping': True,
                                            "pool_size": 300,
                                            "pool_recycle": 300,
                                        }    