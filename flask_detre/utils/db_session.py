# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 15:35:02 2021

@author: 27608
"""



from sqlalchemy.orm import Session
from flask_detre import db
from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()