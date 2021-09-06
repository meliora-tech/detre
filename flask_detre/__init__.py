# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 16:00:59 2021

@author: Detre
"""



from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask import Flask


db = SQLAlchemy()
sess = Session()


def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object('config.DevConfig')
    
    db.init_app(app)
    sess.init_app(app)
    
    
    # Register bluprints
    
    from flask_detre.routes.route import route_bp
    
    app.register_blueprint(route_bp)
    
    return app

